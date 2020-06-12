import sqlite3
import xml.etree.ElementTree as ET

conn = sqlite3.connect('trackdb.sqlite')
c = conn.cursor()

c.executescript('''
DROP TABLE IF EXISTS Artist;
DROP TABLE IF EXISTS Album;
DROP TABLE IF EXISTS Genre;
DROP TABLE IF EXISTS Track;

CREATE TABLE Artist (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE);

CREATE TABLE Genre (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    name TEXT UNIQUE);

CREATE TABLE Album (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    artist_id INTEGER,
    title TEXT UNIQUE);

CREATE TABLE Track (
    id  INTEGER NOT NULL PRIMARY KEY 
    AUTOINCREMENT UNIQUE,
    title TEXT UNIQUE,
    album_id INTEGER,
    genre_id INTEGER,
    len INTEGER, 
    rating INTEGER, 
    count INTEGER);

''')

conn.commit()

fname = input('Enter file name: ')
if ( len(fname) < 1 ) :
    fname = 'Library.xml'

def lookup(dic, attribute):
    found = False
    for child in dic:
        if found : return child.text
        if child.tag == 'key' and child.text == attribute :
            found = True
    return None

# What this lookup(d, key) function does is parse through d (the xml code in question)
# and finds the specific key you are interested in and returns the corresponding value,
# which is in the next bit of code (child) right after the key:

# Initially found is set to False.
# The function will start looping through the code, where child always has a <tag>text</tag> format.
# When the function finds a child that is a key, i.e. where the tag is <key>text</key> (child.tag == 'key')
# and it is the specific key you wanted (child.text == key), found is set to True, otherwise it will remain False.
# Don't get confused by the two keys here. The 'key' in child.tag == 'key' refers to the type of
# tag in question, while key in child.text == key is the second argument in the lookup(d, key) function.
# In this instance, where the key is 'Track ID', found will be True if the child is <key>Track ID</key>.
# So the loop goes to the next child after <key>Track ID</key>, which is <integer>369</integer>.
# Here found is True, so the function will exit here at line 4 and return child.text that is '369', which
# is the corresponding value to the 'Track ID' key. Note that the return statement exits the whole function,
# not just the for loop! * Therefore, the function will only go to line 7 and return None if it couldn't find ' \
# 'the specific key you wanted. In this instance, there was no Track ID (<key>Track ID</key>) in the code it parsed

stuff = ET.parse(fname)
all = stuff.findall('dict/dict/dict')
print('Dict count:', len(all))
print(all)
for entry in all:
    if (lookup(entry, 'Track ID') is None ) : continue

    name = lookup(entry, 'Name')
    artist = lookup(entry, 'Artist')
    album = lookup(entry, 'Album')
    count = lookup(entry, 'Play Count')
    rating = lookup(entry, 'Rating')
    length = lookup(entry, 'Total Time')
    genre = lookup(entry, 'Genre')

    if name is None or artist is None or album is None or genre is None:
        continue

# The statement if ( lookup(entry, 'Track ID') is None ): is basically a boolean.
# Remember that lookup(entry, 'Track ID') will return None if there was no <key>Track ID</key> in entry.
# Which makes the statement in question if ( None is None ): True, so the the lines after the continue
# are skipped and it jumps to the next entry in all. Because, in theory, all tracks should have a
# Track ID, there is no point in looking for the name, artist...and the rest. What is more, it might
# give us erroneous data. It is best just ignore this block of code even if it was at the
# right ('dict/dict/dict') level.


    print(name, artist, album, count, rating, length, genre)

    c.execute('''INSERT OR IGNORE INTO Artist (name) VALUES (?)''', (artist,))
    c.execute('SELECT id FROM Artist WHERE name = ?', (artist,))
    artist_id = c.fetchone()[0]

    c.execute('''INSERT OR IGNORE INTO Album (artist_id, title) VALUES (?,?)''', (artist_id, album,))
    c.execute('SELECT id FROM Album WHERE title = ?', (album,))
    album_id = c.fetchone()[0]

    c.execute('''INSERT OR IGNORE INTO Genre (name) VALUES (?)''', (genre,))
    c.execute('SELECT id FROM Genre WHERE name = ?', (genre,))
    genre_id = c.fetchone()[0]

    c.execute('''INSERT OR REPLACE INTO Track (title, album_id, genre_id, len, rating, count) VALUES
    (?, ?, ?, ?, ?, ?)''', (name, album_id, genre_id, length, rating, count,))

    conn.commit()


# https://www.coursera.org/learn/python-databases/discussions/weeks/3/threads/ZxDLX0aAStGQy19GgBrRiQ/replies/4ZpK5jejQvaaSuY3o8L2nQ
