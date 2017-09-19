import json
import requests
from urllib.request import urlretrieve


page = requests.get('https://api.github.com/search/users?q=followers:1..10000000')
loads = json.loads(page.content)

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
        .container {max-width: 1500px;}      
        .row {float: left;}
        body {line-height: 0;}
        col-md-4 {width: 374px; height: 374px;}
        div.row {width: 374px; height: 374px;}
        img {width: 374px; height: 374px;}
    </style>
  </head>
  <body>
    <div class="container">"""

for i, person in enumerate(loads['items']):
    print(person)
    urlretrieve(person['avatar_url'], "./site/images/faces/local-filename%s.png" % i)

    page+="""<div class="row">
       <div class="col-md-4">
        <div class="thumbnail">
          <a href="{profile}" target="_blank">
            <img src="{filename}" alt="{user}">
          </a>
        </div>
      </div>      
    </div>
    """.format(profile=person['html_url'], filename="./images/faces/local-filename%s.png" % i, user=person['login'],)

page+="""
    </div>   
    <!-- Latest compiled and minified JavaScript -->
    <script src="bootstrap/js/bootstrap.min.js"></script>
    <script src="bootstrap/js/jquery.min.js"></script>
  </body>
</html>
"""

target = open('site/index.html', 'w')
target.write(page)
target.close()
