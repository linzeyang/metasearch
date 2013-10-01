Meta-Search, a web application powered by Django.

#######################################

Main features:
- Query preprocessing
- Boolean operator support
- Client-side and server-side validation
- Aggregated and non-aggregated search mode
- Simple clustering feature

#######################################
Installation:

1. Make sure the following software are installed:
    -Apache httpd 2.2.22 (Apache is not required if you like to use Django's own server)
    -Python 2.7.x
    -Django 1.5.x

2. Install "requests" module for Python, please refer http://docs.python-requests.org/en/latest/user/install/#install.

3. Install "mod\_wsgi" module only if you are using Apache to deploy this application, please refer https://code.google.com/p/modwsgi/wiki/DownloadTheSoftware?tm=2 for download.

4. Unzip "metasearch" folder as well as all its contents into whichever folder you want to deploy this application.

5. Edit "settings.py" in '/mysite/',
    -change the path '/home/zeyang/repo/metasearch/static' in 'STATICFILES\_DIRS' setting into 'your\_path/metasearch/static' where 'your_path' is the folder into which you extract the 'metasearch' folder;
    -change the path "/home/zeyang/repo/metasearch/templates" in 'TEMPLATE\_DIRS' setting into 'your\_path/Project/templates' where 'your_path' is the folder into which you extract the 'metasearch' folder.

6. (Note: This step is only required if you are deploying this application using Apache rather than Django's server.) Edit "httpd.conf" in 'your\_apache\_path/conf/' folder where 'your\_apache\_path' is the folder your Apache is installed, then append the following lines at the end of the file:

    ######################################################
    LoadModule wsgi\_module /usr/local/apache2/modules/mod\_wsgi.so #change the path into your actual path of mod_wsgi.so

    Alias /static/ /home/zeyang/repo/metasearch/static/ #change the path into your actual path of /static/

    <Directory /home/zeyang/repo/metasearch/static/> #change the path into your actual path of /static/
    Order deny,allow
    Allow from all
    </Directory>

    WSGIScriptAlias / /home/zeyang/repo/metasearch/mysite/wsgi.py #change the path into your actual path of wsgi.py
    WSGIPythonPath /home/zeyang/repo/metasearch #change the path into your actual path of Project

    <Directory /home/zeyang/repo/metasearch/mysite> #change the path into your actual path of mysite
    <Files wsgi.py>
    Order deny,allow
    Allow from all
    </Files>
    </Directory>
    ########################################################
    
7. Launch Apache or your Django server, then enter the URL of the server in any browser.

#######################################

Contact:
Zeyang Lin
zeyanglin2013@gmail.com
