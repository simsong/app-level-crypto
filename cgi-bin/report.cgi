#!/usr/bin/env python3
# coding=UTF-8
#
# File change detector

HEAD="""
   <title>Encrypted Survey Demonstration</title>
   <script src="jquery-3.1.1.min.js"></script>
   <script src="encrypt.js"></script>
"""

FORM="""
   <form onsubmit="sendEncrypted(event, rsajwk, 'survey.cgi')">
   First name:   <input type='text' id='firstname' name='firstname'/><br/>
   Age: <input type='text' id='age' name='age'/><br/>
   <!--button type='button' onclick="alert('Hello World!')">Encrypt and Submit!</button><br/-->
   <input type='submit' value='Encrypt and Submit!'>
   </form>
   <div id='status'></div>
"""

CONFIG='/var/www/html/demo/config.ini'

import keyutil

webkey = keyutil.dict_to_jwk(keyutil.read_keydict(CONFIG))

if __name__=="__main__":
   import argparse
   import cgi
   import cgitb
   import keyutil
   cgitb.enable()


   parser = argparse.ArgumentParser("create/test keys")
   parser.add_argument('--debug',action='store_true',help='for debugging')
   args = parser.parse_args()

   print("Content-Type: text/html")
   print()
   print("<html>")
   print("<head>")
   print(HEAD)
   print("<script>")
   print("var rsajwk = ", webkey)
   print("</script>")
   print("</head>")
   print("<body>")
   print("<H1>Survey</H1>")
   print("<p>This is a secure form.</p>")
   print(FORM)
   print("<br/><hr/>")
   print("<p>Here is the public key:</p>")
   print("<p style='font-family:monospace; width: 300px; word-wrap: break-word'>")
   print(webkey)
   print("</p>")
   print("</body>")
   print("</html>")
