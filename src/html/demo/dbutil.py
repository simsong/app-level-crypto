#!/usr/bin/env python3
# coding=UTF-8
#
# File change detector

__version__='0.0.1'
import os.path,sys

import os,sys,re,collections
import MySQLdb
import datetime
from configparser import ConfigParser

CONFIG='/var/www/html/demo/config.ini'

# Replace this with an ORM?
schema = \
"""
CREATE DATABASE IF NOT EXISTS survey;
CREATE TABLE IF NOT EXISTS survey.response (
   rowid INTEGER AUTO_INCREMENT PRIMARY KEY, 
   created timestamp,
   firstnameEncrypted text,
   firstname text,
   ageEncrypted text,
   age integer);
"""

def db_connect():
    config = ConfigParser()
    config.read(CONFIG)
    conn = MySQLdb.connect(host=config['mysql']['host'], user=config['mysql']['user'], passwd=config['mysql']['pass'], db=config['mysql']['base'])
    return conn


def create_schema(conn):
    # If the schema doesn't exist, create it
    c = conn.cursor()
    for line in schema.split(";"):
        print(line,end="")
        c.execute(line)

def iso_now():
    return datetime.datetime.now().isoformat()[0:19]

if(__name__=="__main__"):
    import argparse
    parser = argparse.ArgumentParser(description='Compute file changes')
    parser.add_argument("--create", action="store_true",help="Create database")
    parser.add_argument("--list",   help="List transactions in database",action="store_true")

    args = parser.parse_args()

    if args.create:
        conn = db_connect()
        create_schema(conn)

    if args.list:
        conn = db_connect()
        c = conn.cursor()
        c.execute("select * from response")
        for row in c.fetchall():
            print(row)

