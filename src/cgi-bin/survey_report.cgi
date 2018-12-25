#!/usr/bin/env python3
# coding=UTF-8
#
# File change detector

HEAD="""
    <title>Encrypted Survey Demonstration</title>
    <script src="jquery-3.1.1.min.js"></script>
    <script src="survey_report.js"></script>
    <style>
        body {font-family: sans-serif }
        td { border: 1px solid grey; word-wrap:break-word; padding: 3px; }
        #td1 { max-width: 600px; }
        #td2 { max-width: 100px; }
        #td3 { max-width: 600px; }
        #td4 { max-width: 100px; }
        td#td1 { font-family: 'courier new' }
        td#td3 { font-family: 'courier new' }
    </style>
"""

REPORT="""
   <div id="response"></div>
"""

CONFIG='/var/www/html/demo/config.ini'

if __name__=="__main__":
    import cgi
    import cgitb
    import dbutil
    cgitb.enable()

    form = cgi.FieldStorage()

    # Answer ajax request
    if 'request' in form and form['request'].value=="fetch_results":
        print("Content-Type: text/html")
        print()

        conn = dbutil.db_connect()
        c = conn.cursor()
        c.execute("select firstnameEncrypted, firstname, ageEncrypted, age from response order by created desc limit 5")
        
        print('<table>');
        print('<tr><th id="td1">{:s}</th><th id="td2">{:s}</th><th id="td3">{:s}</th><th id="td4">{:s}</th></tr>'.format('firstnameEncrypted', 'firstname', 'ageEncrypted', 'age')) 
        for row in c.fetchall():
            print('<tr><td id="td1">{:s}</td><td id="td2">{:s}</td><td id="td3">{:s}</td><td id="td4">{:d}</td></tr>'.format(row[0], row[1], row[2], row[3])) 
        
        print('</table>');

    # Output start page
    else:
        print("Content-Type: text/html")
        print()
        print("<html>")
        print("<head>")
        print(HEAD)
        print("</head>")
        print("<body>")
        print("<center>")
        print("<H1>Report</H1>")
        print(REPORT)
        print("</center>")
        print("</body>")
        print("</html>")

