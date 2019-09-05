from django.shortcuts import render
from .models import *
from django.urls import reverse, reverse_lazy
from django.shortcuts import render,get_object_or_404,redirect
from .forms import *
from django.contrib.auth import login, authenticate
from pprint import pprint
from itertools import chain
from django.contrib.auth.models import User
from django.core import serializers
from django.core.mail import BadHeaderError, send_mail, EmailMultiAlternatives
from django.conf import settings
from django.template.loader import get_template
from django.template import Context

def index(request):
	del request.session['reservations_count']
	del request.session['reservations']
	
	request.session['rooms']={}
	rooms = Accomodation.objects.all()
	roomtypes = AccomodationType.objects.all()
	
	for roomtype in roomtypes:
		rooms = rooms.filter(accomodation_type__name__exact=roomtype.name)
		total_room_count = len(rooms)
		vacant_room_count = len(rooms.filter(vacant=True))
		request.session['rooms'].update({roomtype.name:vacant_room_count})
	
	if request.user.is_authenticated:
		return render(request,'reservations/index.html')
	else:
		return redirect('login')

def validate_accom(request,reservation):
	number_of_guests=reservation['number_of_guests']
	number_of_rooms=reservation['number_of_rooms']
	accomodation_type=reservation['accomodation_type']
	room_availability=request.session.get('rooms')
	availability = int(room_availability[accomodation_type])
	if number_of_rooms > availability:
		return False
	else:
		return True

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
			display_info = {
				'GUESTS':number_of_guests,
				'ROOMS':number_of_rooms,
				'CHECK-IN':str(start_date.date()),
				'CHECK-OUT':str(end_date.date())
			}
			reservation = {
				'id':rescount,
				'type':'accomodation',
				'start_date':str(start_date.date()),
				'end_date':str(end_date.date()),
				'comments':comments,
				'number_of_guests':number_of_guests,
				'number_of_rooms':number_of_rooms,
				'accomodation_type':str(accomodation_type),
				'branch':branch.id,
				'todisplay':display_info}
			vd=validate_accom(request,reservation)
			if not vd:
				raise forms.ValidationError("Not enough rooms")

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
			display_info = {
				'CAR TYPE':car_type,
				'LOCATION':location,
				'TRAVEL-DATE':str(date.date()),
			}
			reservation = {
				'id':rescount,
				'type':'transportation',
				'date':str(date.date()),
				'visit_reason':visit_reason,
				'car_type':car_type,
				'location':location,
				'todisplay':display_info}

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
			display_info = {
				'SERVICE':str(security_package.name),
				'START DATE':str(start_date.date()),
				'END DATE':str(end_date.date())
			}
			reservation = {
				'id':rescount,
				'type':'security',
				'start_date':str(start_date.date()),
				'end_date':str(end_date.date()),
				'security_package':str(security_package.id),
				'comments':comments,
				'todisplay':display_info}

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
			number_of_guests = form.cleaned_data.get('number_of_guests')
			
			rescount = request.session.get('reservations_count', 0)
			rescount = rescount+1
			request.session['reservations_count'] = rescount
			display_info={
				'DATE':str(date.date()),
				'BRANCH':str(branch.name),
				'HALL':str(hall.name),
				'GUESTS':number_of_guests
				}
			reservation = {
				'id':rescount,
				'type':'conference',
				'date':str(date.date()),
				'branch':str(branch.id),
				'hall':str(hall.id),
				'number_of_guests':number_of_guests,
				'comments':comments,
				'todisplay':display_info}

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
				made_by=made_by,number_of_guests=number_of_guests,guest_id=guest_id)
			accom_res.save()

			reserved = ReservedAccomodation(reservation_id=accom_res,branch_id=branch,number_of_rooms=number_of_rooms,
				accomodation_type=accomodation_type)
			reserved.save()
			request.session['reservations_count']=rescount-1
			reservationscopy.pop(key)

		if reservation['type'] == "transportation":
			resid = reservation['id']
			sdate = datetime.datetime.strptime(reservation['date'], "%Y-%m-%d").date()
			edate=sdate
			visit_reason = reservation['visit_reason']
			car_type=reservation['car_type']
			number_of_guests=reservation['number_of_guests']
			ocation=reservation['location']
			made_by = Pbguser.objects.get(pk=request.user.pbguser.id)
			guest_id = Pbguser.objects.get(pk=request.user.pbguser.id)
			trans_res = TransportReservation(status='R',start_date=sdate,end_date=edate,purpose_of_visit=visit_reason,
				made_by=made_by,guest_id=guest_id,location=location,number_of_guests=number_of_guests)
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
			number_of_guests=reservation['number_of_guests']
			made_by = Pbguser.objects.get(pk=request.user.pbguser.id)
			guest_id = Pbguser.objects.get(pk=request.user.pbguser.id)
			trans_res = ConferenceReservation(status='R',start_date=sdate,end_date=edate,conference_hall_id=hall,
				made_by=made_by,guest_id=guest_id,comments=comments,number_of_guests=number_of_guests)
			trans_res.save()
			request.session['reservations_count']=rescount-1
			reservationscopy.pop(key)	
	
		if reservation['type'] == "security":
			resid = reservation['id']
			sdate = datetime.datetime.strptime(reservation['start_date'], "%Y-%m-%d").date()
			edate = datetime.datetime.strptime(reservation['start_date'], "%Y-%m-%d").date()
			comments=reservation['comments']
			security_package=SecurityService.objects.get(pk=reservation['security_package'])
			number_of_guests=reservation['number_of_guests']
			made_by = Pbguser.objects.get(pk=request.user.pbguser.id)
			guest_id = Pbguser.objects.get(pk=request.user.pbguser.id)
			sec_res = SecurityReservation(status='R',start_date=sdate,end_date=edate,security_type=security_package,
				made_by=made_by,guest_id=guest_id,comments=comments,number_of_guests=number_of_guests)
			sec_res.save()
			request.session['reservations_count']=rescount-1
			reservationscopy.pop(key)	

	request.session['reservations'] = reservationscopy
	request.session['reservations_count'] = 0

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
	def myfn(r):
		return r.created_at

	reservations = sorted(reservations,key=myfn)
	return render(request,'reservations/admin/dashboard.html',{'reservations':reservations})

