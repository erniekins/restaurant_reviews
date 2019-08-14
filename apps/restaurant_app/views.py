from django.shortcuts import render, HttpResponse, redirect
from .models import *
import bcrypt
from django.contrib import messages

#login page displays login.html
def login(request):
	return render(request, "restaurant_app/login.html")

# adding a new user from the login page
def register(request):
	if request.method == "POST":
		errors = User.objects.register_validation(request.POST)
		if len(errors) == 0:
			user = User.objects.create_user(request.POST)
			request.session["id"] = user.id
			return redirect('/main')
		for error in errors:
			messages.error(request, error)
		return redirect("/")

#checks if user logging in is a valid user
def login_validate(request):
	errors = User.objects.login_validation(request.POST)
	print(errors, '///////')
	if len(errors) == 0:
		user = User.objects.filter(email=request.POST['email'])
		request.session['id'] = user[0].id
		return redirect('/main')
	for error in errors:
		messages.error(request, error)
		return redirect('/')

# renders the main page aka the one that would be the users landing page on login
def main(request):
	user = User.objects.get(id=request.session["id"])
	restaurant = Restaurant.objects.all()
	context = {
		'user': user,
		'restaurants': restaurant
	}
	return render(request, "restaurant_app/main.html", context)
def restaurant_new(request):
	context = {
	'user': User.objects.get(id=request.session['id'])
	}
	return render(request, 'restaurant_app/restaurant.html', context)

def add_new(request):
	if request.method == "POST":
		errors = Restaurant.objects.restaurant_validation(request.POST)
		for error in errors:
			messages.error(request, error)
			return redirect('/restaurant_new')
		if len(errors) == 0:
			user = User.objects.get(id=request.session['id'])
			print(user, '?????')
			Restaurant.objects.create_restaurant(request.POST, user)
		return redirect('/main')

def add_review(request, restaurant_id):
	context = {
		'user' : User.objects.get(id=request.session['id']),
		'restaurant_reviewed' : Restaurant.objects.get(id=restaurant_id)
	}
	return render(request, 'restaurant_app/review.html', context)

#will logout a user deleted the session returns to login page
def logout(request):
	if 'id' in request.session:
		request.session.pop('id')
	return redirect('/')

	
