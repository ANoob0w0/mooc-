#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os,fnmatch,re
for root, dirs, files in os.walk('D:\\Works\\HelpDoc\\Unity', topdown=False):
    for name in files:
        if fnmatch.fnmatch(name,"*.html"):
            filepath = os.path.join(root, name)
            print(filepath)
            file = open(filepath, "r", encoding='utf-8')
            content = file.read()
            content = re.sub("""<script>\(function\(w,d,s,l,i\)\{w\[l\]=w\[l\]\|\|\[\];w\[l\]\.push\(\{'gtm\.start':
      new Date\(\)\.getTime\(\),event:'gtm\.js'\}\);var f=d\.getElementsByTagName\(s\)\[0\],
      j=d\.createElement\(s\),dl=l!='dataLayer'\?'&l='\+l:'';j\.async=true;j\.src=
      '\/\/www\.googletagmanager\.com\/gtm\.js\?id='\+i\+dl;f\.parentNode\.insertBefore\(j,f\);
      \}\)\(window,document,'script','dataLayer','GTM-5V25JL6'\);
    <\/script>""", '', content,flags=0)
            content = re.sub('''<link href="https:\/\/fonts\.googleapis\.com\/css\?family=Roboto&amp;display=swap" rel="stylesheet">''', '', content,flags=0)
            content = re.sub('''<noscript><iframe src="\/\/www\.googletagmanager\.com\/ns\.html\?id=GTM-5V25JL6" height="0" width="0" style="display:none;visibility:hidden"><\/iframe><\/noscript>''', '', content,flags=0)
            content = re.sub('''<link href="https:\/\/fonts\.googleapis\.com\/css\?family=Roboto&amp;display=swap" rel="stylesheet" \/>''', '', content,flags=0)
            file.close()
            file = open(filepath, "w", encoding='utf-8')
            file.write(content)
            file.close()

print('finish')