from django.shortcuts import render, HttpResponse, get_object_or_404
from django.core.paginator import Paginator
from medicine.models import TimeChronicDiseaseMedication, ChronicDisease, Treatment, ChronicDiseaseMedication
from services.forms import ProfileForm
from staff.forms import MedicalStaffForm, UserDjangoForm, ScheduleForm, AssistantStaffForm
from staff.models import MedicalStaffChronicDisease, MedicalStaff, Schedule, AssistantStaff, \
    AssistantStaffChronicDisease


# Create your views here.
def loadBase(request):
    return render(request, 'base.html')


""" chronic_disease = TimeChronicDiseaseMedication.objects.all()
    paginator = Paginator(chronic_disease, 4)
    page = request.GET.get('page')
    chronic_disease_objects = paginator.get_page(page)"""


def register_medical_staff(request):
    chronic_diseases = ChronicDisease.objects.all()
    time_chronic_disease_medications = TimeChronicDiseaseMedication.objects.all()
    treatments = ChronicDiseaseMedication.objects.all()
    if request.method == 'POST':
        medical_staff = MedicalStaffForm(request.POST)
        medical_profile = ProfileForm(request.POST)
        medical_user = UserDjangoForm(request.POST)
        if medical_staff.is_valid() and medical_profile.is_valid() and medical_user.is_valid():
            if medical_user.cleaned_data['password'] == medical_user.cleaned_data['confirm_password']:
                user = medical_user.save(commit=False)
                user.set_password(medical_user.cleaned_data['password'])
                user.is_superuser = True
                user.save()
                profile = medical_profile.save()
                account_medical_staff = medical_staff.save(commit=False)
                account_medical_staff.user = user
                account_medical_staff.profile = profile
                account_medical_staff.save()
                medical_staff.save_m2m()
                # save chronic disease for medical staff
                time_chronic_disease_medication_ids = request.POST.getlist('time_chronic_disease_medication_ids')
                get__medical_staff = medical_user.cleaned_data['username']
                get_medical_staff = MedicalStaff.objects.get(user__username=get__medical_staff)
                for time_chronic_disease_medication_id in time_chronic_disease_medication_ids:
                    time_chronic_disease_medication = TimeChronicDiseaseMedication.objects.get(
                        time_id=time_chronic_disease_medication_id)
                    save_medical_staff_chronic_disease = (MedicalStaffChronicDisease.objects.create
                                                          (medical_disease=get_medical_staff,
                                                           chronic_disease=time_chronic_disease_medication))
                return HttpResponse("save")
            else:
                return HttpResponse("Password does not match")
        else:
            return HttpResponse(f"{medical_staff.errors} {medical_profile.errors} {medical_user.errors}")
    else:
        medical_staff = MedicalStaffForm()
        medical_profile = ProfileForm()
        medical_user = UserDjangoForm()
    return render(request, 'staff/register_medical_staff.html', {'medical_staff': medical_staff,
                                                                 'medical_profile': medical_profile,
                                                                 'medical_user': medical_user,
                                                                 'chronic_diseases': chronic_diseases,
                                                                 'time_chronic_disease_medications':
                                                                     time_chronic_disease_medications,
                                                                 'treatments': treatments})


def register_assistant_staff(request):
    chronic_diseases = ChronicDisease.objects.all()
    time_chronic_disease_medications = TimeChronicDiseaseMedication.objects.all()
    treatments = ChronicDiseaseMedication.objects.all()
    if request.method == 'POST':
        assistant_staff = AssistantStaffForm(request.POST)
        assistant_profile = ProfileForm(request.POST)
        assistant_user = UserDjangoForm(request.POST)
        if assistant_staff.is_valid() and assistant_profile.is_valid() and assistant_user.is_valid():
            if assistant_user.cleaned_data['password'] == assistant_user.cleaned_data['confirm_password']:
                profile = assistant_profile.save()
                save_assistant_user = assistant_user.save(commit=False)
                save_assistant_user.set_password(assistant_user.cleaned_data['password'])
                save_assistant_user.is_staff = True
                save_assistant_user.save()
                account_assistant_staff = assistant_staff.save(commit=False)
                account_assistant_staff.user = save_assistant_user
                account_assistant_staff.profile = profile
                account_assistant_staff.save()
                assistant_staff.save_m2m()
                # save chronic disease for medical staff
                time_chronic_disease_medication_ids = request.POST.getlist('time_chronic_disease_medication_ids')
                get__assistant_staff = assistant_user.cleaned_data['username']
                get_assistant_staff = AssistantStaff.objects.get(user__username=get__assistant_staff)
                for time_chronic_disease_medication_id in time_chronic_disease_medication_ids:
                    time_chronic_disease_medication = TimeChronicDiseaseMedication.objects.get(
                        time_id=time_chronic_disease_medication_id)
                    save_medical_staff_chronic_disease = (AssistantStaffChronicDisease.objects.create
                                                          (assistant_disease=get_assistant_staff,
                                                           chronic_disease=time_chronic_disease_medication))
                return HttpResponse("save")
            else:
                return HttpResponse("Password does not match")
    else:
        assistant_staff = AssistantStaffForm(request.POST)
        assistant_profile = ProfileForm(request.POST)
        assistant_user = UserDjangoForm(request.POST)
    return render(request, 'staff/register_assistant_staff.html', {'assistant_staff': assistant_staff,
                                                                   'assistant_profile': assistant_profile,
                                                                   'assistant_user': assistant_user,
                                                                   'chronic_diseases': chronic_diseases,
                                                                   'time_chronic_disease_medications':
                                                                       time_chronic_disease_medications,
                                                                   'treatments': treatments})


def add_schedule(request):
    if request.method == "POST":
        schedule = ScheduleForm(request.POST)
        if schedule.is_valid():
            schedule.save()
            return HttpResponse("Save")

    else:
        schedule = ScheduleForm()

    return render(request, 'staff/add_schedule.html', {'schedule': schedule})


def show_schedule(request):
    get_schedule = Schedule.objects.all()
    return render(request, 'staff/schedule.html', {'get_schedule': get_schedule})


def schedule_update(request, schedule_id):
    schedule = get_object_or_404(Schedule, schedule_id=schedule_id)
    if request.method == 'POST':
        form_update = ScheduleForm(request.POST, instance=schedule)
        if form_update.is_valid():
            form_update.save()
            return HttpResponse("Update success")
    else:
        form_update = ScheduleForm(instance=schedule)

    return render(request, 'staff/schedule_update.html', {'form_update': form_update})


def schedule_delete(request, schedule_id):
    schedule = get_object_or_404(Schedule, schedule_id=schedule_id)
    schedule.delete()
    get_schedule = Schedule.objects.all()
    return render(request, 'staff/schedule.html', {'get_schedule': get_schedule})
