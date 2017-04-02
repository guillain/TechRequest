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
git clone https://github.com/guillain/digitalDerogation.git
```
### Create additionnal folders
```bash
cd digitalDerogation
mkdir log downloads uploads
```
### Configure and set apache configuration
* For unsecure http (80)
```bash
cp conf/digitalDerogation_apache.conf.default conf/digitalDerogation_apache.conf
vi conf/digitalDerogation_apache.conf
ln -s /var/www/digitalDerogation/conf/digitalDerogation_apache.conf /etc/apache2/conf-enabled/digitalDerogation_apache.conf
```
* For secure http (443)
```bash
cp conf/digitalDerogation_apache-secure.conf.default conf/digitalDerogation_apache_secure.conf
vi conf/digitalDerogation_apache-secure.conf
ln -s /var/www/digitalDerogation/conf/digitalDerogation_apache-secure.conf /etc/apache2/conf-enabled/digitalDerogation_apache-secure.conf
```
### Configure the database
```bash
mysqladmin create digitalDerogation -utoto -p
mysql digitalDerogation -utoto -p < conf/mysql.sql
mysql digitalDerogation -utoto -p < conf/mysql_data.sql (add users can be useful...)
```
### Configure the Cisco Spark application
Remember to have or create an access toekn for Cisco Spark
* [Cisco Spark](http://developper.ciscospark.com) client ID and secret

### Complete setting file
```bash
cp conf/settings.cfg.default conf/settings.cfg
vi conf/settings.cfg
```

