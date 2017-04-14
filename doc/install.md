# PreRequisites
* MySQL
* python (2.7)
* * Flask
* * MySQLdb

Configurations is provided for:
* Apache and WSGI server
* python/flask CLI (cf. run file)
But you can also get only the python with another web server, container...
So according to your choice thanks to install the necessary package

You must have also a Cisco Spark account and create application (all for free ;)
* [Cisco Spark](http://developper.ciscospark.com)

# Install

## Clone localy
```bash
git clone https://github.com/guillain/TechRequest.git
cd digitalException
```
### Install the Python requirements
```bash
pip install -r requirements.txt
```
### Create additionnal folders
```bash
cd TechRequest
mkdir log downloads uploads
```
### Configure and set apache configuration
If you use one dedicated alias on your web server for this specific web app, follow the explanation below (virtual host creation with default config file).
Else put the WSGI content of the default file in your virtual host definiton
* For unsecure http (80)
```bash
cp conf/TechRequest_apache.conf.default conf/TechRequest_apache.conf
vi conf/TechRequest_apache.conf
ln -s /var/www/TechRequest/conf/TechRequest_apache.conf /etc/apache2/conf-enabled/TechRequest_apache.conf
```
* For secure http (443)
```bash
cp conf/TechRequest_apache-secure.conf.default conf/TechRequest_apache_secure.conf
vi conf/TechRequest_apache-secure.conf
ln -s /var/www/TechRequest/conf/TechRequest_apache-secure.conf /etc/apache2/conf-enabled/TechRequest_apache-secure.conf
```
### Configure the database
```bash
mysqladmin create TechRequest -utoto -p
mysql TechRequest -utoto -p < conf/mysql.sql
mysql TechRequest -utoto -p < conf/mysql_data.sql (add users can be useful...)
```
### Configure the Cisco Spark application
Remember to have or create an access toekn for Cisco Spark
* [Cisco Spark](http://developper.ciscospark.com) client ID and secret

### Complete setting file
```bash
cp conf/settings.cfg.default conf/settings.cfg
vi conf/settings.cfg
```


## Fast & Furious method
```bash
yum install httpd
yum mysql-server mysql-client
yum install MySQL-python.x_
yum install mysql-server
yum install python-pip
pip install flask
pip install express
pip install config
pip install requests_toolbelt
```

