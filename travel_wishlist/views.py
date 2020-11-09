from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
# Create your views here.

@login_required
def place_list(request):
    """if this is a Post request, the user clicked the add button
    in the form. check if the new place is valid, if so, save a
    new Place to the database, and redirect to this same page.

    if not a Post route, or Place is not valid, display a page with
    a list of places and a form to add a new place.
    """
    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False) #create a new Place from the form
        place.user = request.user
        if form.is_valid(): # checks against DB constraints
            place.save()    # saves to the database
            return redirect('place_list')

    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm() # used to create HTML
    return render(request, 'travel_wishlist/wishlist.html', {'places': places, 'new_pace_form': new_place_form})

@login_required
def about(request):
    author = 'Abdala'
    about = 'A website to create a list of places to visit'
    return render(request, 'travel_wishlist/about.html', {'author': author, 'about': about})

@login_required
def places_visited(request):
    visited = Place.objects.filter(user=request.user).filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', {'visited': visited})

@login_required
def place_was_visited(request, place_pk):
    if request.method == 'POST':
        place = get_object_or_404(Place, pk=place_pk)
        if place.user == request.user:#only let user visit thier own places
            place.visited = True
            place.save()
        else:
            return redirect('place_list') # redirects to wishlist places

@login_required 
def place_details(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    
    #does this place belong to a current user?
    if place.user != request.user:
        return HttpResponseForbidden()
    #is this a Get request (show data +form) or a Post request (update place object)

    #if POST request, validate form data and update
    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)
        #instance is the model object to update with the form data
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information update')
        else:
            messages.error(request, form.errors) #temp error message. future version should improve

        return redirect('place_details', place_pk=place_pk)

    else: # Get place details
        #if GET request, show Place info and option form 
        # if place is visited, show form, if not show no form
        if place.visited:
            review_form = TripReviewForm(instance=place)
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form} )
        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place} )

@login_required
def delete_place(request, place_pk):
    place = get_object_or_404(Place, pk=place_pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()
    
    return redirect('place_list')