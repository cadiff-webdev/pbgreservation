from django.contrib import admin
from .models import *

admin.site.register(Branch)
admin.site.register(Pbguser)
admin.site.register(Accomodation)
admin.site.register(AccomodationType)
admin.site.register(ConferenceHall)
admin.site.register(SecurityService)
admin.site.register(AccomodationReservation)

