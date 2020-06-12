import sqlite3
import json

conn = sqlite3.connect('rosterdb.sqlite')
c = conn.cursor()

c.executescript('''
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;
CREATE TABLE User (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name   TEXT UNIQUE
);
CREATE TABLE Course (
    id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    title  TEXT UNIQUE
);
CREATE TABLE Member (
    user_id     INTEGER,
    course_id   INTEGER,
    role        INTEGER,
    PRIMARY KEY (user_id, course_id)
)
''')

fname = input("Enter file name: ")
if len(fname) < 1:
    fname = 'roster_data.json'

data = open(fname).read()
js = json.loads(data)

for info in js:
    name = info[0]
    course = info[1]
    role = info[2]
    print( name, course, role)

    c.execute('INSERT OR IGNORE INTO Course (title) VALUES (?)', (course,))
    c.execute('SELECT id FROM Course WHERE title = ?', (course,))
    course_id = c.fetchone()[0]

    c.execute('INSERT OR IGNORE INTO User (name) VALUES (?)', (name,))
    c.execute('SELECT id FROM User WHERE name = ?', (name,))
    user_id = c.fetchone()[0]

    c.execute('INSERT OR REPLACE INTO Member (user_id, course_id, role) VALUES (?,?,?)', (user_id, course_id, role))

conn.commit()
