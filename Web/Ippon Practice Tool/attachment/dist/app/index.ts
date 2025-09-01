// app.js
import express from "express";
import type { Request, Response, NextFunction } from "express";
import sqlite3 from "sqlite3";
import path from "path";
import cookieParser from "cookie-parser";
import crypto from "crypto";
import bcrypt from "bcrypt";
import { open } from "sqlite";
import type { Database } from "sqlite";
import { fileURLToPath, URL } from "url";
import { dbInit } from "./init_db.ts";

const PORT = process.env.PORT || 3000;
const REPORT_URL = process.env.REPORT_URL || "http://localhost:8080/";

const app = express();
const secret = crypto.randomBytes(32).toString("hex");
let db: Database;

app.use(express.urlencoded({ extended: false }));
app.use(cookieParser(secret));
app.use("/static", express.static(path.resolve("static")));

app.set("views", path.resolve("views"));
app.set("view engine", "ejs");

app.use((req: Request, res: Response, next: NextFunction) => {
  res.locals.nonce = crypto.randomBytes(32).toString("hex");
  res.setHeader(
    "Content-Security-Policy",
    `default-src 'self'; img-src *; script-src 'none'; style-src 'nonce-${res.locals.nonce}'`
  );
  next();
});

async function openDb() {
  const db = await open({
    filename: ":memory:",
    driver: sqlite3.Database,
  });
  await dbInit(db);
  return db;
}

function escapeLike(str: string) {
  return str.replace(/\\/g, "\\\\").replace(/%/g, "\\%").replace(/_/g, "\\_");
}

async function authMiddleware(req: Request, res: Response, next: NextFunction) {
  const { uid } = req.signedCookies;
  if (!uid) {
    return res.redirect("/login");
  }
  const row = await db.get("SELECT id FROM users WHERE id = ?", uid);
  if (!row) {
    return res.redirect("/login");
  }
  req.uid = parseInt(uid, 10);
  next();
}

app.get("/", authMiddleware, async (req: Request, res: Response) => {
  const uid = req.uid;
  const answers = await db.all(
    `SELECT a.id, o.text, a.created_at, a.content, a.private, u.username FROM answer AS a INNER JOIN odai AS o ON a.odai=o.id INNER JOIN users AS u ON a.owner=u.id WHERE NOT a.private OR a.owner=? ORDER BY created_at DESC LIMIT 50`,
    uid
  );
  const odai = await db.all(`SELECT * FROM odai`);
  return res.render("index", { answers, odai });
});

app.get("/register", (req: Request, res: Response) =>
  res.render("register", { message: false })
);
app.post("/register", async (req: Request, res) => {
  const { username, password } = req.body;
  if (typeof username !== "string" || typeof password !== "string") {
    return res.status(401).render("register", { message: "Invalid fields" });
  }

  const exists = await db.get(
    "SELECT id FROM users WHERE username = ?1",
    username
  );
  if (exists) {
    return res.status(409).render("register", { message: "User exists" });
  }

  const pwHash = await bcrypt.hash(password, 10);
  const result = await db.run(
    "INSERT INTO users (username, password) VALUES (?1, ?2)",
    username,
    pwHash
  );
  const id = result.lastID;
  res.cookie("uid", id?.toString() ?? "", {
    signed: true,
    httpOnly: true,
  });
  res.redirect("/");
});

app.get("/login", (req: Request, res: Response) =>
  res.render("login", { message: false })
);
app.post("/login", async (req: Request, res: Response) => {
  const { username, password } = req.body;
  if (typeof username !== "string" || typeof password !== "string") {
    return res.status(401).render("login", { message: "Invalid fields" });
  }
  const user = await db.get(
    "SELECT id, password FROM users WHERE username = ?1",
    username
  );
  if (!user) {
    return res.status(401).render("login", { message: "Invalid user" });
  }

  const match = await bcrypt.compare(password, user.password);
  if (!match) {
    return res.status(401).render("login", { message: "Invalid user" });
  }

  res.cookie("uid", user.id.toString(), {
    signed: true,
    httpOnly: true,
  });
  res.redirect("/");
});

app.post("/answer", authMiddleware, async (req: Request, res: Response) => {
  const uid = (req as any).uid;
  const { answer, odai, private: _private } = req.body;
  const priv = _private === "true";
  const odaiId = parseInt(odai);
  if (typeof answer !== "string" || isNaN(odaiId)) {
    return res.status(400).send("Invalid fields");
  }

  const result = await db.run(
    `INSERT INTO answer (owner, odai, content, private) VALUES (?, ?, ?, ?)`,
    uid,
    odaiId,
    answer,
    priv
  );
  res.redirect("/");
});

app.get("/answer/:id", authMiddleware, async (req: Request, res: Response) => {
  const uid = (req as any).uid;

  const answer = await db.get(
    `SELECT a.id, o.text, a.created_at, a.content FROM answer AS a INNER JOIN odai AS o ON a.odai=o.id WHERE a.id=? AND (a.owner=? OR NOT a.private)`,
    req.params.id,
    uid
  );
  if (!answer) {
    return res.status(404).send("Not found");
  }
  res.render("answer", { answer });
});

app.get("/search", authMiddleware, async (req: Request, res: Response) => {
  const uid = (req as any).uid;
  const q: string = req.query.q?.toString() || "";

  if (q.length === 0) {
    return res.end("<html><body>Invalid query. <a href='/'>Home</a></body></html>");
  }
  const answers = await db.all(
    `SELECT a.id, o.text, a.created_at FROM answer AS a INNER JOIN odai AS o ON a.odai=o.id WHERE owner = ? AND content LIKE ? ESCAPE '\\' ORDER BY created_at DESC `,
    uid,
    `%${escapeLike(q)}%`
  );

  if (answers.length === 0) {
    return res.end("<html><body>Not found. <a href='/'>Home</a></body></html>");
  }
  return res.render("search", { answers });
});

app.get("/report", (req: Request, res: Response) =>
  res.redirect(`${REPORT_URL}?id=${req.query.id}`)
);

(async () => {
  db = await openDb();
  app.listen(PORT, () => {
    console.log(`Express server listening on http://localhost:${PORT}`);
  });
})();
