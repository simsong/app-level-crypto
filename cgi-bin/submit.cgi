#!/usr/bin/env python3
# coding=UTF-8
#
# File change detector

HEAD="""
   <title>Encrypted Survey Demonstration</title>
   <script src="jquery-3.1.1.min.js"></script>
"""

CONFIG='/var/www/html/demo/config.ini'

if __name__=="__main__":
   import argparse
   import urllib
   import cgi
   import cgitb
   import json
   import keyutil
   import dbutil
   from Crypto.Cipher import PKCS1_OAEP
   from Crypto.PublicKey import RSA
   from Crypto.Hash import SHA256

   cgitb.enable()

   # with open("/tmp/r","w") as f:
   #     f.write("Hello world")

   parser = argparse.ArgumentParser("create/test keys")
   parser.add_argument('--debug',action='store_true',help='for debugging')
   args = parser.parse_args()

   # Fetch http request information
   form = cgi.FieldStorage()

   # Fetch rsa private key from key store
   keydict = keyutil.read_keydict(CONFIG)
   priv    = keyutil.dict_to_priv(keydict)

   # Decrypt http request information
   # Use RSA_OAEP SHA256 to decrypt
   h256   = SHA256.new()
   impl   = RSA.RSAImplementation(use_fast_math=False)
   prikey = RSA.construct((priv['n'], priv['e'], priv['d']))
   cipher = PKCS1_OAEP.new(prikey, h256)
   
   firstname = cipher.decrypt(keyutil.base64_to_uchr(form['firstnameEncrypted'].value))
   age       = cipher.decrypt(keyutil.base64_to_uchr(form['ageEncrypted'].value))

   # Connect to mysql database
   conn = dbutil.db_connect()

   # Make data safe to insert
   firstnameEncrypted = conn.escape_string(urllib.parse.unquote(form['firstnameEncrypted'].value))
   ageEncrypted       = conn.escape_string(urllib.parse.unquote(form['ageEncrypted'].value))

   # Peform database insert
   c = conn.cursor()
   c.execute("insert into response (firstname, age, firstnameEncrypted, ageEncrypted) values (%s, %s, %s, %s)",(firstname, age, firstnameEncrypted, ageEncrypted))
   c.execute("commit")

   # Return results back to client browser
   print("Content-Type: text/html")
   print()
   print("<p>")
   print("Your survey submission is recorded.", firstname, age)
   print("</p>")

