# Generated by Django 2.1.12 on 2019-09-20 12:14

from django.db import migrations

def populate_branches(apps,schema_editor):
	Branch = apps.get_model('reservations','Branch')
	if not Branch.objects.filter(name="Peace 1").exists():
		b1=Branch.objects.create(name='Peace 1')
		b2=Branch.objects.create(name='Peace 2')
	

def populate_room_types(apps,schema_editor):
	AccomodationType = apps.get_model('reservations','AccomodationType')
	if not AccomodationType.objects.filter(name="Deluxe Room").exists():
		acc1=AccomodationType.objects.create(name='Deluxe Room',
			description="Ensuite bathroom with a refreshing rainshower and a spacious executive workspace.",
			price='145',
			capacity='2')
		acc2=AccomodationType.objects.create(name='Executive Room',
			description="Modern designed room with great entertainment options,with access to exclusive Peace Hotel Club privileges.",
			capacity='2',
			price='130')
	
def populate_rooms(apps,schema_editor):
	Branch = apps.get_model('reservations','Branch')
	b1=Branch.objects.get(pk=1)
	AccomodationType = apps.get_model('reservations','AccomodationType')
	dlxroom = AccomodationType.objects.get(pk=1)
	stdroom = AccomodationType.objects.get(pk=1)
	Room = apps.get_model('reservations','Accomodation')
	r1 = Room.objects.create(branch_id=b1,accomodation_type=dlxroom,description='RoomOne',vacant=True,room_number='room1')
	r2 = Room.objects.create(branch_id=b1,accomodation_type=stdroom,description='RoomTwo',vacant=True,room_number='room2')

def populate_halls(apps,schema_editor):
	Branch = apps.get_model('reservations','Branch')
	b1=Branch.objects.get(pk=1)
	ConferenceHall = apps.get_model('reservations','ConferenceHall')
	
	h1 = ConferenceHall.objects.create(branch_id=b1,name="Hakaba VIP Room",theater_cap=35,classroom_cap=18,ushape_cap=18,reception_cap=25)
	h2 = ConferenceHall.objects.create(branch_id=b1,name="Daalo Banquet Hall",theater_cap=200,classroom_cap=40,ushape_cap=60,reception_cap=220)
	h3 = ConferenceHall.objects.create(branch_id=b1,name="Ogo Villa 1 Room",theater_cap=30,classroom_cap=15,ushape_cap=20,reception_cap=25)
	h4 = ConferenceHall.objects.create(branch_id=b1,name="Gezira VIP Room",theater_cap=290,classroom_cap=180,ushape_cap=100,reception_cap=330)
	h5 = ConferenceHall.objects.create(branch_id=b1,name="Jilib Room",theater_cap=150,classroom_cap=80,ushape_cap=55,reception_cap=180)
	h6 = ConferenceHall.objects.create(branch_id=b1,name="Golis Room",theater_cap=160,classroom_cap=100,ushape_cap=60,reception_cap=190)
	h7 = ConferenceHall.objects.create(branch_id=b1,name="Camel Room",theater_cap=70,classroom_cap=30,ushape_cap=25,reception_cap=50)
	h8 = ConferenceHall.objects.create(branch_id=b1,name="Damo Villa 2 Room",theater_cap=25,classroom_cap=12,ushape_cap=18,reception_cap=20)
	h9 = ConferenceHall.objects.create(branch_id=b1,name="Warsheikh Villa 2 Room",theater_cap=15,classroom_cap=8,ushape_cap=8,reception_cap=15)
	h10 = ConferenceHall.objects.create(branch_id=b1,name="Hargeisa OB 3 Room",theater_cap=10,classroom_cap=6,ushape_cap=8,reception_cap=12)
	h11 = ConferenceHall.objects.create(branch_id=b1,name="Lag Badana Room",theater_cap=15,classroom_cap=8,ushape_cap=10,reception_cap=12)

def populate_security_services(apps,schema_editor):
	SecurityService = apps.get_model('reservations','SecurityService')
	s1 = SecurityService.objects.create(description="Site-based security",name="Ground Security-Site-based")
	s2 = SecurityService.objects.create(description="Marine Security",name="Ship and Harbour Security")
	s3 = SecurityService.objects.create(description="Operations Room",name="Risk consulting services")
	s4 = SecurityService.objects.create(description="Operations Room",name="Crisis Management & Crisis Response")
	



class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0001_initial'),
    ]

    operations = [
    	migrations.RunPython(populate_branches),
    	migrations.RunPython(populate_room_types),
    	migrations.RunPython(populate_rooms),
    	migrations.RunPython(populate_halls),
    	migrations.RunPython(populate_security_services),
    ]