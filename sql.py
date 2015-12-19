# -*- coding: utf-8 -*-

import sqlite3

with sqlite3.connect("sample.db") as connection:
    c = connection.cursor()
    c.execute("DROP TABLE posts")
    c.execute("CREATE TABLE posts(title TEXT, description TEXT)")
    c.execute('INSERT INTO posts VALUES("Awesome!", "Best recipe ever.")')
    c.execute('INSERT INTO posts VALUES("Loved it!", "Finger licking chicken.")')
