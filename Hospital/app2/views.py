import datetime
from pyexpat.errors import messages
from venv import logger
from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout as auth_logout
from django.core.mail import send_mail
from django.contrib import messages 
from django.conf import settings
from app2.models import addstaff,userr,scheduled,Patientt,Slot,Medicine,Medication,Room
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta

# Create your views here.
def signup(request):
    if request.method == 'POST':
        firstname = request.POST['name']
        lastname = request.POST['lname']
        username = request.POST['uname']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username= username):
            messages.error(request,"Username already exits! Please try some other user name")
            return redirect('home')

        if User.objects.filter(email = email):
            messages.error(request,"mail already registered")
            return redirect('home')
        
        if len(username)>10:
            messages.error(request,"Username must be under 10 characters")
        
        user = User.objects.create_user(username=username,first_name = firstname,last_name = lastname, email=email, password=password)
        user.save()

        z = Patientt(username=username,first_name = firstname,last_name = lastname, email=email)
        print("helloo")
        z.save()
        
        print("user created successfully")
        subject = "Welcome to Bharat Hospital ❤️"
        message = "Hello" + user.first_name + "!\n" + "Thank u for visiting our website \n Please feel free to reach out to us at +919428235545 or reply to this email if you have any questions or require further assistance. We look forward to providing you with excellent care and support."
        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)
        return redirect('home')
    else:
        return render(request, 'signup.html')



