# RESTful_django_bears
This application focuses on creating a RESTful version of the previous polar bears in django with forms repository so that we can add various front ends to consume JSON data. As before, this is an example of how you might do a RESTful application with Django.

The goal of this session is to show how to run an application that serves both the HTML as before, plus, the JSON that can be consumed by another application.

Start with the basics, pull down the repo and then set up your python envivonment and ensure Django is ready for use. 

        pyenv local 3.10.7 # this sets the local version of python to 3.10.7
        python3 -m venv .venv # this creates the virtual environment for you
        source .venv/bin/activate # this activates the virtual environment
        pip install --upgrade pip [ this is optional]  # this installs pip, and upgrades it if required.
        pip install django
        python3 manage.py migrate # to create the database and configure other parts of django
        python3 manage.py parse_csv # to load the csv data into the database

We'll use the Django REST framework https://www.django-rest-framework.org/ to supply the JSON serialisations/deserialisations and other hooks that we'll need in our application. As we're aiming to mix the JSON with the HTML, this shows one path through the various options of the framework. Go look at other parts of their tutorial to see how to create a version that serves only JSON too, if that is what you need.

We can install it with this command:

        pip install djangorestframework

This enables us to do a number of things. First, we can build serialisers that map to our models.



