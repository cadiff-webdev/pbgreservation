from django.shortcuts import render
from .models import *
from django.urls import reverse, reverse_lazy
from django.shortcuts import render,get_object_or_404,redirect
from .forms import *
from django.contrib.auth import login, authenticate
from pprint import pprint
from itertools import chain
from django.contrib.auth.models import User

def index(request):
	#del request.session['reservations_count']
	#del request.session['reservations']

	if request.user.is_authenticated:
		return render(request,'reservations/index.html')
	else:
		return redirect('login')

def accomodation(request):
	if request.method == 'POST':
		form = AccomodationReservationForm(request.POST)
		if form.is_valid():
			start_date = form.cleaned_data.get('start_date')
			end_date = form.cleaned_data.get('end_date')
			comments = form.cleaned_data.get('comments')
			number_of_rooms = form.cleaned_data.get('number_of_rooms')
			number_of_guests = form.cleaned_data.get('number_of_guests')
			accomodation_type = form.cleaned_data.get('accomodation_type')
			branch = form.cleaned_data.get('branch')

			rescount = request.session.get('reservations_count', 0)
			rescount = rescount+1
			request.session['reservations_count'] = rescount
			
			reservation = {
				'id':rescount,
				'type':'accomodation',
				'start_date':str(start_date.date()),
				'end_date':str(end_date.date()),
				'comments':comments,
				'number_of_guests':number_of_guests,
				'number_of_rooms':number_of_rooms,
				'accomodation_type':str(accomodation_type),
				'accomodation_type_id':str(accomodation_type.id),
				'branch':branch.id}
			if not request.session.get('reservations'):
				request.session['reservations']={}
			request.session['reservations'].update({rescount:reservation})
			
			return redirect('reservations:index')
	else:
	  form = AccomodationReservationForm()
	return render(request,'reservations/accomodation_form.html', {'form': form})

def transportation(request):
	if request.method == 'POST':
		form = TransportationReservationForm(request.POST)
		if form.is_valid():
			date = form.cleaned_data.get('date')
			visit_reason = form.cleaned_data.get('visit_reason')
			car_type = form.cleaned_data.get('car_type')
			location = form.cleaned_data.get('location')
			
			rescount = request.session.get('reservations_count', 0)
			rescount = rescount+1
			request.session['reservations_count'] = rescount
			
			reservation = {
				'id':rescount,
				'type':'transportation',
				'date':str(date.date()),
				'visit_reason':visit_reason,
				'car_type':car_type,
				'location':location}

			if not request.session.get('reservations'):
				request.session['reservations']={}
			request.session['reservations'].update({rescount:reservation})
			
			return redirect('reservations:index')
	else:
	  form = TransportationReservationForm()
	return render(request,'reservations/transportation_form.html', {'form': form})

def security(request):
	if request.method == 'POST':
		form = SecurityReservationForm(request.POST)
		if form.is_valid():
			start_date = form.cleaned_data.get('start_date')
			end_date = form.cleaned_data.get('end_date')
			comments = form.cleaned_data.get('comments')
			security_package = form.cleaned_data.get('security_packages')
			
			rescount = request.session.get('reservations_count', 0)
			rescount = rescount+1
			request.session['reservations_count'] = rescount
			
			reservation = {
				'id':rescount,
				'type':'security',
				'start_date':str(start_date.date()),
				'end_date':str(end_date.date()),
				'security_package':str(security_package.id),
				'comments':comments}

			if not request.session.get('reservations'):
				request.session['reservations']={}
			request.session['reservations'].update({rescount:reservation})
			
			return redirect('reservations:index')
	else:
	  form = SecurityReservationForm()
	return render(request,'reservations/security_form.html', {'form': form})

def conference(request):
	if request.method == 'POST':
		form = ConferenceReservationForm(request.POST)
		if form.is_valid():
			date = form.cleaned_data.get('date')
			comments = form.cleaned_data.get('comments')
			branch = form.cleaned_data.get('branch')
			hall = form.cleaned_data.get('hall')
			
			rescount = request.session.get('reservations_count', 0)
			rescount = rescount+1
			request.session['reservations_count'] = rescount
			
			reservation = {
				'id':rescount,
				'type':'conference',
				'date':str(date.date()),
				'branch':str(branch.id),
				'hall':str(hall.id),
				'comments':comments}

			if not request.session.get('reservations'):
				request.session['reservations']={}
			request.session['reservations'].update({rescount:reservation})
				
			return redirect('reservations:index')
	else:
	  form = ConferenceReservationForm()
	return render(request,'reservations/conference_form.html', {'form': form})

