"""
Python 3 script to build a webpage of avatars from GitHub mostly followed profiles or users.
"""

from urllib.request import urlretrieve
from calendar import timegm
import json
import time
import os
import requests


# debug / change run time
lastrun = int(time.time()) - os.path.getmtime("./site/index.html")
print(lastrun)

# run it
if lastrun < 73000:
    gsearch = 'https://api.github.com/search/users?q=followers:1..10000000&per_page=100'
    searches = [gsearch, '%s%s' % (gsearch, '&page=2')]
    loads = []
    logins = []
    for x in searches:
        page = requests.get(x)
        loads.append(json.loads(page.content))

    #
    page = """<!DOCTYPE html>
<html>
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
        <title>Top Github Faces</title>
        <!-- Latest compiled and minified CSS -->
        <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
        <style>
            .container {max-width: 1900px;}
            .row {float: left;}
            body {line-height: 0;}
            col-md-4 {width: 374px; height: 374px;}
            div.row {width: 374px; height: 374px;}
            img {width: 374px; height: 374px;}
            #flagcounter {width: auto; height: auto; position: fixed; bottom: 0px; left: 0px; margin-top: 65px; }
        </style>
         <!-- Global Site Tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-106852135-1"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments)};
            gtag('js', new Date());        
            gtag('config', 'UA-106852135-1');
        </script>
    </head>
    <body>
        <div class="container">"""
    for i, x in enumerate(loads):
        for j, person in enumerate(x['items']):
            k = i * 100 + j
            print(k, person)
            logins.append(person['login'])

            # fix ?? for deleting old avatars that are no longer top 200.
            # wait until we have 201 or more avatars to test code.
            try:
                localtime = os.path.getmtime("./site/images/faces/%s.png" % person['login'])
            except FileNotFoundError:
                localtime = 0

            with open(('./temp/%s.txt' % person['login']), 'w+') as f:
                os.system("curl --silent --head %s | awk '/^Last-Modified/{print $0}' | sed 's/^Last-Modified: //' > %s" % (person['avatar_url'], f.name))
                first_line = f.readline().rstrip()

                print(first_line)
                print(time.strptime(first_line, "%a, %d %b %Y %H:%M:%S GMT"))
                print(timegm(time.strptime(first_line, "%a, %d %b %Y %H:%M:%S GMT")))

                remotetime = timegm(time.strptime(first_line, "%a, %d %b %Y %H:%M:%S GMT"))

                # only download users avatar if its newer than the current local one.
                if localtime < remotetime:
                    print('remote newer')
                    urlretrieve(person['avatar_url'], "./site/images/faces/%s.png" % person['login'])
                else:
                    print('local newer')

            page += """
            <div class="row">
                <div class="col-md-4">
                    <div class="thumbnail">
                        <a href="{profile}" target="_blank">
                            <img src="{filename}" alt="{user}" title="{user}">
                        </a>
                    </div>
                </div>      
            </div>""".format(profile=person['html_url'], filename="./images/faces/%s.png" % person['login'],
                             user=person['login'])

    page += """
            <a href="https://info.flagcounter.com/sesT">
                <img id="flagcounter" alt="Flag Counter" 
                     src="https://s11.flagcounter.com/count2/sesT/bg_FFFFFF/txt_000000/border_CCCCCC/columns_3/maxflags_100/viewers_0/labels_0/pageviews_0/flags_0/percent_0/">
            </a>
        </div>       
        <!-- Latest compiled and minified JavaScript -->
        <script src="bootstrap/js/jquery.min.js"></script>
        <script src="bootstrap/js/popper.min.js"></script> 
        <script src="bootstrap/js/bootstrap.min.js"></script>    
    </body>
</html>"""

    target = open('site/index.html', 'w')
    target.write(page)
    target.close()

    #
    print(logins)

else:
    print("wait")
