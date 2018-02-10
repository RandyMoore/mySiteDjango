# Dockerized Nginx-Django-Postgres AWS Deployable Stack
 
 Personal project to learn and experiment with these technologies.
 
 This is the source code and content behind [randalmoore.me](http://randalmoore.me)  
 
 ## Overview
 Basic personal website with blog.  Utilizes Django with Wagtail as a means to quickly 
  input and manage the blog content.  Various technologies and deployment techniques
  are used for the purpose of exploration and experimentation; not intended to be robust or for mission
  critical applications.
  
 ### Site Content
 The blog content is exported as a data fixture (.json format) and checked into version control here.
 Upon deployment the data is loaded into the database using Django migrations.
 This isn't recommended for real world projects - I wanted to separate content from technology.
 For a real project [Docker volumes](https://docs.docker.com/engine/admin/volumes/volumes/) would be a better choice.
 Other _interesting_ choices have been made in this project. 
  
 ### Docker
 Docker is used to make creation and deployment of the test or production environment
  as painless and repeatable as possible.
 
 ### Nginx
 Nginx is used as a high performance web server and is connected to Django using 
  uWSGI.  Nginx serves static files without resorting to calling the Django code.
  
 ### AWS
  The docker-compose-AWS.yml file is AWS compatible and serves as the task definition behind http://randalmoore.me 
  (details below)
   
## Usage
Quickstart outline of commands made at project root.
Poking around and reading documentation for the various technologies strongly encouraged.
 
### Development
Create a python virtual environment (here I use python3, default python2 also works)
```bash
virtualenv -p python3 .
```
Install dependencies
```bash
pip3 install -r config/requirements.txt
```
Create database schemas and populate data
```bash
python my_site_django/manage.py migrate
```
Run the Django dev server
```bash
python my_site_django/manage.py runserver
```
You should be able to access the site at [http://localhost:8000](http://localhost:8000) now.

### Adding or changing site content
Follow steps above for development then create a superuser 
```bash
python my_site_django/manage.py createsuperuser
```
Next login to the development server using your super user name and password at 
[http://localhost:8000/cms](http://localhost:8000/cms)

To make the changes permanent use Django's "dumpdata" command (the default options to dump data for all Django applications). 
Replace the contents of my_site_django/weblog/fixtures/initial_data.json with the output of this 
command.  
Test the loading of 
the data in the development environment by deleting the db.sqlite file and running the 
manage.py migrate command again. I had to delete some Wagtail model instances from the 
data, presumably they had already been included with previously applied core Wagtail 
migrations.
 
### Local Docker and AWS deployment
Obtain a secret for use by Django, for example from
http://www.miniwebtool.com/django-secret-key-generator/

Building the image without a key defined will result in deployment failure.

Before deploying to AWS you need to build the image (AWS doesn't support this for docker-compose yet).
Ensure Docker is running on your machine and then use it to build the image and run
the production environment locally.

```bash
docker build -t website . --build-arg django_secret_key='<Your secret key>'
```

This creates an image called "website" which is referenced by the docker-compose.yml
 file.  Then bring up the production environment locally.  Look at the output in the 
 terminal for any issues
```bash
docker-compose up
```
If all goes well you should be able to access the website at [http://localhost](http://localhost) 
(note the default http port 80 is used - Nginx is serving requests, not the Django dev server on port 8000).


### How to view webserver logs and poke around:
1. Find the container id running your website image
```bash
docker ps
```
2. Open a bash shell into the container
```bash
docker exec -ti <website container id> bash
```
3. Now you can poke around in a minimal Ubuntu like environment [phusion/baseimage](https://github.com/phusion/baseimage-docker)
For example
```bash
# Nginx errors
cat /var/log/nginx/error.log
# Web server access log
cat /var/log/nginx/access.log 
# uWSGI log (includes Django errors)
cat /var/log/uwsgi/uwsgi.log
# show running processes and resource usage
top
```