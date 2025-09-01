import express from "express";
import rateLimit from "express-rate-limit";
import { visit } from "./bot.js";

const PORT = process.env.PORT ?? "1337";

const app = express();
app.set("view engine", "ejs");

app.use(express.json());

app.get("/", async (_req, res) => {
  return res.render("./index.ejs");
});

app.use(
  "/api",
  rateLimit({
    windowMs: 60 * 1000,
    max: 4,
  })
);

app.post("/api/report", async (req, res) => {
  const { url } = req.body;
  if (
    typeof url !== "string" || !/^https?:\/\/.+$/.test(url)
  ) {
    return res.status(400).send("Invalid url");
  }

  try {
    await visit(url);
    return res.send("OK");
  } catch (e) {
    console.error(e);
    return res.status(500).send("Something wrong");
  }
});

app.listen(PORT, () => {
    console.log(`Listening on http://localhost:${PORT}`);
});
