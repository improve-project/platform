# Developer One-liners
Note: Examples are for Ubuntu(14.04) Apache HTTP Server(2.4) and MySQL

# Prerequisites
    sudo apt-get update &&
    sudo apt-get upgrade

    sudo apt-get -y install python-dev &&
    sudo apt-get -y install python-pip &&
    sudo apt-get -y install libmysqlclient-dev &&
    sudo apt-get -y install python-numpy &&
    sudo apt-get -y install python-matplotlib

    sudo pip install MySQL-python &&
    sudo pip install Flask &&
    sudo pip install SQLAlchemy

# Data Storage - MySQL
## Database installation
    sudo apt-get install mysql-server
    sudo mysql_secure_installation

## Database initialization
    mysql -u USERNAME -p < ./doc/database/db_init.sql

### Users for newly created databases
In MySQL shell

    CREATE USER 'newuser'@'localhost' IDENTIFIED BY 'password';
    GRANT SELECT, INSERT, UPDATE, DELETE ON [database name].* TO '[username]'@'localhost';

## Configure database connections
    nano ./databases.conf

## Configure database engines if needed
    nano ./database_handler.py

# Deployment
## Development mode
[ Flask - Quickstart ](http://flask.pocoo.org/docs/0.10/quickstart/#a-minimal-application)


### Clone platform source
    git clone https://github.com/improve-project/platform.git ./platform/

### Configure platform host and port
Edit `app.run(host="0.0.0.0", port=8080, threaded=False)` section from file `./__init__.py`

- Defaults
    - `host="0.0.0.0"`
    - `port=8080`
- To restrict access only for localhost set `host="127.0.0.1"`

### Start platform
In project root

    python __init__.py

## Production mode

### Clone platform source
    git clone https://github.com/improve-project/platform.git /var/www/platform/platform/

### Apache HTTP Server
[ Apache HTTP Server Project ](http://httpd.apache.org/)

    sudo apt-get install apache2

#### mod_wsgi
[ mod_wsgi Documentation ](https://modwsgi.readthedocs.org)

    sudo apt-get install libapache2-mod-wsgi python-dev
    sudo a2enmod wsgi

#### .wsgi file
Create new .wsgi file

    sudo nano /var/www/platform/platform.wsgi

Add following lines to file

    #!/usr/bin/python
    import sys
    import logging
    logging.basicConfig(stream=sys.stderr)
    sys.path.insert(0,"/var/www/platform/")
    from platform import app as application

#### Virtual Host
Create new Virtual Host

    sudo nano /etc/apache2/sites-available/platform.conf

Add following lines to file

    <VirtualHost *:8080>
        KeepAlive Off

        LogLevel debug
        ErrorLog ${APACHE_LOG_DIR}/platform_error.log
        CustomLog ${APACHE_LOG_DIR}/platform_access.log vhost_combined

        WSGIDaemonProcess platform user=www-data group=www-data processes=5 threads=1
        WSGIScriptAlias / /var/www/platform/platform.wsgi

        <Directory /var/www/platform/platform/>
            WSGIScriptReloading On
            WSGIProcessGroup platform
            WSGIApplicationGroup %{GLOBAL}
            Options Indexes FollowSymLinks
            AllowOverride None
            Require all granted
        </Directory>
    </VirtualHost>

To enable created Virtual Host

    sudo a2ensite platform

#### Restart Apache
    sudo service apache2 restart
