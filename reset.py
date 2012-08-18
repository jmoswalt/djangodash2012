from os import system

system('python manage.py reset gmail --noinput')
system('python manage.py syncdb --noinput')