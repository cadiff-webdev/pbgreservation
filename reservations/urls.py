from django.urls import path,re_path
from . import views

app_name='reservations'
urlpatterns = [
    path('', views.index, name='index'),
    path('accomodation',views.accomodation, name='accomodationform'),
    path('transportation',views.transportation, name='transportationform'),
    path('security',views.security, name='securityform'),
    path('conference',views.conference,name='conferenceform'),
   
    path('admin/edit/<slug:category>/<int:res_id>/',views.editreservation,name='edit_reservation'),
    path('dashboard/account/',views.editprofile,name='editprofile'),
    re_path(r'^dashboard/(?P<category>[\w]*)/',views.clientdashboard,name='clientdashboard'),
    re_path(r'^admin/list/(?P<category>[\w]*)/',views.admindashboard,name='admindashboard'),
    
    path('admin/users/',views.userslist,name='users'),
    path('signup/',views.signup,name='signup'),
    path('book/',views.bookreservations,name='book'),


]