def bookreservations(request):
	reservations = request.session.get('reservations')
	reservationscopy = reservations.copy()
	rescount = request.session.get('reservations_count')

	for key,reservation in reservations.items():
		if reservation['type'] == "accomodation":
			resid = reservation['id']
			sdate = datetime.datetime.strptime(reservation['start_date'], "%Y-%m-%d").date()
			edate = datetime.datetime.strptime(reservation['end_date'], "%Y-%m-%d").date()
			comments = reservation['comments']
			branch = Branch.objects.get(pk=reservation['branch'])
			number_of_guests=reservation['number_of_guests']
			number_of_rooms=reservation['number_of_rooms']
			accomodation_type = AccomodationType.objects.get(name=reservation['accomodation_type'])
			made_by = Pbguser.objects.get(pk=request.user.pbguser.id)
			guest_id = Pbguser.objects.get(pk=request.user.pbguser.id)
			accom_res = AccomodationReservation(status='R',start_date=sdate,end_date=edate,comments=comments,
				made_by=made_by,guest_id=guest_id)
			accom_res.save()

			reserved = ReservedAccomodation(reservation_id=accom_res,branch_id=branch,number_of_rooms=number_of_rooms,
				number_of_guests=number_of_guests,accomodation_type_id=accomodation_type)
			reserved.save()
			request.session['reservations_count']=rescount-1
			reservationscopy.pop(key)

		if reservation['type'] == "transportation":
			resid = reservation['id']
			sdate = datetime.datetime.strptime(reservation['date'], "%Y-%m-%d").date()
			edate=sdate
			visit_reason = reservation['visit_reason']
			car_type=reservation['car_type']
			location=reservation['location']
			made_by = Pbguser.objects.get(pk=request.user.pbguser.id)
			guest_id = Pbguser.objects.get(pk=request.user.pbguser.id)
			trans_res = TransportReservation(status='R',start_date=sdate,end_date=edate,purpose_of_visit=visit_reason,
				made_by=made_by,guest_id=guest_id,location=location)
			trans_res.save()
			request.session['reservations_count']=rescount-1
			reservationscopy.pop(key)
		
		if reservation['type'] == "conference":
			resid = reservation['id']
			sdate = datetime.datetime.strptime(reservation['date'], "%Y-%m-%d").date()
			edate=sdate
			branch = Branch.objects.get(pk=reservation['branch'])
			hall= ConferenceHall.objects.get(pk=reservation['hall'])
			comments=reservation['comments']
			made_by = Pbguser.objects.get(pk=request.user.pbguser.id)
			guest_id = Pbguser.objects.get(pk=request.user.pbguser.id)
			trans_res = ConferenceReservation(status='R',start_date=sdate,end_date=edate,conference_hall_id=hall,
				made_by=made_by,guest_id=guest_id,comments=comments)
			trans_res.save()
			request.session['reservations_count']=rescount-1
			reservationscopy.pop(key)	
	
		if reservation['type'] == "security":
			resid = reservation['id']
			sdate = datetime.datetime.strptime(reservation['start_date'], "%Y-%m-%d").date()
			edate = datetime.datetime.strptime(reservation['start_date'], "%Y-%m-%d").date()
			comments=reservation['comments']
			security_package=SecurityService.objects.get(pk=reservation['security_package'])
			made_by = Pbguser.objects.get(pk=request.user.pbguser.id)
			guest_id = Pbguser.objects.get(pk=request.user.pbguser.id)
			sec_res = SecurityReservation(status='R',start_date=sdate,end_date=edate,security_type=security_package,
				made_by=made_by,guest_id=guest_id,comments=comments)
			sec_res.save()
			request.session['reservations_count']=rescount-1
			reservationscopy.pop(key)	

	request.session['reservations'] = reservationscopy

	return render(request,'reservations/successfulbooking.html')

def admindashboard(request,category):
	accomodation = AccomodationReservation.objects.all()
	transportation = TransportReservation.objects.all()
	security = SecurityReservation.objects.all()
	conference = ConferenceReservation.objects.all()
	
	if(category=='accomodation'):
		reservations = accomodation
	elif(category=='transportation'):
		reservations = transportation
	elif(category=='security'):
		reservations = security
	elif(category=='conference'):
		reservations = conference
	else:		
		reservations = chain(accomodation,transportation)
		reservations = chain(reservations,security)
		reservations = chain(reservations,conference)

	return render(request,'reservations/admin/dashboard.html',{'reservations':reservations})

def userslist(request):
	users = Pbguser.objects.all()

	return render(request,'reservations/admin/users.html',{'users':users})

def clientdashboard(request,category):
	guest = Pbguser.objects.get(pk=request.user.pbguser.id)
	
	accomodation = AccomodationReservation.objects.filter(guest_id=guest)
	transportation = TransportReservation.objects.filter(guest_id=guest)
	security = SecurityReservation.objects.filter(guest_id=guest)
	conference = ConferenceReservation.objects.filter(guest_id=guest)
	
	if(category=='accomodation'):
		reservations = accomodation
	elif(category=='transportation'):
		reservations = transportation
	elif(category=='security'):
		reservations = security
	elif(category=='conference'):
		reservations = conference
	else:		
		reservations = chain(accomodation,transportation)
		reservations = chain(reservations,security)
		reservations = chain(reservations,conference)

	return render(request,'reservations/client/dashboard.html',{'reservations':reservations})

def signup(request):
  if request.method == 'POST':
      form = SignUpForm(request.POST)
      if form.is_valid():
          user = form.save()
          user.refresh_from_db()
          user.pbguser.gender = form.cleaned_data.get('gender')
          user.save()
          username = form.cleaned_data.get('username')
          raw_password = form.cleaned_data.get('password1')
          user = authenticate(username=username, password=raw_password)
          login(request, user)
          return redirect('reservations:index')
  else:
      form = SignUpForm()
  return render(request, 'registration/signup.html', {'form': form})
