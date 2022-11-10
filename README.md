# RESTful_django_bears
This application focuses on creating a RESTful version of the previous polar bears in django with forms repository so that we can add various front ends to consume JSON data. As before, this is an example of how you might do a RESTful application with Django.

Most of this repository is a regular 'django app'. There is also a 'frontend' folder, which holds the javascript front end of this two part application. First, we build the backend with django. Second, we build the frontend javascript components.

The goal of this session is to show how to run an application that serves both the HTML as before, plus, the JSON that can be consumed by another application.

## Start with the backend
Start with the basics, pull down the repo and then set up your python envivonment and ensure Django is ready for use. 

        pyenv local 3.10.7 # this sets the local version of python to 3.10.7
        python3 -m venv .venv # this creates the virtual environment for you
        source .venv/bin/activate # this activates the virtual environment
        pip install --upgrade pip [ this is optional]  # this installs pip, and upgrades it if required.
        pip install django
        python3 manage.py migrate # to create the database and configure other parts of django
        python3 manage.py parse_csv # to load the csv data into the database

We'll use the Django REST framework https://www.django-rest-framework.org/ to supply the JSON serialisations/deserialisations and other hooks that we'll need in our application. As we're aiming to mix the JSON with the HTML, this shows one path through the various options of the framework. Go look at other parts of their tutorial to see how to create a version that serves only JSON too, if that is what you need. 

You can find much more detail about using the rest_framework in its tutorial pages, and in the API Guide. 

We can install it with this command:

        pip install djangorestframework

This enables us to do a number of things. First, we can build serialisers that map to our models.

## Modifying your configuration files

Open the polar_bears/settings.py file and add the relevant REST libraries for Django to the application. Add the line 'rest_framework', as shown below (don't forget the , at the end of the line). 

        INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'bears',
        'rest_framework',
    ]

Open the bears/urls.py file and add this line as an import:

        from rest_framework.urlpatterns import format_suffix_patterns

Next, add this line at the end of the file in order to map views to json output.

        urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])

With this in place we can now start to modify the bears application.

## Creating Serializers
We use serialisers to convert our models to/from JSON data. The rest_framework does this for us, but we need to tell it what to produce. We do this by adding a bears/serializers.py file next to the models.py file. You can add this code to the file:

        from django.contrib.auth.models import User, Group #common, but we don't need them
        from rest_framework import serializers
        from .models import Bear, Sighting

        class BearSerializer(serializers.HyperlinkedModelSerializer):
            class Meta:
                model = Bear
                fields = ['id','bearID', 'pTT_ID', 'capture_lat', 'capture_long', 'sex', 'age_class', 'ear_applied', 'created_date']

        class SightingSerializer(serializers.ModelSerializer):
            class Meta:
                model = Sighting
                fields = ['bear_id', 'deploy_id', 'recieved', 'latitude', 'longitude', 'temperature', 'created_date']

As you can see this is very similar to what you put into a form file, with the addition that we can include the autogenerated data such as 'id' and 'created_date'. This makes it easy to manipulate our models and the associted output.

The SightingSerialiser differs from the BearSerialiser in that it uses ModelSerialiser instead of HyperLinkedModelSerialiser. The BearSerialiser needs to link back to the url of each instance for the views. As we only show sightings on the bear_detail page, but not individually, we don't use the HyperLinkedModelSerializer. If you did have sighting_detail pages for each sighting, then you should do that. We don't, so they cause an error.

## Using the Serialisers in the Views
We want to be able to continue using the HTML template output, while also having the option for JSON output. This means we keep everything as close to the current views as possible. We can start by adding rest_framework, and our serializer.py file as imports to bears/views.py

        from django.utils import timezone
        from django.shortcuts import redirect, render, get_object_or_404
        from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
        from rest_framework.decorators import api_view, renderer_classes
        from rest_framework.response import Response
        from .models import Bear, Sighting
        from .forms import BearForm
        from .serializers import BearSerializer, SightingSerializer

