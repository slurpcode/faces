"""
Python 3 script to build a HTML5 web page of GitHub avatars from users with the most followers.

Uses urllib and the requests library.
"""

from urllib.request import urlretrieve
from calendar import timegm
import time
import os
import requests


# debug / change run time
last_run = int(time.time()) - os.path.getmtime('./site/index.html')
print(last_run)


def page_header():
    """HTML5 page header."""
    return """<!DOCTYPE html>
<html lang="en-US">
    <head>
        <meta charset="UTF-8">
        <meta http-equiv="X-UA-Compatible" content="IE=edge">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <!-- The above 3 meta tags *must* come first in the head; any other head content must come *after* these tags -->
        <title>Top Github Faces</title>        
        <link rel="manifest" href="manifest.json">
        <meta name="theme-color" content="#FF0000">
        <link rel="stylesheet" href="bootstrap/css/bootstrap.min.css">
        <style>
            .row {float: left;}
            body {line-height: 0;}
            .col-md-4, div.row, img {width: 374px; height: 374px; padding: 0px;}
            #flagcounter {width: auto; height: auto; position: fixed; bottom: 0px; left: 0px; margin-top: 65px;}
            div#head {width: 100%; height: auto;}
            h1 {text-align: center; width: 100%;}
        </style>
        <!-- Global Site Tag (gtag.js) - Google Analytics -->
        <script async src="https://www.googletagmanager.com/gtag/js?id=UA-106852135-1"></script>
        <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments)};
            gtag('js', new Date());        
            gtag('config', 'UA-106852135-1');        
            if ('serviceWorker' in navigator) {
            
                navigator.serviceWorker.register('service-worker.js', {scope: './'}).then(function(registration) {
            
                }).catch(function(error) {
            
                });
            } else {
            // The current browser doesn't support service workers.
            }
        </script>
    </head>
    <body>
        <div class="container-fluid">
            <div class="row" id="head">
                <h1>Hacker Manifesto Faces</h1>
            </div>"""


def page_footer():
    """HTML5 page footer."""
    return """
            <a href="https://info.flagcounter.com/sesT" target="_blank" rel="noopener">
                <img id="flagcounter" alt="Flag Counter">
            </a>
            <script>
                if(navigator.onLine){
                    document.getElementById("flagcounter").src = "https://s11.flagcounter.com/count2/sesT/bg_FFFFFF/txt_000000/border_CCCCCC/columns_3/maxflags_100/viewers_0/labels_0/pageviews_0/flags_0/percent_0/";
                } else {
                    document.getElementById("flagcounter").src = "images/other/flagcounter.png";
                }
            </script>
        </div>
        <script src="bootstrap/js/jquery.min.js"></script>
        <script src="bootstrap/js/popper.min.js"></script> 
        <script src="bootstrap/js/bootstrap.min.js"></script>    
    </body>
</html>"""


def run(last_run_time):
    """Build the web page of avatars."""
    if last_run_time > 200:
        user_search = 'https://api.github.com/search/users?q=followers:1..10000000&per_page=100'
        user_searches = []
        for i in range(1, 4):
            user_searches.append('%s%s%s' % (user_search, '&page=', i))
        loads = []
        user_logins = []
        for api_search in user_searches:
            loads.append(requests.get(api_search).json())

        # HTML page header
        page = page_header()
        # loop over each json load
        for i, each_json in enumerate(loads):
            for j, person in enumerate(each_json['items']):
                k = i * 100 + j
                print(k, person)
                user_logins.append(person['login'])

                # fix ?? for deleting old avatars that are no longer top 300
                # wait until we have more avatars to try garbage collection
                try:
                    localtime = os.path.getmtime('./site/images/faces/%s.png' % person['login'])
                except FileNotFoundError:
                    localtime = 0

                with open(('./temp/%s.txt' % person['login']), 'w+') as fname:
                    curl_string = "curl --silent --head %s | awk '/^Last-Modified/{print $0}'"
                    curl_string += " | sed 's/^Last-Modified: //' > %s"
                    os.system(curl_string % (person['avatar_url'], fname.name))
                    first_line = fname.readline().rstrip()

                    print(first_line)
                    print(time.strptime(first_line, '%a, %d %b %Y %H:%M:%S GMT'))
                    print(timegm(time.strptime(first_line, '%a, %d %b %Y %H:%M:%S GMT')))

                    remotetime = timegm(time.strptime(first_line, '%a, %d %b %Y %H:%M:%S GMT'))

                    # only download users avatar if its newer than the current local one.
                    if localtime < remotetime:
                        print('remote newer')
                        urlretrieve(person['avatar_url'],
                                    './site/images/faces/%s.png' % person['login'])
                    else:
                        print('local newer')

                page += """
            <div class="row">
                <div class="col-md-4">
                    <div class="thumbnail">
                        <a href="{profile}" target="_blank" rel="noopener">
                            <img src="{filename}" alt="{user}" title="{user}">
                        </a>
                    </div>
                </div>      
            </div>""".format(profile=person['html_url'],
                             filename='./images/faces/%s.png' % person['login'],
                             user=person['login'])
        # retrieve the flag counter for offline use
        urlretrieve('https://s11.flagcounter.com/count2/sesT/bg_FFFFFF/txt_000000/border_CCCCCC/columns_3/maxflags_100/viewers_0/labels_0/pageviews_0/flags_0/percent_0/',
                    './site/images/other/flagcounter.png')
        # HTML page footer
        page += page_footer()
        # write page to file
        target = open('site/index.html', 'w')
        target.write(page)
        target.close()

        #
        print(user_logins)

    else:
        print("wait")


run(last_run)
