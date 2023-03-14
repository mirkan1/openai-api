# I need to rewrite for aws connection because pythonanywhere free does not cover mongo db since it is not a http but in allowlist, see below link for more info
# https://www.pythonanywhere.com/whitelist/

import os
import mysql.connector
from sys import platform
import time
from dotenv import load_dotenv
load_dotenv()

HOST = os.environ.get("HOST")
USER = os.environ.get("USER")
PASSWORD = os.environ.get("PASSWORD")
PORT = os.environ.get("PORT")

def get_db(database):
  db = mysql.connector.connect(
    host=HOST,
    user=USER,
    password=PASSWORD,
    port=PORT,
    database=database,
  )
  return db
