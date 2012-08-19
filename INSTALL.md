# Install OldMail

These instructions are for a Mac, so adjust for your dev environment. 

You will need Python 2.6 or 2.7 to run OldMail. To check the version type 'python' in Terminal.

## Set up Dev Environment
---
Oldmail is designed to use virtualenv with virtualenvwrapper to isolate the application and avoid package conflicts. From Terminal:

### Install virtualenv

    sudo pip install virtualenv
    sudo pip install virtualenvwrapper

    
### Edit Environment Variables
Edit your .bashrc (or .bash_profile on a Mac) with the text editor of your choice.

    nano ~/.bash_profile
    
And add the following lines to your .bashrc file.

    export WORKON_HOME=$HOME/.virtualenv
    source /usr/local/bin/virtualenvwrapper.sh
    export PIP_VIRTUALENV_BASE=$WORKON_HOME
    export PIP_RESPECT_VIRTUALENV=true`
    
Restart your shell by closing and opening it, or in terminal type:

    source ~/.bash_profile

### Configure Virtual Environment
Make a virtualenv called `oldmail` excluding site packages for a clean install

    mkvirtualenv --no-site-packages oldmail

Activate the virtual environment

    workon oldmail

Navigate to where you want to create the project locally. For example:

    cd ~/Code/

Verify prompt shows the virtual environment in () and your PWD (Present Working Dir)

    (oldmail)LOCAL:~/Code/

### Pull Oldmail code
Clone project. This will create the oldmail directory in you present working directory

    git clone git@github.com:jmoswalt/djangodash2012.git oldmail

### Navigate into the new directory:

    cd oldmail

### Install dependencies. 
You may want to look at the requirements.txt file first

    pip install -r requirements.txt

### Create Database and Tables
Download the [Postgres App](http://postgresapp.com) and follow instructions to get installed if you do not already have a Postgres server running.

From the command line in the root of your project (and in your `oldmail` virtualenv of course) run:

    >> psql -h localhost
    >> CREATE DATATBASE oldmail;
    >> \q
    >> python reset.py

The last command will create the tables for you, but not create a super user yet.


### Test Your Development Server

Now you can test your site by running the site locally. From terminal run:

    python manage.py runserver 0:8000

In your web browser of choice, navigate to your site at one of these URLs:

    http://127.0.0.1:8000