def userslist(request):
	users = Pbguser.objects.all()

	return render(request,'reservations/admin/users.html',{'users':users})

def clientaccount(request,user_id):
	user = Pbguser.objects.get(pk=user_id)

	return render(request,'reservations/dashboard/clientaccount.html',{'user':user})

def editreservation(request,category,res_id):
	if(category=='accomodation'):
		reservation = AccomodationReservation.objects.select_related().get(pk=res_id)
		roominfo = ReservedAccomodation.objects.get(reservation_id=res_id)
		error =''
		msg=''
		if request.method == 'POST':
			if request.POST.get("btn_approve") and not reservation.status=='A':
				#block one room of that type and change status of the reservation
				rooms = Accomodation.objects.filter(vacant=True,accomodation_type=roominfo.accomodation_type,branch_id=roominfo.branch_id)
				if len(rooms)>=roominfo.number_of_rooms:
					selected_rooms = rooms[:roominfo.number_of_rooms]
					for room in selected_rooms:
						room.vacant=False
						room.save()
					
					reservation.status='A'
					reservation.save()
					#send email 
					html_message = get_template('reservations/email_reservation_confirmed.html')

					subject = "TEST EMAIL"
					text_message = "Test email"
					recepients = ["michaelmulatya@hotmail.com"]
					sender = settings.EMAIL_HOST_USER
					email_msg = EmailMultiAlternatives(subject, text_message, sender, recepients)
					email_msg.attach_alternative(html_message.render({'reservation':reservation}), "text/html")	
					email_msg.send()

					msg="Reservation Accepted. A confirmation email has been sent to the guest."
					return render(request,'reservations/admin/accom_reservation.html',{'res':reservation,'room':roominfo,'success':1,'msg':msg})
				else:
					error = 'No rooms available'
			elif request.POST.get("btn_reject") and not reservation.status=='D':
				#change status of reservation to Denied
				reservation.status='D'
				reservation.save()
				return render(request,'reservations/admin/accom_reservation.html',{'res':reservation,'room':roominfo,'success':1,'msg':'Reservation denied.'})
			elif request.POST.get("btn_cancel") and not reservation.status=='C':
				#change status of reservation to Cancelled. Unblock rooms
				rooms = Accomodation.objects.filter(vacant=False,accomodation_type=roominfo.accomodation_type,branch_id=roominfo.branch_id)
				if len(rooms)>=roominfo.number_of_rooms:
					selected_rooms = rooms[:roominfo.number_of_rooms]
					for room in selected_rooms:
						room.vacant=True
						room.save()
					
					reservation.status='C'
					reservation.save()
					return render(request,'reservations/admin/accom_reservation.html',{'res':reservation,'room':roominfo,'success':1,'msg':'Reservation cancelled.'})
				else:
					error = "No booked rooms to unblock."
			else:
				error = "This action has already been performed."
			return render(request,'reservations/admin/accom_reservation.html',{'res':reservation,'room':roominfo,'error':error})
					
		return render(request,'reservations/admin/accom_reservation.html',{'res':reservation,'room':roominfo})
	elif(category=='transportation'):
		reservation =get_object_or_404( TransportReservation,pk=res_id)
		duration = reservation.start_date - reservation.end_date
		
		if request.method == 'POST':
			if request.POST.get("btn_approve") and not reservation.status=='A':
					reservation.status='A'
					reservation.save()
					return render(request,'reservations/admin/trans_reservation.html',{'res':reservation,'duration':duration,'success':1,'msg':"Reservation Approved."})
			elif request.POST.get("btn_reject") and not reservation.status=='D':
				reservation.status='D'
				reservation.save()
				return render(request,'reservations/admin/trans_reservation.html',{'res':reservation,'duration':duration,'success':1,'msg':"Reservation Denied."})
			elif request.POST.get("btn_cancel") and not reservation.status=='C':
				reservation.status='C'
				reservation.save()
				return render(request,'reservations/admin/trans_reservation.html',{'res':reservation,'duration':duration,'success':1,'msg':"Reservation Cancelled."})
			else:
				error = "This action cannot be performed."
			return render(request,'reservations/admin/trans_reservation.html',{'res':reservation,'duration':duration,'error':"Reservation Denied."})	
		else:
			return render(request,'reservations/admin/trans_reservation.html',{'res':reservation,'duration':duration})
	elif(category=='security'):
		reservation = get_object_or_404(SecurityReservation,pk=res_id)
		duration = reservation.start_date - reservation.end_date
		
		if request.method == 'POST':
			if request.POST.get("btn_approve") and not reservation.status=='A':
					reservation.status='A'
					reservation.save()
					return render(request,'reservations/admin/sec_reservation.html',{'res':reservation,'duration':duration,'success':1,'msg':"Reservation Approved."})
			elif request.POST.get("btn_reject") and not reservation.status=='D':
				reservation.status='D'
				reservation.save()
				return render(request,'reservations/admin/sec_reservation.html',{'res':reservation,'duration':duration,'success':1,'msg':"Reservation Denied."})
			elif request.POST.get("btn_cancel") and not reservation.status=='C':
				reservation.status='C'
				reservation.save()
				return render(request,'reservations/admin/sec_reservation.html',{'res':reservation,'duration':duration,'success':1,'msg':"Reservation Cancelled."})
			else:
				error = "This action cannot be performed."
			return render(request,'reservations/admin/sec_reservation.html',{'res':reservation,'duration':duration,'error':"Reservation Denied."})	
		else:
			return render(request,'reservations/admin/sec_reservation.html',{'res':reservation,'duration':duration})
	elif(category=='conference'):
		reservation = get_object_or_404(ConferenceReservation,pk=res_id)
		duration = reservation.start_date - reservation.end_date
		if request.method == 'POST':
			if request.POST.get("btn_approve") and not reservation.status=='A':
					reservation.status='A'
					reservation.save()
					return render(request,'reservations/admin/conf_reservation.html',{'res':reservation,'duration':duration,'success':1,'msg':"Reservation Approved."})
			elif request.POST.get("btn_reject") and not reservation.status=='D':
				reservation.status='D'
				reservation.save()
				return render(request,'reservations/admin/conf_reservation.html',{'res':reservation,'duration':duration,'success':1,'msg':"Reservation Denied."})
			elif request.POST.get("btn_cancel") and not reservation.status=='C':
				reservation.status='C'
				reservation.save()
				return render(request,'reservations/admin/conf_reservation.html',{'res':reservation,'duration':duration,'success':1,'msg':"Reservation Cancelled."})
			else:
				error = "This action cannot be performed."
			return render(request,'reservations/admin/conf_reservation.html',{'res':reservation,'duration':duration,'error':"Reservation Denied."})	
		else:
			return render(request,'reservations/admin/conf_reservation.html',{'res':reservation,'duration':duration})
	else:
		return render(request,'reservations/admin/dashboard.html')
def testemail(request):
	return render(request,'reservations/email_reservation_confirmed.html')

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

def editprofile(request):
	if request.method == 'POST':
		userform = EditUserForm(request.POST,instance=request.user)
		pbguserform = EditPbguserForm(request.POST,request.FILES,instance=request.user.pbguser)

		if userform.is_valid() and pbguserform.is_valid():
			user = userform.save()
			pbguser = pbguserform.save()
			pbguser.user=user
			if pbguser.phone_number=='1234':
				return redirect('reservations:index')
			if request.user.is_staff:
				return redirect('reservations:admindashboard','all')
			else:
				return redirect('reservations:clientdashboard','all')		
	else:
		userform = EditUserForm(instance=request.user)
		pbguserform = EditPbguserForm(instance=request.user.pbguser)
		args = {}
		# args.update(csrf(request))
		args['userform'] = userform
		args['pbguserform'] = pbguserform
	if request.user.is_staff:
		return render(request, 'reservations/admin/editprofile.html', {'userform': userform,'pbguserform':pbguserform})
	else:
		return render(request, 'reservations/client/editprofile.html', {'userform': userform,'pbguserform':pbguserform})
		