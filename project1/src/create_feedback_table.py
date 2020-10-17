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
INSERT INTO Feedback (author, content) VALUES('admin','This feedback is from Admin');
INSERT INTO Feedback (author, content) VALUES('alice','This feedback is from Alice');
INSERT INTO Feedback (author, content) VALUES('bob','This feedback is from Bob');
COMMIT;
"""

conn = sqlite3.connect('src/db.sqlite3')
conn.cursor().executescript(db)
conn.commit()
