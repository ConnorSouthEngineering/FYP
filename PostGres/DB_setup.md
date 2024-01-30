<!--INTRODUCTION
The following file describes the required steps to setup the POSTGRESQL (PSQL) DB for the OVision Framework.
First PSQL must be installed. At the time of development PSQL Version 10 was used.
-->

<!--Install postgresql and start the service -->
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql.service

<!--Switch to the PSQL user, load PSQL and set password
    {password} needs to be replaced with the password you want -->
sudo -i -u postgres
PSQL
ALTER USER postgres WITH PASSWORD '{password}';

<!--New DB for OVision needs to be created -->
CREATE DATABSE ovision;
<!--Swith to ovision DB and create schema -->
\c ovision
CREATE SCHEMA vision_data;
CREATE SCHEMA site_data;
ctrl+z  <!--(to exit) -->
<!--Installation of pg_cron is needed to allow for scheduled execution of Stored Procedures
    installation instructions could be updated here: https://github.com/citusdata/pg_cron

    The following was used at time of writing
-->
sudo sh -c 'echo "deb http://apt.postgresql.org/pub/repos/apt $(lsb_release -cs)-pgdg main" > /etc/apt/sources.list.d/pgdg.list'
wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
sudo apt-get update
sudo apt-get install postgresql-10-cron

<!--pg_cron must be configured in PSQL configuration file
    postgresql.conf is normally found in /etc/postgresql/[version]/main
-->
cd [postgresql.conf location]
sudo gedit psotgresql.conf
<!--add pg_cron extension to configuration file-->
shared_preload_libraries = 'pg_cron'
<!--set pg_cron to the newly created ovision db-->
cron.database_name = 'ovision'
<!--restart psql-->
sudo systemctl restart postgresql
<!--to allow execution of cron functions by user account enter following-->
PSQL
\c test_db
GRANT USAGE ON SCHEMA cron TO postgres;


<!--DOCKER PSQL ACCESS-->
psql --username=[username] --dbname=[dbname] --password