def add_staff_view(request):
    if request.method == 'POST':
        type = request.POST.get('type')
        firstname = request.POST.get('fname')
        lastname = request.POST.get('lname')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        number = request.POST.get('number')
        department = request.POST.get('department')
        staff_py = True

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists! Please try some other username")
            return redirect('add_staff_view')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered")
            return redirect('add_staff_view')

        user = User.objects.create_user(username=username, is_staff=staff_py, first_name=firstname, last_name=lastname, email=email, password=password)
        user.save()

        y = addstaff(
            username=username,
            fname=firstname,
            lname=lastname,
            email=email,
            department=department,
            number=number,
            type=type,
            password=password,
            gender='',
            medical_license='',
            specialization='',
            experience=0,  # default value
            medical_school='',
            graduation_year=0,  # default value
            country='',
            city='',
            languages='',
            publications='',
            awards='',
            hobbies=''
        )
        y.save()

        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        password_reset_url = request.build_absolute_uri(reverse('password_reset_confirm', kwargs={'uidb64': uid, 'token': token}))

        subject = "Welcome to Bharat Hospital ❤️"
        message = render_to_string('welcome_email.html', {
            'first_name': y.fname,
            'type': y.type,
            'password_reset_url': password_reset_url,
        })

        from_email = settings.EMAIL_HOST_USER
        to_list = [user.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect('home')
    else:
        return render(request, 'addstaff.html')



    
def logout_view(request):
    auth_logout(request)
    return redirect('home')
    
    

def loginform(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = request.POST.get('uname')
        print(request.method)
        print(email)
        print(password)
        
        user = authenticate(request, email=email, password=password,username = username)
        print(user)
        if user is not None:
            login(request, user)
            return redirect('home')  
        else:
            messages.error(request, 'Invalid email or password')
            return render(request, 'signup.html')
    else:
        return render(request, 'signup.html')
    

def view_profile(request, staff_type):
    if request.user.is_superuser:
        if staff_type == 'staff':
            staff_members = addstaff.objects.all()
        else:
            staff_members = addstaff.objects.filter(type=staff_type)
        return render(request, 'view_profile.html', {'staff_members': staff_members, 'staff_type': staff_type})
    else:
        return redirect('home')
    


def get_doctors_by_department(request):
    if request.method == 'GET' and 'department' in request.GET:
        department = request.GET['department']
        doctors = addstaff.objects.filter(department=department).values('id', 'fname', 'lname')
        doctor_list = list(doctors)
        return JsonResponse(doctor_list, safe=False)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def appointment(request):
    if request.method == 'POST':
        department = request.POST.get('department')
        doctor_id = request.POST.get('doctor')
        date = request.POST.get('date')
        time_slot = request.POST.get('time_slot')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        symptoms = request.POST.get('symptoms')

        # Fetch doctor information
        try:
            doctor = addstaff.objects.get(id=doctor_id)
        except addstaff.DoesNotExist:
            return JsonResponse({'error': 'Doctor not found'}, status=400)

        # Check if the selected time slot is already booked
        if scheduled.objects.filter(doctor=doctor, date=date, time_slot=time_slot).exists():
            return JsonResponse({'error': 'Time slot already booked'}, status=400)

        # Save the appointment
        sch = scheduled(
            department=department,
            doctor=doctor,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            symptoms=symptoms,
            doctoremail=doctor.email,
            date=date,
            time_slot=time_slot
        )
        sch.save()

        # Send email to the patient
        patient_subject = "Appointment Confirmation"
        patient_message = f"Dear {first_name} {last_name},\n\nYour appointment with Dr. {doctor.fname} {doctor.lname} in the {department} department has been scheduled successfully.\n\nDetails:\nDate: {date}\nTime: {time_slot}\nSymptoms: {symptoms}\nContact: {phone}\n\nThank you!"
        from_email = settings.EMAIL_HOST_USER
        send_mail(patient_subject, patient_message, from_email, [email], fail_silently=False)

        # Send email to the doctor
        doctor_subject = "New Appointment"
        doctor_message = f"Dear Dr. {doctor.fname} {doctor.lname},\n\nYou have a new appointment scheduled.\n\nPatient Details:\nName: {first_name} {last_name}\nDate: {date}\nTime: {time_slot}\nEmail: {email}\nPhone: {phone}\nSymptoms: {symptoms}\n\nThank you!"
        send_mail(doctor_subject, doctor_message, from_email, [doctor.email], fail_silently=False)

        return JsonResponse({'success': 'Appointment scheduled successfully'}, status=200)
    else:
        return render(request, 'appointment.html')
    
# def view_appointments(request):
#     if request.user.is_authenticated:
#         # Fetch the logged-in user's email
#         doctor_email = request.user.email
        
#         try:
#             # Get the doctor object using the logged-in user's email
#             doctor = addstaff.objects.get(email=doctor_email)
#         except addstaff.DoesNotExist:
#             return render(request, 'no_appointments.html', {'message': 'You are not registered as a doctor.'})
        
#         # Fetch appointments for the logged-in doctor
#         appointments = scheduled.objects.filter(doctor=doctor)
        
#         return render(request, 'view_appointments.html', {'appointments': appointments})
#     else:
#         return redirect('login')



def view_appointments(request):
    if request.user.is_authenticated:
        doctor_email = request.user.email
        
        try:
            doctor = addstaff.objects.get(email=doctor_email)
        except addstaff.DoesNotExist:
            return render(request, 'view_appointments.html', {'message': 'You are not registered as a doctor.'})
        
        appointments = scheduled.objects.filter(doctor=doctor, done=False)
        return render(request, 'view_appointments.html', {'appointments': appointments})
    else:
        return redirect('login')

@csrf_exempt
def mark_appointment_done(request):
    if request.method == 'POST':
        appointment_id = request.POST.get('appointment_id')
        try:
            appointment = scheduled.objects.get(id=appointment_id)
            appointment.done = True
            appointment.save()
            return JsonResponse({'status': 'success'})
        except scheduled.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Appointment not found'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})

def view_appointment_history(request):
    if request.user.is_authenticated:
        doctor_email = request.user.email
        
        try:
            doctor = addstaff.objects.get(email=doctor_email)
        except addstaff.DoesNotExist:
            return render(request, 'no_appointments.html', {'message': 'You are not registered as a doctor.'})
        
        done_appointments = scheduled.objects.filter(doctor=doctor, done=True)
        return render(request, 'view_appointment_history.html', {'appointments': done_appointments})
    else:
        return redirect('login')

@login_required
def update_staff_details(request):
    try:
        staff_member = addstaff.objects.get(username=request.user.username)
    except addstaff.DoesNotExist:
        messages.error(request, "Staff member not found.")
        return redirect('home')

    if request.method == 'POST':
        # Update fields in addstaff model
        staff_member.gender = request.POST.get('gender')
        staff_member.medical_license = request.POST.get('medical_license')
        staff_member.specialization = request.POST.get('specialization')
        staff_member.experience = request.POST.get('experience')
        staff_member.medical_school = request.POST.get('medical_school')
        staff_member.graduation_year = request.POST.get('graduation_year')
        staff_member.country = request.POST.get('country')
        staff_member.city = request.POST.get('city')
        staff_member.languages = request.POST.get('languages')
        staff_member.publications = request.POST.get('publications')
        staff_member.awards = request.POST.get('awards')
        staff_member.hobbies = request.POST.get('hobbies')
        staff_member.capacity = request.POST.get('capacity')

        # Update availability in addstaff model
        availability = {}
        for day in ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]:
            availability[day] = request.POST.getlist(f'availability_{day}')
        staff_member.availability = availability

        staff_member.save()  # Save changes to addstaff model

        # Update or create slots based on availability
        for day, slots in availability.items():
            Slot.objects.filter(doctor=staff_member, day=day).delete()  # Clear existing slots for the day
            for slot in slots:
                Slot.objects.create(doctor=staff_member, day=day, time_slot=slot, capacity=staff_member.capacity)

        messages.success(request, "Staff details updated successfully.")
        return redirect('home')
    else:
        # Pre-fill form with existing staff member details
        return render(request, 'update_staff_details.html', {
            'staff': staff_member,
            'days': ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
            'hours': list(range(9, 18))
        })





from django.http import JsonResponse
from datetime import datetime, timedelta
from .models import addstaff, Slot, scheduled

def get_available_time_slots(request):
    doctor_id = request.GET.get('doctor')
    date = request.GET.get('date')
    
    if not doctor_id or not date:
        return JsonResponse({'error': 'Doctor and date are required'}, status=400)

    try:
        doctor = addstaff.objects.get(id=doctor_id)
    except addstaff.DoesNotExist:
        return JsonResponse({'error': 'Doctor not found'}, status=400)

    day_name = datetime.strptime(date, '%Y-%m-%d').strftime('%A')

    try:
        slots = Slot.objects.filter(doctor=doctor, day=day_name)
        if not slots.exists():
            return JsonResponse({'error': 'No slots available for the selected day'}, status=400)
    except Slot.MultipleObjectsReturned:
        return JsonResponse({'error': 'Multiple slots returned for the selected day. Contact support.'}, status=400)
    
    booked_slots = scheduled.objects.filter(doctor=doctor, date=date).values_list('time_slot', flat=True)

    available_slots = []
    for slot in slots:
        capacity = slot.capacity
        interval = 60 // capacity

        start_time = datetime.strptime(f"{slot.time_slot.zfill(2)}:00", '%H:%M')
        end_time = start_time + timedelta(minutes=interval)
        
        while start_time < end_time:
            for _ in range(capacity):
                slot_start = start_time.strftime('%H:%M')
                slot_end = (start_time + timedelta(minutes=interval)).strftime('%H:%M')
                available_slots.append(f"{slot_start} - {slot_end}")
                start_time += timedelta(minutes=interval)
    
    return JsonResponse({
        'available_slots': available_slots,
        'booked_slots': list(booked_slots)
    }, safe=False)

@login_required
def patient_details(request):
    try:
        patient = Patientt.objects.get(username=request.user.username)
    except Patientt.DoesNotExist:
        messages.error(request, "Patient member not found.")
        return redirect('home')
    
    if request.method == 'POST':
        # Update patient information
        patient.first_name = request.POST['first_name']
        patient.last_name = request.POST['last_name']
        patient.blood_pressure = request.POST['blood_pressure']
        patient.sugar_level = request.POST['sugar_level']
        patient.blood_group = request.POST['blood_group']
        patient.gender = request.POST['gender']
        patient.phone_number = request.POST['phone_number']
        patient.weight = request.POST['weight']
        patient.height = request.POST['height']
        patient.smoking_status = request.POST['smoking_status']
        patient.alcohol_use = request.POST['alcohol_use']
        patient.has_insurance = request.POST['has_insurance']
        patient.save()
        return redirect('home')

    return render(request, 'patient_form.html', {'patient': patient})



# # Example view where you handle saving slots for a doctor
# @csrf_exempt
# def save_slots_for_doctor(request):
#     if request.method == 'POST':
#         doctor_id = request.POST.get('doctor_id')
#         time_slots = request.POST.getlist('time_slots')
#         capacity = request.POST.get('capacity')

#         # Retrieve doctor object
#         try:
#             doctor = addstaff.objects.get(id=doctor_id)
#         except addstaff.DoesNotExist:
#             return JsonResponse({'error': 'Doctor not found'}, status=404)

#         # Clear existing slots for this doctor
#         Slot.objects.filter(doctor=doctor).delete()

#         # Save new slots
#         for slot in time_slots:
#             day, hour = slot.split('-')
#             Slot.objects.create(doctor=doctor, day=day, time_slot=f"{hour}:00", capacity=capacity)

#         return JsonResponse({'success': 'Slots saved successfully'})
#     else:
#         return JsonResponse({'error': 'Invalid request method'}, status=400)

# def get_doctor_schedule(request):
#     if request.method == 'GET':
#         doctor_id = request.GET.get('doctor_id')

#         # Fetch the doctor
#         try:
#             doctor = addstaff.objects.get(id=doctor_id)
#         except addstaff.DoesNotExist:
#             return JsonResponse({'error': 'Doctor not found'}, status=404)

#         # Fetch available dates with slots for the doctor
#         available_dates = Slot.objects.filter(doctor=doctor).values_list('date', flat=True).distinct()

#         # Convert dates to string format (if needed)
#         available_dates = [str(date) for date in available_dates if date >= date.today()]

#         return JsonResponse({'available_dates': available_dates}, safe=False)

#     return JsonResponse({'error': 'Method not allowed'}, status=405)

# def get_slots_by_doctor(request):
#     doctor_id = request.GET.get('doctor_id')
#     if doctor_id:
#         slots = Slot.objects.filter(doctor_id=doctor_id).values_list('day', flat=True).distinct()
#         available_dates = list(slots)
#         return JsonResponse({'dates': available_dates})
#     else:
#         return JsonResponse({}, status=400)






# def add_medicine(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         price = request.POST.get('price')
#         quantity = request.POST.get('quantity')
#         category = request.POST.get('category')

#         if name and price and quantity and category:
#             medicine = Medicine(
#                 name=name,
#                 price=price,
#                 quantity=quantity,
#                 category=category
#             )
#             medicine.save()
#             return redirect('add_medicine')  # Redirect to the same form or another page

#     return render(request, 'medicine.html')



def add_medicine(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        category = request.POST.get('category')

        if name and price and quantity and category:
            medicine = Medicine(
                name=name,
                price=price,
                quantity=quantity,
                category=category
            )
            medicine.save()
            return redirect('add_medicine')  # Redirect to the same form or another page

    medicines = Medicine.objects.all()
    return render(request, 'medicine.html', {'medicines': medicines})

def update_medicine(request, medicine_id):
    if request.method == 'POST':
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        medicine = Medicine.objects.get(id=medicine_id)

        if price and quantity:
            medicine.price = price
            medicine.quantity = quantity
            medicine.save()
            return redirect('add_medicine')  # Redirect to the same form or another page
    return redirect('add_medicine')




# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from django.template.loader import render_to_string
# from django.http import HttpResponse
# from django.core.mail import EmailMessage
# from xhtml2pdf import pisa
# from .models import Patientt, Medicine, Medication, scheduled

# @login_required
# def view_patient_profile(request, email, appointment_id):
#     patient = get_object_or_404(Patientt, email=email)
#     medicines = Medicine.objects.all()
#     schedule = get_object_or_404(scheduled, id=appointment_id, email=patient.email)

#     # Fetch medications for the current patient and appointment date
#     medications = Medication.objects.filter(patient=patient, schedule_date=schedule.date)

#     if request.method == 'POST':
#         description_data = request.POST.getlist('description')
#         medicine_data = request.POST.getlist('medicine')
#         quantity_data = request.POST.getlist('quantity')
#         total_price_data = request.POST.getlist('total_price')
#         time_schedule_data = request.POST.getlist('time_schedule')

#         for description, medicine_id, quantity, total_price, time_schedule in zip(description_data, medicine_data, quantity_data, total_price_data, time_schedule_data):
#             if description and medicine_id and quantity and total_price and time_schedule:
#                 # Fetch the medicine and reduce its quantity
#                 medicine = get_object_or_404(Medicine, id=medicine_id)
#                 if medicine.quantity >= int(quantity):
#                     medicine.quantity -= int(quantity)
#                     medicine.save()
#                 else:
#                     messages.error(request, f"Not enough stock for {medicine.name}. Available quantity: {medicine.quantity}")
#                     return redirect('view_patient_profile', email=email, appointment_id=appointment_id)

#                 # Save the medication record
#                 medication = Medication(
#                     description=description,
#                     medicine=medicine,  # Update: use the medicine object directly
#                     quantity=quantity,
#                     total_price=float(total_price),
#                     patient=patient,
#                     doctor=schedule.doctor,
#                     schedule_date=schedule.date,
#                     time_schedule=time_schedule
#                 )
#                 medication.save()

#         # Mark the appointment as done
#         schedule.done = True
#         schedule.save()

        # # Generate PDF and send it via email
        # try:
        #     # Render the HTML template to generate PDF
        #     context = {
        #         'patient': patient,
        #         'medications': medications,
        #         'appointments': [schedule],  # Include only the current appointment
        #     }
        #     html_content = render_to_string('medication_report_pdf.html', context)

        #     # Generate PDF
        #     response = HttpResponse(content_type='application/pdf')
        #     response['Content-Disposition'] = f'attachment; filename="medication_report_{patient.username}.pdf"'
        #     pisa_status = pisa.CreatePDF(html_content, dest=response)

        #     # Check if PDF generation was successful
        #     if pisa_status.err:
        #         messages.error(request, 'PDF generation error.')
        #     else:
        #         # Send the PDF as an email attachment to the patient
        #         subject = 'Medication Report'
        #         message = 'Please find your medication report attached.'
        #         email_message = EmailMessage(subject, message, to=[patient.email])
        #         email_message.attach(f'medication_report_{patient.username}.pdf', response.content, 'application/pdf')
        #         email_message.send()

        #         # Optionally, add a success message for email
        #         messages.success(request, 'Medication report sent successfully via email.')

        # except Exception as e:
        #     messages.error(request, f"An error occurred while generating the medication report: {e}")

#         messages.success(request, "Medications added successfully.")
#         return redirect('home')

#     return render(request, 'view_patient_profile.html', {
#         'patient': patient,
#         'medicines': medicines,
#         'appointment_date': schedule.date if schedule else None,
#         'medications': medications  # Pass medications to pre-fill in the template
#     })

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import EmailMessage
from xhtml2pdf import pisa
from .models import Patientt, Medicine, Medication, scheduled, Room

@login_required
def view_patient_profile(request, email, appointment_id):
    patient = get_object_or_404(Patientt, email=email)
    medicines = Medicine.objects.all()
    rooms = Room.objects.all()
    schedule = get_object_or_404(scheduled, id=appointment_id, email=patient.email)

    medications = Medication.objects.filter(patient=patient, schedule_date=schedule.date)

    if request.method == 'POST':
        description_data = request.POST.getlist('description')
        medicine_data = request.POST.getlist('medicine')
        quantity_data = request.POST.getlist('quantity')
        total_price_data = request.POST.getlist('total_price')
        time_schedule_data = request.POST.getlist('time_schedule')
        admit_data = request.POST.getlist('admit')
        room_id_data = request.POST.getlist('room')

        for description, medicine_id, quantity, total_price, time_schedule, admit, room_id in zip(description_data, medicine_data, quantity_data, total_price_data, time_schedule_data, admit_data, room_id_data):
            if description and medicine_id and quantity and total_price and time_schedule:
                medicine = get_object_or_404(Medicine, id=medicine_id)
                if medicine.quantity >= int(quantity):
                    medicine.quantity -= int(quantity)
                    medicine.save()
                else:
                    messages.error(request, f"Not enough stock for {medicine.name}. Available quantity: {medicine.quantity}")
                    return redirect('view_patient_profile', email=email, appointment_id=appointment_id)

                room = None
                room_type = ""
                room_price = None
                if admit == 'yes' and room_id:
                    room = get_object_or_404(Room, id=room_id)
                    if room.quantity > 0:
                        room.quantity -= 1
                        room.save()
                        room_type = room.get_type_of_room_display()
                        room_price = room.price
                    else:
                        messages.error(request, f"No available rooms of type {room.get_type_of_room_display()}.")
                        return redirect('view_patient_profile', email=email, appointment_id=appointment_id)

                medication = Medication(
                    description=description,
                    medicine=medicine,
                    quantity=quantity,
                    total_price=float(total_price),
                    patient=patient,
                    doctor=schedule.doctor,
                    schedule_date=schedule.date,
                    time_schedule=time_schedule,
                    room=room,
                    room_type=room_type,
                    room_price=room_price
                )
                medication.save()

        schedule.done = True
        schedule.save()

        # Generate PDF and send it via email (same as before)
        
        # Generate PDF and send it via email
        try:
            # Render the HTML template to generate PDF
            context = {
                'patient': patient,
                'medications': medications,
                'appointments': [schedule],  # Include only the current appointment
            }
            html_content = render_to_string('medication_report_pdf.html', context)

            # Generate PDF
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="medication_report_{patient.username}.pdf"'
            pisa_status = pisa.CreatePDF(html_content, dest=response)

            # Check if PDF generation was successful
            if pisa_status.err:
                messages.error(request, 'PDF generation error.')
            else:
                # Send the PDF as an email attachment to the patient
                subject = 'Medication Report'
                message = 'Please find your medication report attached.'
                email_message = EmailMessage(subject, message, to=[patient.email])
                email_message.attach(f'medication_report_{patient.username}.pdf', response.content, 'application/pdf')
                email_message.send()

                # Optionally, add a success message for email
                messages.success(request, 'Medication report sent successfully via email.')

        except Exception as e:
            messages.error(request, f"An error occurred while generating the medication report: {e}")

        messages.success(request, "Medications added successfully.")
        return redirect('home')

    return render(request, 'view_patient_profile.html', {
        'patient': patient,
        'medicines': medicines,
        'rooms': rooms,  # Pass rooms to template
        'appointment_date': schedule.date if schedule else None,
        'medications': medications
    })

from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Patientt, Medication

@login_required
def previous_appointments(request, email):
    patient = get_object_or_404(Patientt, email=email)

    # Fetch previous medications
    previous_medications = Medication.objects.filter(patient=patient).order_by('-schedule_date')
    previous_medications_by_date = {}
    for medication in previous_medications:
        date = medication.schedule_date
        if date not in previous_medications_by_date:
            previous_medications_by_date[date] = []
        previous_medications_by_date[date].append(medication)

    return render(request, 'previous_appointments.html', {
        'patient': patient,
        'previous_medications_by_date': previous_medications_by_date
    })




# # views.py
# from .models import scheduled, addstaff  # Import the addstaff model

# @login_required
# def medication_report(request):
#     try:
#         # Fetch the logged-in user
#         logged_in_user = request.user
#         print("Logged-in user: ID =", logged_in_user.id, ", Username =", logged_in_user.username)

#         # Fetch Patientt using the logged-in user's username
#         patient = Patientt.objects.get(username=logged_in_user.username)
        
#         # Print patient ID and username
#         print("Patient found: ID =", patient.id, ", Username =", patient.username)
        
#         # Get the Medication instances related to this patient
#         medications = Medication.objects.filter(patient=patient)
        
#         # Debug: Print details of medications
#         print(f"Medications found: {len(medications)}")
#         for medication in medications:
#             print(f"Medication ID: {medication.id}, Description: {medication.description}, Doctor: {medication.doctor.fname} {medication.doctor.lname}")

#         # Fetch scheduled appointments for the patient
#         appointments = scheduled.objects.filter(email=patient.email)  # Assuming email is used to identify appointments
        
#         # Debug: Print details of appointments
#         print(f"Appointments found: {len(appointments)}")
#         for appointment in appointments:
#             print(f"Appointment ID: {appointment.id}, Date: {appointment.date}, Time Slot: {appointment.time_slot}, Doctor: {appointment.doctor.fname} {appointment.doctor.lname}")

#         # Pass the data to the template
#         return render(request, 'medication_report.html', {
#             'patient': patient,
#             'medications': medications,
#             'appointments': appointments,
#         })
#     except Patientt.DoesNotExist:
#         print("Patientt does not exist for username:", logged_in_user.username)
#         messages.error(request, "You are not registered as a patient.")
#         return redirect('home')



@login_required
def medication_report(request):
    try:
        # Fetch the logged-in user
        logged_in_user = request.user
        logger.info(f"Logged-in user: ID = {logged_in_user.id}, Username = {logged_in_user.username}")

        # Fetch Patientt using the logged-in user's username
        patient = Patientt.objects.get(username=logged_in_user.username)
        
        # Log patient ID and username
        logger.info(f"Patient found: ID = {patient.id}, Username = {patient.username}")
        
        # Get the Medication instances related to this patient
        medications = Medication.objects.filter(patient=patient).select_related('doctor')
        
        # Log details of medications
        logger.info(f"Medications found: {medications.count()}")
        for medication in medications:
            logger.info(f"Medication ID: {medication.id}, Description: {medication.description}, Doctor: {medication.doctor.fname} {medication.doctor.lname}")

        # Fetch scheduled appointments for the patient
        appointments = scheduled.objects.filter(email=patient.email).select_related('doctor')  # Assuming email is used to identify appointments
        
        # Log details of appointments
        logger.info(f"Appointments found: {appointments.count()}")
        for appointment in appointments:
            logger.info(f"Appointment ID: {appointment.id}, Date: {appointment.date}, Time Slot: {appointment.time_slot}, Doctor: {appointment.doctor.fname} {appointment.doctor.lname}")

        # Pass the data to the template
        return render(request, 'medication_report.html', {
            'patient': patient,
            'medications': medications,
            'appointments': appointments,
        })
    except Patientt.DoesNotExist:
        logger.error(f"Patientt does not exist for username: {logged_in_user.username}")
        messages.error(request, "You are not registered as a patient.")
        return redirect('home')
    except Exception as e:
        logger.exception("An error occurred while generating the medication report.")
        messages.error(request, "An error occurred while generating the medication report.")
        return redirect('home')


from django.template.loader import render_to_string
from django.http import HttpResponse
from django.core.mail import EmailMessage
from xhtml2pdf import pisa

@login_required
def medication_report_pdf(request):
    try:
        # Fetch the logged-in user
        logged_in_user = request.user

        # Fetch Patient using the logged-in user's username
        patient = Patientt.objects.get(username=logged_in_user.username)

        # Get the Medication instances related to this patient
        medications = Medication.objects.filter(patient=patient).select_related('doctor')

        # Fetch scheduled appointments for the patient
        appointments = scheduled.objects.filter(email=patient.email).select_related('doctor')

        # Render the HTML template to generate PDF
        context = {
            'patient': patient,
            'medications': medications,
            'appointments': appointments,
        }
        html_content = render_to_string('medication_report_pdf.html', context)

        # Generate PDF
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="medication_report_{patient.username}.pdf"'
        pisa_status = pisa.CreatePDF(html_content, dest=response)

        # Check if PDF generation was successful
        if pisa_status.err:
            return HttpResponse('PDF generation error', status=500)

        # Send the PDF as an email attachment to the patient
        subject = 'Medication Report'
        message = 'Please find your medication report attached.'
        email = EmailMessage(subject, message, to=[patient.email])
        email.attach(f'medication_report_{patient.username}.pdf', response.content, 'application/pdf')
        email.send()

        # Return the PDF as HTTP response (optional)
        return response

    except Patientt.DoesNotExist:
        messages.error(request, "You are not registered as a patient.")
        return redirect('home')
    except Exception as e:
        messages.error(request, "An error occurred while generating the medication report.")
        return redirect('home')
    




def add_room(request):
    if request.method == 'POST':
        type_of_room = request.POST.get('type_of_room')
        price = request.POST.get('price')
        quantity = request.POST.get('quantity')
        
        if type_of_room and price and quantity:
            try:
                price = float(price)
                quantity = int(quantity)
                room = Room(type_of_room=type_of_room, price=price, quantity=quantity)
                room.save()
                return redirect('add_room')  # Redirect to avoid form resubmission on page refresh
            except ValueError:
                # Handle the error if conversion to float or int fails
                pass
    
    rooms = Room.objects.all()  # Retrieve all rooms for display
    return render(request, 'add_room.html', {'rooms': rooms})
