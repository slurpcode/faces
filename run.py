"""
Python 3 script to build a web page of GitHub avatars from users with the most followers.
"""

from urllib.request import urlretrieve
from calendar import timegm
import json
import time
import os
import requests


# debug / change run time
last_run = int(time.time()) - os.path.getmtime("./site/index.html")
print(last_run)


def run(last_run_time):
    """
    :param last_run_time:
    Function to build the web page of avatars.
    """
    if last_run_time < 73000:
        user_search = 'https://api.github.com/search/users?q=followers:1..10000000&per_page=100'
        user_searches = [user_search, '%s%s' % (user_search, '&page=2')]
        loads = []
        user_logins = []
        for api_search in user_searches:
            page = requests.get(api_search)
            loads.append(json.loads(page.content))

        # HTML page header
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
        for i, each_json in enumerate(loads):
            for j, person in enumerate(each_json['items']):
                k = i * 100 + j
                print(k, person)
                user_logins.append(person['login'])

                # fix ?? for deleting old avatars that are no longer top 200.
                # wait until we have 201 or more avatars to test code.
                try:
                    localtime = os.path.getmtime("./site/images/faces/%s.png" % person['login'])
                except FileNotFoundError:
                    localtime = 0

                with open(('./temp/%s.txt' % person['login']), 'w+') as fname:
                    curl_string = "curl --silent --head %s | awk '/^Last-Modified/{print $0}'"
                    curl_string += " | sed 's/^Last-Modified: //' > %s"
                    os.system(curl_string % (person['avatar_url'], fname.name))
                    first_line = fname.readline().rstrip()

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

        # HTML page footer
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
        print(user_logins)

    else:
        print("wait")


run(last_run)
