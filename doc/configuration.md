# Configuration
In the root folder you'll find a conf folder that contains the configurations files need for:
* settings.cfg: application configuration
* TechRequest_apache.conf
* TechRequest_apache-secure.conf
* mysql.sql
* mysql_data.sql

## settings.cfg
This file contains the configuration for the application like:
* url
* path
* Spark account
* MySQL access
* upload and download folders
* global constantes

## TechRequest_apache.conf & TechRequest_apache-secure.conf
These files are provided for Apache WSGI integration for unsecure and secure mode.
Thanks to remember to add your certificates in secure part.... ;)
On my side I used symbolic link in the apache conf folder... easy to maintain and switch ;)

## mysql.sql & mysql_data.sql
Two files to split structure and data.
As you understand structure is in mysql.sql file when data are in the second.
To initialize your environement thanks to remember to adapt at least one admin user in the data file before injection.

