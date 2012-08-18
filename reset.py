from os import system

system('python manage.py reset oldmail --noinput')
system('python manage.py syncdb --noinput')