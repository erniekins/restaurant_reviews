from __future__ import unicode_literals
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
import re, bcrypt, datetime

#email validation REGEX
EMAIL_REGEX = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)")

#user validations for login and registration and creates a user
class UserManager(models.Manager):
	def register_validation(self, input):
		error = []
		if(len(input["first_name"]) < 3):
			error.append("First name should be more than two characters")
		if(len(input["last_name"]) < 3):
			error.append("Last name should be more than two characters")
		if not EMAIL_REGEX.match(input["email"]):
			error.append("Email needs to be in the proper format")
		if(len(input["password"]) < 9):
			error.append("Password must be longer than eight characters")
		if input["password"] != input["password_confirm"]:
			error.append("Passwords must match")
		print(error, "******")
		return error

	def login_validation(self, input):
		error = []
		user = User.objects.filter(email=input["email"])
		if len(user) == 0:
			error.append("Email does not exist")
			return error
		if bcrypt.checkpw(input["password"].encode(), user[0].password.encode()):
			print("Passwords match!")
		else:
			error.append("Not a valid password")
		return error

	def create_user(self, input):
		hashpw = bcrypt.hashpw(input["password"].encode(), bcrypt.gensalt())
		user = self.create(
				first_name = input["first_name"],
				last_name = input["last_name"],
				email = input["email"],
				password = hashpw
			)
		return user

# Table for the user
class User(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

#validations for new restaurants
class RestaurantManager(models.Manager):
	def restaurant_validation(self, input):
		error = []
		if(len(input['name'])<1):
			error.append("Restaurant name must be present")
		if(len(input['cuisine'])<5):
			error.append("Please Select a type of cuisine")
		return error

	def create_restaurant(self, input, user):
		print(user.id, '*********')
		restaurant = self.create(
						name = input['name'],
						desc = input['desc'],
						cuisine = input['cuisine'],
						price = input['price']
		)
		return restaurant		


# Table for restaurants
class Restaurant(models.Model):
	name = models.CharField(max_length=255)
	desc = models.TextField()
	cuisine = models.CharField(max_length=100)
	price = models.IntegerField(
		validators=[
			MaxValueValidator(3),
			MinValueValidator(1)
		]
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	users = models.ManyToManyField(User, related_name='restaurants')
	objects = RestaurantManager()

# table for reviews which is a join table for restaurants and users 
class Review(models.Model):
	rating = models.IntegerField(
		default = 3,
		validators=[
			MaxValueValidator(5),
			MinValueValidator(1)
		]
	)
	review = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	# objects = ReviewManager()
	user = models.ForeignKey('User', related_name='reviews_user')
	restaurant = models.ForeignKey('Restaurant', related_name='reviews_restaurant')




