# Meta-Search, a web application powered by Django.

## Live DEMO:
  http://zeyang.alwaysdata.net

## Main features:
- Aggregated and non-aggregated search mode
- Client-side and server-side validation
- Query pre-processing
- Boolean operator support
- Optional cluster feature
  
## Installation:

1. Make sure the following software are installed:
    - Apache httpd 2.2.2x (*not* required if you'd like to use Django's own server)
    - Python 2.7.x
    - Django 1.5.x

2. Install `requests` module for Python, please refer http://docs.python-requests.org/en/latest/user/install/#install.

3. Install `mod_wsgi` module *only if* you are using Apache to deploy this application, please refer https://code.google.com/p/modwsgi/wiki/DownloadTheSoftware?tm=2.

4. Unzip "metasearch" folder into whichever folder you want to deploy this application.

5. Edit `settings.py` in `/mysite/` folder,
    - Change the path in `STATICFILES_DIRS` setting into `your_path/metasearch/static` where "your_path" is the folder into which you extract the "metasearch" folder;
    - Change the path in `TEMPLATE_DIRS` setting into `your_path/metasearch/templates` where "your_path" is the folder into which you extract the "metasearch" folder.

6. (Note: This step is *only* required if you are deploying this application using Apache rather than Django's server.) Edit `httpd.conf` in `your_apache_path/conf/` folder where "your_apache_path" is the folder your Apache is installed, then append the following lines at the end of the file:

    ```
    #change the path into your actual path of mod_wsgi.so
    LoadModule wsgi_module /your_apache_path/modules/mod_wsgi.so

    #change the path into your actual path of /static/
    Alias /static/ your_path/metasearch/static/

    #change the path into your actual path of /static/
    <Directory your_path/metasearch/static/>
    Order deny,allow
    Allow from all
    </Directory>
    
    #change the path into your actual path of wsgi.py
    WSGIScriptAlias / your_path/metasearch/mysite/wsgi.py

    #change the path into your actual path of Project
    WSGIPythonPath your_path/metasearch

    #change the path into your actual path of mysite
    <Directory your_path/metasearch/mysite>
    <Files wsgi.py>
    Order deny,allow
    Allow from all
    </Files>
    </Directory>
    ```
    
7. Launch Apache or your Django server, then open the URL on which your server is hosting in any browser.
  
## Contact:
Zeyang Lin
zeyanglin2013@gmail.com
