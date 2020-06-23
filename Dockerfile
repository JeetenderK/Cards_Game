FROM ubuntu
LABEL maintainer="jacktan@gmail.com"
RUN apt-get update
RUN apt-get -y install apache2
RUN apt-get -y install python3-pip
RUN apt-get -y install libapache2-mod-wsgi-py3
RUN mkdir django
ADD Cards_Game/ /home/ubuntu/django/
ADD 000-default.conf /etc/apache2/sites-available/000-default.conf
RUN pip -y install django
RUN python manage.py collectstatic
RUN nohup python manage.py runserver 0.0.0.0:8000
ENTRYPOINT apachectl -D FOREGROUND
ENV name Django