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
 For real project [Docker volumes](https://docs.docker.com/engine/admin/volumes/volumes/) would be a better choice.
 Other _interesting_ choices have been made in this project. 
  
 ### Docker
 Docker is used to make creation and deployment of the test or production environment
  as painless and repeatable as possible.
 
 ### Nginx
 Nginx is used as the high performance web server and is connected to Django using 
  uWSGI.  Nginx serves static files without resorting to calling the Django code.
  
 ### AWS
  The docker-compose-AWS.yml file is AWS compatible and serves as the task definition behind http://randalmoore.me 
  (details below)
   
## Usage
Quickstart outline of commands made at project root.
Poking around and reading documentation for the various technologies strongly encouraged.
 
### Development (Django + sqlite.  Does not use Docker, Nginx, Postgres)
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

Now that you know the Docker images work together you have a better shot of things working
when deploying to AWS.  This is the outline to deploy to AWS:
1. Create AWS account.
2. Install AWS tools locally
  * (uses pip, you can install in the virtualenv) http://docs.aws.amazon.com/cli/latest/userguide/installing.html
  * (installs in /usr/local/src) http://docs.aws.amazon.com/AmazonECS/latest/developerguide/ECS_CLI_installation.html
3. Create a cluster by browsing to "EC2 Container Service" (not EC2) in AWS management console.  This can probably
also be done via the ecs-cli command line.  Make sure your selections correspond to free tier options if you don't
want to spend money (my site is running on a single t2.micro instance).
4. Push your image to the repository following the AWS tutorial.
  * http://docs.aws.amazon.com/AmazonECR/latest/userguide/docker-push-ecr-image.html
5. Update docker-compose-AWS.yml in this project to reference the image you pushed (your specific image name / tag).
6. Use ecs-cli to issue the equivalent of docker-compose command but against your AWS 
cluster.  This creates a new task in your cluster with 2 containers, one each for the
 website and db images.
```bash
ecs-cli compose --file docker-compose-AWS.yml --verbose up
```
7. If all goes well you should see something that indicates both containers reach RUNNING status ("lastStatus=RUNNING")
> INFO[0007] Started container...                          container=".../web" desiredStatus=RUNNING lastStatus=RUNNING taskDefinition="ecscompose-..."
> 
>INFO[0007] Started container...                          container=".../db" desiredStatus=RUNNING lastStatus=RUNNING taskDefinition="ecscompose-..."
8. Access your site on AWS using the EC2 instance public DNS name that is hosting your
cluster (click around on the AWS management site to find this).
  * (Optional) You can use AWS Elastic IP to link your site to a registered DNS entry using a "type A" record.

How to SSH into the instance and view logs etc:
1. Open AWS EC2 (not EC2 Container Service) management in your browser and click on
the instance hosting your site.
2. Click on the security group link for your instance.
3. Click on the Inbound tab of the security group, edit, and add port 22.
4. Follow the AWS docs for how to SSH into the instance (use the same public DNS name as 
you used to view the site in the browser)
  * http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/AccessingInstancesLinux.html
5. After SSHing into the EC2 instance you will have landed in an Amazon virtual machine 
 image which is running Docker with your two containers plus a third amazon-ecs-agent 
 container.
6. Find the container id running your website image
```bash
docker ps
```
7. Open a bash shell into the container
```bash
docker exec -ti <website container id> bash
```
8. Now you can poke around in a minimal Ubuntu like environment [phusion/baseimage](https://github.com/phusion/baseimage-docker)
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