Then we can use the serializers in the list and detail views. We'll start with the list view by adding the decorators and the if ... format=='html' part plus the JSON serialisation below that.

        @api_view(['GET']) # use this for function based views
        @renderer_classes([TemplateHTMLRenderer, JSONRenderer]) #return either html or json
        def bear_list(request, format=None):
            bears = Bear.objects.all()
            if request.accepted_renderer.format =='html': # check for HTML
                return render(request, 'bears/bear_list.html', {'bears' : bears})
            serializer = BearSerializer(bears, many=True) # return JSON if html not requested
            data = serializer.data
            return Response(data)

Notice that the serializer takes arguments for the object, and a flag that we are passing in multiple bear instances.

We can write something similar for the bear_detail method as well. The potentially messy part here is that we want to return one bear, and possibly many sightings. 

        @api_view(['GET'])
        @renderer_classes([TemplateHTMLRenderer, JSONRenderer])
        def bear_detail(request, id):
            bear = get_object_or_404(Bear, id=id)
            sightings = Sighting.objects.filter(bear_id=id)
            if request.accepted_renderer.format=='html':
                return render(request, 'bears/bear_detail.html', {'bear' : bear, 'sightings' : sightings})
            serializerBear = BearSerializer(bear, context={'request': request})
            serializerSighting = SightingSerializer(sightings, many=True, context={'request': request})
            bear_data = serializerBear.data
            sightings_data = serializerSighting.data
            data = [bear_data, sightings_data]
            return Response(data)

## Confirm it works smoothly
You can start Django in the usual manner with the command:

        python3 manage.py runserver

You can then open a terminal and use either curl if you're on linux or a MacOS. You can also use https://httpie.io/docs/cli/installation as an alternative if you prefer. In either case you can call the pages to test them with commands like:

        http://localhost:8000/
        http://localhost:8000/bear/5/

The first should return the list of all bears, while the second should give you the details for bear 5 (possibly deploy_id: 20446) and the associated sightings. Any error should appear in the terminal, plus the terminal showing the django output too.

## Now we need a front-end to consume the JSON
We can build a small Javascript front end to consume our JSON. In order to do this we need to modify our backend again, and to possibly put some basic development tooling in place. The basics of this are from a simple example showing you how to pull movie titles from Studio Ghibli https://www.taniarascia.com/how-to-connect-to-an-api-with-javascript/ 

First, add the Node Version Manager if you don't have that already. This will allow you to run a small http server hosting the Javascript frontend alongside Django running the backend. You can go to either https://github.com/nvm-sh/nvm or use https://nodejs.org/en/. 

Maybe, like me, you find that you use Node irregularly, so it's time to update things. You can do that from the terminal with this command:

        nvm install node --reinstall-packages-from=node

Second, with NVM in place, we can now add http-server https://www.npmjs.com/package/http-server to drive the frontend application that pulls JSON from our Django backend. You can install/launch it simply with the command:

        nvm http-server -c-1

I found that adding the -c-1 flags meant it stopped (made it less likely) that my browser would cache the html and js source files. Otherwise, I'm spending too long dumping the cache from the browser each time I make an edit of the html or js files.

http-server will start a service on a different port than Django, so this is fine, and you can then load your frontend application there.

### Add support for cross origin resource sharing (CORS)
We need another library to be added to our django backend so that we can call the JSON parts from another application server. We didn't experience this before as we were only calling the pages from our own server. We'll use https://pypi.org/project/django-cors-headers/ for this, which we install with the command:

        pip install django-cors-headers

Then modify the polar_bear/settings.py file as follows to finish configuration.

1. Edit the INSTALLED_APPS by adding this to the list:

        "corsheaders",

