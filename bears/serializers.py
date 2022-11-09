from django.contrib.auth.models import User, Group #common, but we don't need them
from rest_framework import serializers
from .models import Bear, Sighting

class BearSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bear
        fields = ['id','bearID', 'pTT_ID', 'capture_lat', 'capture_long', 'sex', 'age_class', 'ear_applied', 'created_date']

# As we have no views associated with sightings, we use a model serialiser
class SightingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sighting
        fields = ['bear_id', 'deploy_id', 'recieved', 'latitude', 'longitude', 'temperature', 'created_date']

