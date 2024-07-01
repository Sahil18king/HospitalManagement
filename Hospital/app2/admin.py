from django.contrib import admin
from .models import userr,addstaff,scheduled,Patientt,Slot,Medicine,Medication,Room
# Register your models here.

admin.site.register(Patientt)
admin.site.register(addstaff)
admin.site.register(scheduled)
admin.site.register(Slot)
admin.site.register(Medicine)
admin.site.register(Medication)
admin.site.register(Room)

