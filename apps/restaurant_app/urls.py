from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.login),
	url(r'^register$', views.register),
	url(r'^main$', views.main),
	url(r'^login_validate$', views.login_validate),
	url(r'^restaurant_new$', views.restaurant_new),
	url(r'^add_new$', views.add_new),
	url(r'^add_review/(?P<restaurant_id>\d+)$', views.add_review),
	url(r'^logout$', views.logout)
]