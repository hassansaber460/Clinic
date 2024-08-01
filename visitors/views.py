from django.db import transaction
from django.core.paginator import Paginator
from django.shortcuts import render, HttpResponse, get_object_or_404
from medicine.models import ChronicDisease, TimeChronicDiseaseMedication, ChronicDiseaseMedication
from services.forms import ProfileForm
from services.models import Profile, StartExamination
from visitors.forms import PatientForm, MedicalRapForm
from visitors.models import Patient, PatientChronicDisease, MedicalRap


# Create your views here.

def show_patient(request):
    get_patient = Patient.objects.all()
    paginator = Paginator(get_patient, 12)
    page = request.GET.get('page')
    patient_objects = paginator.get_page(page)
    return render(request, 'visitors/show_patient.html', {
        'patient_objects': patient_objects
    })


def show_all_medical_rap(request):
    medical_raps = MedicalRap.objects.all()
    paginator = Paginator(medical_raps, 12)
    page = request.GET.get('page')
    medical_rap_objects = paginator.get_page(page)
    return render(request, 'visitors/info_medical_rap.html', {
        'medical_rap_objects': medical_rap_objects
    })


def register_patient(request):
    chronic_diseases = ChronicDisease.objects.all()
    time_chronic_disease_medications = TimeChronicDiseaseMedication.objects.all()
    treatments = ChronicDiseaseMedication.objects.all()
    if request.method == 'POST':
        patient = PatientForm(request.POST)
        patient_profile = ProfileForm(request.POST)
        if patient.is_valid() and patient_profile.is_valid():
            save_profile_patient = patient_profile.save()
            save_patient = patient.save(commit=False)
            save_patient.profile = save_profile_patient
            save_patient.save()
            try:
                time_chronic_disease_medication_ids = request.POST.getlist('time_chronic_disease_medication_ids')
                if time_chronic_disease_medication_ids is not None:
                    get__patient = patient.cleaned_data['ssn']
                    get_patient = Patient.objects.get(ssn=get__patient)
                    for time_chronic_disease_medication_id in time_chronic_disease_medication_ids:
                        time_chronic_disease_medication = TimeChronicDiseaseMedication.objects.get(
                            time_id=time_chronic_disease_medication_id)
                        PatientChronicDisease.objects.create(patient=get_patient,
                                                             chronic_disease=time_chronic_disease_medication)
            except Exception as e:
                return HttpResponse(e)
            return HttpResponse("save")
        else:
            return HttpResponse(f'{patient.errors} {patient_profile.errors}')
    else:
        patient = PatientForm()
        patient_profile = ProfileForm()
    return render(request, 'visitors/register_patient.html', {'patient': patient,
                                                              'patient_profile': patient_profile,
                                                              'chronic_diseases': chronic_diseases,
                                                              'time_chronic_disease_medications':
                                                                  time_chronic_disease_medications,
                                                              'treatments': treatments})


def update_patient(request, patient_id):
    get_profile = Patient.objects.get(patient_id=patient_id)
    get__profile = get_profile.profile.profile_id
    patient = get_object_or_404(Patient, patient_id=patient_id)
    profile = get_object_or_404(Profile, profile_id=get__profile)
    if request.method == 'POST':
        patient_form_update = PatientForm(request.POST, instance=patient)
        profile_form_update = ProfileForm(request.POST, instance=profile)
        if patient_form_update.is_valid() and profile_form_update.is_valid():
            patient_form_update.save()
            profile_form_update.save()
            return HttpResponse("update success")
        else:
            return HttpResponse(f'{patient_form_update.errors} {profile_form_update.errors}')
    else:
        patient_form_update = PatientForm(instance=patient)
        profile_form_update = ProfileForm(instance=profile)
    return render(request, 'visitors/update_patient.html', {'patient_form_update': patient_form_update,
                                                            'profile_form_update': profile_form_update})


def delete_patient(request, patient_id):
    patient = get_object_or_404(Patient, patient_id=patient_id)
    with transaction.atomic():
        # حذف السجلات المرتبطة في PatientChronicDisease
        PatientChronicDisease.objects.filter(patient__patient_id=patient_id).delete()

        # حذف السجلات المرتبطة في StartExamination
        StartExamination.objects.filter(patient__patient_id=patient_id).delete()

        # حذف الملف الشخصي المرتبط بالمريض
        get_profile = patient.profile.profile_id
        Profile.objects.get(profile_id=get_profile).delete()

        # حذف المريض
        patient.delete()
    get_patient = Patient.objects.all()
    paginator = Paginator(get_patient, 15)
    page = request.GET.get('page')
    patient_objects = paginator.get_page(page)
    return render(request, 'visitors/show_patient.html', {
        'patient_objects': patient_objects
    })


def post_medical_rap(request):
    if request.method == 'POST':
        form_medical_rap = MedicalRapForm(request.POST)
        form_profile = ProfileForm(request.POST)
        if form_profile.is_valid() and form_medical_rap.is_valid():
            profile_medical_rap = form_profile.save()
            medical_rap = form_medical_rap.save(commit=False)
            medical_rap.profile = profile_medical_rap
            medical_rap.save()
            return HttpResponse("Save medical rap success")
        else:
            return HttpResponse(f"{form_medical_rap.errors} {form_profile.errors}")
    else:
        form_medical_rap = MedicalRapForm()
        form_profile = ProfileForm()
    return render(request, 'visitors/add_medical_rap.html', {
        'form_medical_rap': form_medical_rap, 'form_profile': form_profile
    })


def put_medical_rap(request, medicalRap_id):
    get_medical_rap = get_object_or_404(MedicalRap, medicalRap_id=medicalRap_id)
    get__medical_rap = MedicalRap.objects.get(medicalRap_id=medicalRap_id)
    profile = get_object_or_404(Profile, profile_id=get__medical_rap.profile.profile_id)
    if request.method == 'POST':
        form_medical_rap_update = MedicalRapForm(request.POST, instance=get_medical_rap)
        profile_form_update = ProfileForm(request.POST, instance=profile)
        if form_medical_rap_update.is_valid() and profile_form_update.is_valid():
            form_medical_rap_update.save()
            profile_form_update.save()
            return HttpResponse("update success")
        else:
            return HttpResponse(f'{form_medical_rap_update.errors} {profile_form_update.errors}')
    else:
        form_medical_rap_update = PatientForm(instance=get_medical_rap)
        profile_form_update = ProfileForm(instance=profile)
    return render(request, 'visitors/update_medical_rap.html', {'form_medical_rap_update': form_medical_rap_update,
                                                                'profile_form_update': profile_form_update})
