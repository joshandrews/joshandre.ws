#!/usr/bin/env python

import web
import datetime
import re
import config
import random
import string
import hashlib

con = config.Config()
cache = True

def get_posts():
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    return db.select('entries', order='id DESC')

def get_published_posts():
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    return db.select('entries', where='published=1', order='id DESC')

def get_unpublished_posts():
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    return db.select('entries', where='published=0', order='id DESC')

def get_post(id):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    try:
        return db.select('entries', where='id=$id', vars=locals())[0]
    except IndexError:
        return None

def new_post(title, text, published):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    dt = datetime.datetime.utcnow()
    return db.insert('entries', title=re.sub('<[^<]+?>', '', title), content=text, posted_on=dt, published=published)

def del_post(id):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    db.delete('entries', where="id=$id", vars=locals())

def update_post(id, title, text, published):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    db.update('entries', where="id=$id", vars=locals(),
        title=re.sub('<[^<]+?>', '', title), content=text, published=published)

def update_post_body(id, text):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    db.update('entries', where="id=$id", vars=locals(), content=text)

def update_post_title(id, title):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    db.update('entries', where="id=$id", vars=locals(), title=re.sub('<[^<]+?>', '', title))

def generateUser(username, password, email):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    slt = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(20))
    pswd = hashlib.sha1(slt+password).hexdigest()
    return db.insert('users', user=username, passwd=pswd, email=email, privilege=2, salt=slt)

def get_user():
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    return db.select('users', where='id=1', vars=locals())

def update_user(username, password, email):
    db = web.database(dbn='mysql', db=con.ConfigSectionMap("MySQL")["database"], user=con.ConfigSectionMap("MySQL")["username"], pw=con.ConfigSectionMap("MySQL")["password"])
    db.update('users', where="id=1", vars=locals(), user=username, passwd=password, email=email)