2. Add these these two items to the MIDDLEWARE section:

        MIDDLEWARE = [
            ...,
            "corsheaders.middleware.CorsMiddleware",
            "django.middleware.common.CommonMiddleware",
            ...,
        ]

3. Add allowed access for calls into the system. You can use a wildcard to allow anything, but it is safer to specify the specific locations that you expect as we do with this addition. You can add this below your middleware section:

        CORS_ALLOWED_ORIGINS = [
            "http://localhost:8080",
        ]

Now you can resart the server.

### Creating the index page
We want to have a basic html file to load the javascript content as JSON. We can do that like this. Create an index.html file in the 'frontend' folder with this content:

        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />

            <title>Bear App</title>
            <link href="css/style.css" rel="stylesheet" />
        </head>

        <body>
            <h1>Bear App</h1>
            <div id="root"></div>
            <script src="js/index.js"></script>
        </body>
        </html>

Next, add a 'frontend/css' folder with a styles.css file. That file can hold this code:

        body {
            background-color: white;
            margin-left: 20px;
            margin-right: 20px;
        }
        
        h1 {
            color: black;
            text-align: center;
        }
        
        p {
            font-family: verdana;
            font-size: 12px;
        }

Hopefully, none of this is a surprise, and it should be clear that this will be basic, but functional.

Now we can add a 'frontend/js' folder with an index.js file to do the work pulling the JSON from our Django application so that we can see some bears. In the index.js file you can add this code:

        const app = document.getElementById('root')

        const container = document.createElement('div')
        container.setAttribute('class', 'container')

        app.appendChild(container)

        // Create a request variable and assign a new XMLHttpRequest object to it.
        var request = new XMLHttpRequest()

        // Open a new connection, using the GET request on the URL endpoint
        request.open('GET', 'http://localhost:8000/?format=json', true)

        request.onload = function () {
        // Begin accessing JSON data here
        var data = JSON.parse(this.response)
        if (request.status >= 200 && request.status < 400) {
            data.forEach(bear => {
            const card = document.createElement('div')
            card.setAttribute('class', 'card')

            const h2 = document.createElement('h2')
            h2.textContent = bear.bearID

            const p = document.createElement('p')
            bear.id = bear.id
            p.textContent = `This is a ${ bear.age_class} aged bear 
            ${bear.bearID}, a ${ bear.sex } bear, who has has an tag in its' ${bear.ear_applied } ear, 
            with ${bear.pTT_ID } device, and was
            tagged at ${ bear.capture_lat } and ${ bear.capture_long }`

            container.appendChild(card)
            card.appendChild(h2)
            card.appendChild(p)
            })
        } else {
            const errorMessage = document.createElement('marquee')
            errorMessage.textContent = `Gah, it's not working!`
            app.appendChild(errorMessage)
        }
        }

        // Send request
        request.send()

This code uses the DOM of the page to dynamically add a container to the root, and then add each bear as a card into that container. The JSON is pulled from the Django app by using the ?format=json parameter in the URL request.

## Going Further
This app only touches the basics. You now know how to convert a current Django app into a RESTful one. You also know how to create a Javascript frontend to consume the JSON generated by your backend. You can find more of everything for the Django parts at https://www.django-rest-framework.org in either the tutorials, or API Guide, which have plenty.

This example still leaves more waiting to be done, depending upon your focus. These fall into three key areas:
1. You can build out more of the backend so that you can add new bears, and/or sightings, plus a means to edit, or delete entries. You would probably want to add some authentication for this too. 
2. There is more that could be done on the frontend so that we can browse bears and their associated sightings. 
3. Lastly, the code for the backend is mixed up: the methods to produce JSON sit alongside the methods to produce HTML. It might be worthwhile exploring how to separate the two of them more fully. This leads to more questions:
    1. Should the models and the database be in a separate app, with the JSON API and HTML being in two separate apps?
    2. If the bear models are separated out, then much code for JSON and HTML will still be similar, but the endpoints can be done differently - more consistently.

