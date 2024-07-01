import datetime
from django.db import models
from django.contrib.auth.models import User
import _datetime

# Create your models here.
class userr(models.Model):
    username= models.CharField(max_length=20)
    fname= models.CharField(max_length=20)
    lname= models.CharField(max_length=20)
    email= models.CharField(max_length=20)
    password= models.CharField(max_length=20)

class addstaff(models.Model):
    type= models.CharField(max_length=150)
    username= models.CharField(max_length=30)
    fname= models.CharField(max_length=20)
    lname= models.CharField(max_length=20)
    email= models.CharField(max_length=200)
    password= models.CharField(max_length=20)
    number= models.CharField(max_length=10)
    department= models.CharField(max_length=20)
    gender = models.CharField(max_length=10)
    medical_license = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    experience = models.IntegerField()
    medical_school = models.CharField(max_length=100)
    graduation_year = models.IntegerField()
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    languages = models.CharField(max_length=255)
    publications = models.TextField(null=True, blank=True)
    awards = models.TextField(null=True, blank=True)
    hobbies = models.TextField(null=True, blank=True)
    # submission_date = models.DateField()
    # submitted_registration = models.BooleanField(default=False)



class Patientt(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    blood_pressure = models.CharField(max_length=50, blank=True)
    sugar_level = models.CharField(max_length=50, blank=True)
    blood_group = models.CharField(max_length=10, blank=True)
    gender = models.CharField(max_length=10, blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    weight = models.CharField(max_length=10, blank=True)
    height = models.CharField(max_length=10, blank=True)
    smoking_status = models.CharField(max_length=20, blank=True)
    alcohol_use = models.CharField(max_length=20, blank=True)
    has_insurance = models.CharField(max_length=3, blank=True)






class scheduled(models.Model):
    department = models.CharField(max_length=20)
    doctor = models.ForeignKey(addstaff, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.CharField(max_length=50)
    phone = models.CharField(max_length=10)
    symptoms = models.CharField(max_length=200)
    doctoremail = models.CharField(max_length=50)
    date = models.DateField(null=True, blank=True)  # Allow null values
    time_slot = models.CharField(max_length=20, null=True, blank=True)  # Allow null values
    done = models.BooleanField(default=False)



    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.doctor} on {self.date} at {self.time_slot}"


class Slot(models.Model):
    doctor = models.ForeignKey('addstaff', on_delete=models.CASCADE)
    day = models.CharField(max_length=20)
    time_slot = models.CharField(max_length=20)
    capacity = models.IntegerField()

    def __str__(self):
        return f"{self.doctor.username} - {self.day} at {self.time_slot}"
    


class Medicine(models.Model):
    CATEGORY_CHOICES = [
        ('LIQUID', 'Liquid'),
        ('SOLID', 'Solid'),
        ('TUBE', 'Tube'),
        ('POWDER', 'Powder'),
    ]
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField()
    category = models.CharField(max_length=10, choices=CATEGORY_CHOICES)


    def __str__(self):
        return self.name
 
# class Medication(models.Model):
#     description = models.TextField()
#     medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
#     quantity = models.PositiveIntegerField()
#     total_price = models.DecimalField(max_digits=10, decimal_places=2)
#     patient = models.ForeignKey(Patientt, on_delete=models.CASCADE)
#     doctor = models.ForeignKey(addstaff, on_delete=models.CASCADE)
#     time_schedule = models.CharField(max_length=7)  # Example: "1-0-1"
#     schedule_date = models.DateField(default=datetime.date.today)

#     def __str__(self):
#         return self.description  # or whatever you want to display
    

from django.core.validators import MinValueValidator
from django.db import models
from django.contrib.auth.models import User

class Room(models.Model):
    ROOM_TYPES = [
        ('AC', 'AC Room'),
        ('Non-AC', 'Non-AC Room'),
        ('General', 'General Room'),
    ]
    
    type_of_room = models.CharField(max_length=10, choices=ROOM_TYPES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    
    @property
    def availability(self):
        return self.quantity > 0

    def decrement_quantity(self):
        if self.quantity > 0:
            self.quantity -= 1
            self.save()

    def __str__(self):
        return f"{self.get_type_of_room_display()} - {self.price} - {'Available' if self.availability else 'Not Available'}"

# Modify Medication model to include room foreign key
class Medication(models.Model):
    description = models.TextField()
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    patient = models.ForeignKey(Patientt, on_delete=models.CASCADE)
    doctor = models.ForeignKey(addstaff, on_delete=models.CASCADE)
    time_schedule = models.CharField(max_length=7)  # Example: "1-0-1"
    schedule_date = models.DateField(default=datetime.date.today)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True, blank=True)  # Add foreign key to Room
    room_type = models.CharField(max_length=30, blank=True)  # Store room type
    room_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)  # Store room price

    def __str__(self):
        return self.description