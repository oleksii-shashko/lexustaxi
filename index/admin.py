from django.contrib import admin
from .models import Car, Client, Distance, Address, Request


admin.site.register(Car)
admin.site.register(Client)
admin.site.register(Distance)
admin.site.register(Address)
admin.site.register(Request)