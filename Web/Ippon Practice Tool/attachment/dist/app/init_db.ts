import { existsSync, mkdirSync } from "fs";
import type { Database } from "sqlite";

export async function dbInit(db: Database) {
  await db.run(`CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT UNIQUE,
      password TEXT
    )`);
  await db.run(`CREATE TABLE IF NOT EXISTS odai (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      text INTEGER NOT NULL
    )`);
  await db.run(`CREATE TABLE IF NOT EXISTS answer (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      owner INTEGER NOT NULL,
      odai INTEGER NOT NULL,
      content TEXT NOT NULL,
      private BOOLEAN NOT NULL,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN KEY(odai) REFERENCES odai(id),
      FOREIGN KEY(owner) REFERENCES users(id)
    )`);
  await db.run(`INSERT INTO odai (text) VALUES('おばあちゃんのスマホに勝手に入っていた怪しすぎるアプリとは？')`)
  await db.run(`INSERT INTO odai (text) VALUES('異世界に転生したらこんな脆弱性が悪用されていた！どんな脆弱性？')`)
  await db.run(`INSERT INTO odai (text) VALUES('今年のShift_JISコード')`)
  await db.run(`INSERT INTO odai (text) VALUES('最新AIアシスタントが絶対に答えてくれないNG質問とは？')`)
  await db.run(`INSERT INTO odai (text) VALUES('パスワードに『password』を設定したら会社からの警告メールが届いた。どんな内容？')`)
  await db.run(`INSERT INTO odai (text) VALUES('アホアホ大学情報理工学部にありがちなこと。')`)
}
