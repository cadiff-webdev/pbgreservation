from django.urls import path
from . import views

app_name='reservations'
urlpatterns = [
    path('', views.index, name='index'),
    path('accomodation',views.accomodation, name='accomodationform'),
    path('transportation',views.transportation, name='transportationform'),
    path('security',views.security, name='securityform'),
    path('conference',views.conference,name='conferenceform'),
    path('admin-site/',views.admindashboard,name='admindashboard'),
    path('dashboard/',views.clientdashboard,name='clientdashboard'),
    path('admin-site/users/',views.userslist,name='users'),
    path('signup/',views.signup,name='signup'),
    path('book/',views.bookreservations,name='book'),


]
