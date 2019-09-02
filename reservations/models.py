from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django import forms

class Pbguser(models.Model):
	user = models.OneToOneField(
		User,
		default=None,
		null=True,
		on_delete=models.CASCADE)
	gender_choices = [('M','Male'),('F','Female')]
	gender = models.CharField(
		choices=gender_choices,
		max_length=1,
		default=None,
		null=True
		)
	phone_number = models.CharField(max_length=50)

	@receiver(post_save,sender=User)
	def create_user_profile(sender,instance,created,**kwargs):
		if created:
			Pbguser.objects.create(user=instance)

	@receiver(post_save,sender=User)
	def update_user_profile(sender,instance,**kwargs):
		instance.pbguser.save()
	def __str__(self):
		return self.user.get_full_name()

class AccomodationType(models.Model):
	name = models.CharField(max_length=20,unique=True)
	description = models.TextField()
	capacity = models.PositiveIntegerField(default=0)

	def __str__(self):
		return self.name

class Branch(models.Model):
	name = models.CharField(max_length=200,unique=True)
	contact = models.CharField(max_length=200,blank=True)
	def __str__(self):
		return self.name

class Accomodation(models.Model):
	room_number = models.CharField(max_length=200,unique=True)
	vacant = models.BooleanField(default=True)
	branch_id =  models.ForeignKey(Branch,on_delete=models.PROTECT)
	accomodation_type_id = models.ForeignKey(AccomodationType,on_delete=models.PROTECT) 
	description = models.CharField(max_length=200)
	def __str__(self):
		return self.room_number
	


class ConferenceHall(models.Model):
	name = models.CharField(unique=True,max_length=200)
	description = models.TextField(blank=True)
	theatre_cap = models.SmallIntegerField(default=0) 
	classroom_cap = models.SmallIntegerField(default=0)
	ushape_cap = models.SmallIntegerField(default=0)
	reception_cap = models.SmallIntegerField(default=0)
	width_in_meters = models.SmallIntegerField('width',default=0)
	length_in_meters = models.SmallIntegerField('length',default=0)
	branch_id = models.ForeignKey(Branch,on_delete=models.PROTECT)
	def __str__(self):
		return self.name

class Reservation(models.Model):
	status_options=[('R','Requested'),('A','Accepted'),('D','Denied')]
	status = models.CharField(choices=status_options,max_length=1)
	start_date = models.DateField()
	end_date = models.DateField()
	comments = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)
	class Meta:
		abstract = True

class AccomodationReservation(Reservation):
	made_by = models.ForeignKey(Pbguser,related_name='room_made_by',on_delete=models.PROTECT)
	guest_id = models.ForeignKey(Pbguser,related_name='room_guest_id',on_delete=models.PROTECT)
	def gettype(self):
		return "accomodation"
		
class ReservedAccomodation(models.Model):
	branch_id = models.ForeignKey(Branch,on_delete=models.PROTECT)
	number_of_rooms = models.SmallIntegerField()
	number_of_guests = models.SmallIntegerField()
	reservation_id = models.ForeignKey(AccomodationReservation,on_delete=models.PROTECT)
	accomodation_type_id= models.ForeignKey(AccomodationType,on_delete=models.PROTECT)

class SecurityService(models.Model):
	name = models.CharField(max_length=200,unique=True)
	description = models.TextField(default='')
	def __str__(self):
		return self.name

class SecurityReservation(Reservation):
	made_by = models.ForeignKey(Pbguser,related_name='security_made_by',on_delete=models.PROTECT)
	guest_id = models.ForeignKey(Pbguser,related_name='security_guest_id',on_delete=models.PROTECT)
	security_type = models.ForeignKey(SecurityService,on_delete=models.PROTECT)
	def gettype(self):
		return "security"

class ConferenceReservation(Reservation):
	made_by = models.ForeignKey(Pbguser,related_name='conference_made_by',on_delete=models.PROTECT)
	guest_id = models.ForeignKey(Pbguser,related_name='conference_guest_id',on_delete=models.PROTECT)
	conference_hall_id = models.ForeignKey(ConferenceHall,on_delete=models.PROTECT)
	def gettype(self):
		return "conference"

class TransportReservation(Reservation):
	made_by = models.ForeignKey(Pbguser,related_name='transport_made_by',on_delete=models.PROTECT)
	guest_id = models.ForeignKey(Pbguser,related_name='transport_guest_id',on_delete=models.PROTECT)
	car_options = [('A','Armored'),('N','Normal')]
	car_type = models.CharField(choices=car_options,max_length=1,default='N')
	districts = ['']
	district = models.CharField(max_length=100,default='')
	location = models.CharField(max_length=200)
	purpose_of_visit = models.CharField(max_length=200)
	def gettype(self):
		return "transportation"