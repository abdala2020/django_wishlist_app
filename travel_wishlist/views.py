from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm
# Create your views here.

def place_list(request):
    """if this is a Post request, the user clicked the add button
    in the form. check if the new place is valid, if so, save a
    new Place to the database, and redirect to this same page.

    if not a Post route, or Place is not valid, display a page with
    a list of places and a form to add a new place.
    """
    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        place = form.save() #create a new Place from the form
        if form.is_valid(): # checks agains DB constraints
            place.save()    # saves to the database
            return redirect('place_list')

    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm() # used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_pace_form': new_place_form})

def about(request):
    author = 'Abdala'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})

def places_visited(request):
    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

def place_was_visited(request, place_pk):
    if request.method == 'POST':
        # place = Place.objects.get(pk=place_pk)
        place = get_object_or_404(Place, pk=place_pk)
        place.visited = True
        place.save()
    return redirect('place_list') # redirects to wishlist places