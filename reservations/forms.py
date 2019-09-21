from django import forms
from django.contrib.auth.forms import AuthenticationForm,UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django.utils.timezone import now
from reservations.models import * 
import datetime 
from .widgets import BootstrapDateTimePickerInput

	
class AccomodationReservationForm(forms.Form):
	room_type= [('S','Standard Room'),('E','VIP Room'),('V','Villa')]
	start_date = forms.DateTimeField(
		label='CHECK IN',
    input_formats=['%d/%m/%Y'], 
    widget=BootstrapDateTimePickerInput(),
    initial=datetime.date.today()
  )
	start_date.widget.attrs.update({'class': 'form-control'})
	end_date = forms.DateTimeField(
		label='CHECK OUT',
    input_formats=['%d/%m/%Y'], 
    widget=BootstrapDateTimePickerInput()
  )
	end_date.widget.attrs.update({'class': 'form-control'})
	comments = forms.CharField(required=False,widget=forms.Textarea())
	comments.widget.attrs.update({'class': 'commentbox form-control'})
	branch =  forms.ModelChoiceField(Branch.objects.all())
	branch.widget.attrs.update({'class': 'form-control'})
	number_of_rooms = forms.IntegerField(min_value=1)
	number_of_rooms.widget.attrs.update({'class': 'form-control'})
	number_of_guests = forms.IntegerField(min_value=1)
	number_of_guests.widget.attrs.update({'class': 'form-control'})


	extra_attrs={}
	# rooms = Accomodation.objects.all()
	# roomtypes = AccomodationType.objects.all()
	
	# for roomtype in roomtypes:
	# 	rooms = rooms.filter(accomodation_type__name__exact=roomtype.name)
	# 	total_room_count = len(rooms)
	# 	vacant_room_count = len(rooms.filter(vacant=True))

	# 	extra_attrs.update({'data-vacant-'+roomtype.name.replace(" ",""):vacant_room_count})

	extra_attrs.update({'class':'form-control'})
	accomodation_type =  forms.ModelChoiceField(AccomodationType.objects.all(),label='ROOM TYPE')
	accomodation_type.widget.attrs.update(extra_attrs)

class SecurityReservationForm(forms.Form):
	start_date = forms.DateTimeField(
		label='MEETING DATE',
    input_formats=['%d/%m/%Y'], 
    widget=BootstrapDateTimePickerInput()
  )
	start_date.widget.attrs.update({'class': 'form-control'})
	end_date = forms.DateTimeField(
		label='MEETING DATE',
    input_formats=['%d/%m/%Y'], 
    widget=BootstrapDateTimePickerInput()
  )
	end_date.widget.attrs.update({'class': 'form-control'})
	comments = forms.CharField(required=False,widget=forms.Textarea())
	comments.widget.attrs.update({'class': 'commentbox form-control'})
	security_options = [('S','Site-Based'),('M','Mobile'),('C','Close Protection')]
	security_packages = forms.ModelChoiceField(SecurityService.objects.all())
	security_packages.widget.attrs.update({'class': 'form-control'})
	number_of_guests = forms.IntegerField(min_value=1)
	number_of_guests.widget.attrs.update({'class': 'form-control'})
	
class ConferenceReservationForm(forms.Form):
	date = forms.DateTimeField(
		label='MEETING DATE',
    input_formats=['%d/%m/%Y'], 
    widget=BootstrapDateTimePickerInput()
  )
	date.widget.attrs.update({'class': 'form-control'})
	comments = forms.CharField(required=False,widget=forms.Textarea())
	comments.widget.attrs.update({'class': 'commentbox form-control'})
	branch = forms.ModelChoiceField(Branch.objects.all())
	branch.widget.attrs.update({'class': 'form-control'})
	hall = forms.ModelChoiceField(ConferenceHall.objects.all())
	hall.widget.attrs.update({'class': 'form-control'})
	number_of_guests = forms.IntegerField(min_value=1)
	number_of_guests.widget.attrs.update({'class': 'form-control'})
	 
class TransportationReservationForm(forms.Form):
	date = forms.DateTimeField(
		label='TRAVEL DATE',
    input_formats=['%d/%m/%Y'], 
    widget=BootstrapDateTimePickerInput()
  )
	car_options = [('A','Armored'),('N','Normal')]
	car_type = forms.CharField(max_length=1,widget=forms.Select(choices=car_options))
	car_type.widget.attrs.update({'class': 'form-control'})
	location = forms.CharField(max_length=200)
	location.widget.attrs.update({'class': 'form-control'})
	visit_reason = forms.CharField(required=False,widget=forms.Textarea())
	visit_reason.widget.attrs.update({'class': 'form-control, commentbox'})
	number_of_guests = forms.IntegerField(min_value=1)
	number_of_guests.widget.attrs.update({'class': 'form-control'})


class SignUpForm(UserCreationForm):
	first_name = forms.CharField(
		max_length=30, 
		required=False, help_text='Optional',
		widget=forms.TextInput(attrs={'placeholder':'First Name'}
		))
	last_name = forms.CharField(
		max_length=30, required=False, help_text='Optional',
				widget=forms.TextInput(attrs={'placeholder':'Last Name'}))
	email = forms.EmailField(max_length=254, help_text='Required. Provide a valid email address.',
				widget=forms.TextInput(attrs={'placeholder':'Email Address'}))
	gender_choices = [('M','Male'),('F','Female')]
	gender = forms.CharField(max_length=1, help_text='M / F',widget=forms.RadioSelect(choices=gender_choices))

	class Meta:
		model = User
		fields = ('username','password1','password2','first_name','last_name','email','gender')
		widgets = {
      'password1': forms.fields.TextInput(attrs={'placeholder': 'Password'}),
      'username': forms.fields.TextInput(attrs={'placeholder': 'Username'}),
      'password2': forms.fields.TextInput(attrs={'placeholder': 'Confirm Password'})
    }

class EditUserForm(UserChangeForm):
	class Meta:
		model = User
		fields = ('email','username','first_name','last_name')
		widgets = {
      'first_name': forms.fields.TextInput(attrs={'class': 'form-control'}),
      'last_name': forms.fields.TextInput(attrs={'class': 'form-control'}),
      'username': forms.fields.TextInput(attrs={'class': 'form-control'}),
      'email': forms.fields.TextInput(attrs={'class': 'form-control'}),
    }


class EditPbguserForm(UserChangeForm):
	class Meta:
		model = Pbguser
		fields = ('gender','phone_number')
		widgets = {
			'gender':forms.RadioSelect(attrs={'class': 'form-control'}),
  		'phone_number': forms.fields.TextInput(attrs={'class': 'form-control'}),
		}		

