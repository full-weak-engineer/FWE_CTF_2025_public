import express from "express";
import rateLimit from "express-rate-limit";
import { visit } from "./bot.js";

const PORT = process.env.PORT ?? "1337";

const app = express();
app.set("view engine", "ejs");

app.use(express.json());
const envs = {
  APP_URL: process.env.APP_URL ?? "http://localhost:1337",
  FLAG: (process.env.FLAG ?? "fwectf{fake_flag}"),
};

app.use(
  "/api",
  rateLimit({
    windowMs: 60 * 1000,
    max: 4,
  })
);

app.get("/report", async (req, res) => {
  const { id } = req.query;
  if (typeof id !== "string" || !/^\d+$/.test(id)) {
    return res.status(400).send("Invalid id");
  }

  try {
    const url = `${envs.APP_URL}/answer/${id}`;
    await visit(url, envs);
    return res.send("OK");
  } catch (e) {
    console.error(e);
    return res.status(500).send("Something wrong");
  }
});

app.listen(PORT, () => {
  console.log(`Listening on http://localhost:${PORT}`);
});
