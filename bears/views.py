from django.utils import timezone
from django.shortcuts import redirect, render, get_object_or_404
from rest_framework import status
from rest_framework.renderers import JSONRenderer, TemplateHTMLRenderer
from rest_framework.decorators import api_view, APIView, renderer_classes
from rest_framework.response import Response
from .models import Bear, Sighting
from .forms import BearForm
from .serializers import BearSerializer, SightingSerializer

def bear_new(request):
    if request.method=="POST":
        form = BearForm(request.POST)
        if form.is_valid():
            bear = form.save(commit=False) # don't save yet, as want to add created_date
            bear.created_date = timezone.now()
            bear.save()
            return redirect('bear_detail', id=bear.id) # use bear.id as we already have instance
    else:
        form = BearForm()
    return render(request, 'bears/bear_edit.html', {'form': form}) #folder/file_name under 'templates' folder

def bear_edit(request, id):
    bear = get_object_or_404(Bear, id=id)
    if request.method=="POST":
        form = BearForm(request.POST, instance=bear)
        if form.is_valid():
            bear = form.save(commit=False)
            bear.created_date = timezone.now()
            bear.save()
            return redirect('bear_detail', id=bear.id)
    else:
        form = BearForm(instance=bear)
    return render(request, 'bears/bear_edit.html', {'form': form, 'bear': bear})

def bear_delete(request, id):
    bear = get_object_or_404(Bear, id=id)
    bear.delete()
    return redirect('bear_list' )

@api_view(['GET'])
@renderer_classes([TemplateHTMLRenderer, JSONRenderer])
def bear_list(request, format=None):
    bears = Bear.objects.all()
    if request.accepted_renderer.format =='html':
        return render(request, 'bears/bear_list.html', {'bears' : bears})
    serializer = BearSerializer(bears, many=True)
    data = serializer.data
    return Response(data)

def females(request):
    females = Bear.female()
    return render(request, 'bears/bear_list.html', {'bears' : females})

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

       
    
