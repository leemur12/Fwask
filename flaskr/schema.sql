DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS pics;

CREATE TABLE user(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL,
  date_joined DATE
);

CREATE TABLE pics(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT,
  owner_id INTEGER NOT NULL,
  string_path TEXT NOT NULL,
  FOREIGN KEY (owner_id) REFERENCES user (id)

);
