from django.utils import timezone
from django.shortcuts import redirect, render, get_object_or_404
from .models import Bear, Sighting
from .forms import BearForm

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

def bear_list(request):
    bears = Bear.objects.all()
    return render(request, 'bears/bear_list.html', {'bears' : bears})

def females(request):
    females = Bear.female()
    return render(request, 'bears/bear_list.html', {'bears' : females})

def bear_detail(request, id):
    bear = get_object_or_404(Bear, id=id)
    sightings = Sighting.objects.filter(bear_id=id)
    return render(request, 'bears/bear_detail.html', {'bear' : bear, 'sightings' : sightings})
