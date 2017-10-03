#!/usr/bin/env python3
# coding=UTF-8
#
# File change detector

HEAD="""
    <title>Encrypted JSON Survey Demonstration</title>
    <script src="jquery-3.1.1.min.js"></script>
    <script src="encrypt_json.js"></script>
    <style>
        body {font-family: sans-serif }
        input { font-size: 18pt; border: 1px solid grey; border-radius: 3px}
        div#form {
            text-align: left;
            display: table-cell;
            padding: 9px;
            border: 1px solid black;
            border-radius: 5px;
        }
    </style>
"""

FORM="""
    <div id="form">
    <form onsubmit="sendEncrypted(event, rsajwk, 'submit_json.cgi')">
    <table style="font-size:18pt">
    <tr><td>First name</td><td><input type='text' id='firstname' name='firstname'/></td></tr>
    <tr><td>Age</td><td><input type='text' id='age' name='age'/></td></tr>
    </table>
    <input style="float: right; font-size: 14pt" type='submit' value='Encrypt and Submit!'>
    </form>
    </div>
    <div id="message" style="text-align: center; font-size: 18pt; font-weight: bold; margin-top: 20px"></div>
"""

import keyutil

webkey = keyutil.dict_to_jwk(keyutil.read_keydict(keyutil.CONFIG))

if __name__=="__main__":
   import argparse
   import cgi
   import cgitb
   import keyutil
   import textwrap
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
   print("var rsajwk = "+webkey+";")
   print("</script>")
   print("</head>")
   print("<body>")
   print("<center>")
   print("<H1>Survey</H1>")
   print("<p>This is a secure form.</p>")
   print(FORM)
   print("</center>")
   print("</body>")
   print("</html>")
