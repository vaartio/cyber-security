import sqlite3
import os

db = \
"""
PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
CREATE TABLE Feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author varchar(200),
	content TEXT NOT NULL
);
INSERT INTO Feedback (author, content) VALUES('johndoe','This is great!');
COMMIT;
"""

conn = sqlite3.connect('src/db.sqlite3')
conn.cursor().executescript(db)
conn.commit()
