from datetime import datetime

from django.core.paginator import Paginator
from django.db.models import Max
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect

from communication.forms import QueueForm
from services.forms import TypeExaminationForm, StartExaminationForm, MedicalRapContentForm, ExaminationForm, \
    TransferLettersForm, CompanyForm, MedicalReportsForm
from services.models import MedicalRapContent, TypeExamination, StartExamination, Examination, TransferLetters, Company
from staff.models import MedicalStaff
from visitors.models import Patient
from django.utils import timezone
from communication.views import create_paginator
# Create your views here.
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML, CSS
from django.conf import settings
import os


def render_pdf_view(request, startExamination_id):
    examination = StartExamination.objects.get(startExamination_id=startExamination_id)
    html_string = render_to_string('index/prescribed.html', {'examination': examination})
    html = HTML(string=html_string, base_url=request.build_absolute_uri('/'))

    css_files = [
        os.path.join(settings.STATIC_ROOT, 'staff/vendors/styles/core.css'),
        os.path.join(settings.STATIC_ROOT, 'staff/vendors/styles/icon-font.min.css'),
        os.path.join(settings.STATIC_ROOT, 'staff/vendors/styles/style.css'),
    ]

    css = [CSS(filename=css_file) for css_file in css_files]

    pdf = html.write_pdf(stylesheets=css)

    response = HttpResponse(pdf, content_type='application/pdf')
    response['Content-Disposition'] = 'inline; filename="invoice.pdf"'
    return response


def get_content_medical_rap(request):
    get__medical_raps = (MedicalRapContent.objects.values('medical_rap').annotate(content_id=Max('content_id')).
                         order_by())
    latest_get__medical_rap = MedicalRapContent.objects.filter(
        content_id__in=[get__medical_rap['content_id'] for get__medical_rap in get__medical_raps])
    paginator = Paginator(latest_get__medical_rap, 12)
    page = request.GET.get('page')
    medical_rap_objects = paginator.get_page(page)
    return render(request, 'visitors/show_medical_rap.html', {
        'medical_rap_objects': medical_rap_objects
    })


def get_all_content_medical_rap(request, medicalRap_id):
    get_medical_rap = MedicalRapContent.objects.filter(medical_rap__medicalRap_id=medicalRap_id)
    paginator = Paginator(get_medical_rap, 12)
    page = request.GET.get('page')
    medical_rap_objects = paginator.get_page(page)
    return render(request, 'visitors/all_content_for_medical_rap.html', {
        'medical_rap_objects': medical_rap_objects
    })


def post_medical_rap_content(request, medicalRap_id):
    if request.method == 'POST':
        form_medical_rap_content = MedicalRapContentForm(request.POST)
        form_queue_medical_rap = QueueForm(request.POST)
        if form_medical_rap_content.is_valid() and form_queue_medical_rap.is_valid():
            queue_medical_rap = form_queue_medical_rap.save()
            save_medical_rap_content = form_medical_rap_content.save(commit=False)
            save_medical_rap_content.medical_rap_id = medicalRap_id
            save_medical_rap_content.queue = queue_medical_rap
            save_medical_rap_content.save()
            return HttpResponse("Save success")
        else:
            return HttpResponse(form_medical_rap_content.errors)
    else:
        form_queue_medical_rap = QueueForm(default_datetime=datetime.now)
        form_medical_rap_content = MedicalRapContentForm()
    return render(request, 'visitors/post_medical_rap_content.html', {
        'form_medical_rap_content': form_medical_rap_content, 'form_queue_medical_rap': form_queue_medical_rap
    })


def post_type_examination(request):
    if request.method == 'POST':
        form_type_examination = TypeExaminationForm(request.POST)
        if form_type_examination.is_valid():
            form_type_examination.save()
            return HttpResponse("Save")
        else:
            return HttpResponse(form_type_examination.errors)
    else:
        form_type_examination = TypeExaminationForm()
    return render(request, 'services/add_type_examination.html', {'form_type_examination': form_type_examination})


def get_type_examination(request):
    type_examinations = TypeExamination.objects.all()
    return render(request, 'services/all_type_examination.html', {
        'type_examinations': type_examinations
    })


def put_type_examination(request, type_id):
    update_type = get_object_or_404(TypeExamination, type_id=type_id)

    if request.method == 'POST':
        form_update_type = TypeExaminationForm(request.POST, instance=update_type)
        if form_update_type.is_valid():
            form_update_type.save()
            return HttpResponse("update success")
        else:
            return HttpResponse(form_update_type.errors)
    else:
        form_update_type = TypeExaminationForm(instance=update_type)

    return render(request, 'services/update_type_examination.html', {
        'form_update_type': form_update_type
    })


def delete_type_examination(request, type_id):
    delete_type = get_object_or_404(TypeExamination, type_id=type_id)
    delete_type.delete()
    type_examinations = TypeExamination.objects.all()
    return render(request, 'services/all_type_examination.html', {
        'type_examinations': type_examinations
    })


def post_new_examination(request, patient_id):
    patient = Patient.objects.get(patient_id=patient_id)
    if request.method == 'POST':
        form_start_examination = StartExaminationForm(request.POST)
        form_queue_examination = QueueForm(request.POST)
        if form_queue_examination.is_valid() and form_start_examination.is_valid():
            queue_examination = form_queue_examination.save()
            start_examination = form_start_examination.save(commit=False)
            start_examination.queue = queue_examination
            start_examination.patient = patient
            start_examination.save()
            return HttpResponse("Save success")
        else:
            return HttpResponse(f"{form_queue_examination.errors} {form_start_examination.errors}")
    else:
        form_queue_examination = QueueForm(default_datetime=datetime.now)
        form_start_examination = StartExaminationForm()
    return render(request, 'services/post_new_examination.html',
                  {'patient': patient, 'form_start_examination': form_start_examination,
                   'form_queue_examination': form_queue_examination
                   })


# test if doctor is busy
def open_examination(request, doctor):
    try:
        open_examinations = StartExamination.objects.filter(queue__activate_doctor=True, medical__user__username=doctor)

        if open_examinations.exists():
            examinations_details = [
                {
                    'examination_id': examination.startExamination_id,
                    'medical': examination.medical.slug
                }
                for examination in open_examinations
            ]
            return JsonResponse(examinations_details, safe=False)
        else:
            return HttpResponse("No open examinations", status=404)

    except Exception as e:
        return HttpResponse(f"An error occurred: {e}", status=500)


# التعديل علي كشف
def get_start_examinations(request, patient_id):
    get_start_examination = Examination.objects.filter(start_examination__patient__patient_id=patient_id)
    start_examination_objects = create_paginator(request, get_start_examination, 10)
    return render(request, 'services/history_examination.html', {
        'start_examination_objects': start_examination_objects
    })


def put_examination(request, examination_id):
    examination = get_object_or_404(Examination, examination_id=examination_id)
    if request.method == 'POST':
        examination_form = ExaminationForm(data=request.POST, instance=examination)
        if examination_form.is_valid():
            examination_form.save()
            return HttpResponse('Update')
    else:
        examination_form = ExaminationForm(instance=examination)
    return render(request, 'index/send_examination_to_doctor.html', {'examination': examination,
                                                                     'examination_form': examination_form})


def post_transfer_letters(request, patient_id):
    if request.method == 'POST':
        form_transfer_letter = TransferLettersForm(request.POST)
        if form_transfer_letter.is_valid():
            save_transfer_letter = form_transfer_letter.save(commit=False)
            save_transfer_letter.patient_id = patient_id
            save_transfer_letter.save()
            return HttpResponse("save transfer letters")
        else:
            return HttpResponse(form_transfer_letter.errors)
    else:
        form_transfer_letter = TransferLettersForm()
    return render(request, 'services/post_transfer_letters.html', {
        'form_transfer_letter': form_transfer_letter
    })


def get_transfer_letters(request):
    transfer_letters = TransferLetters.objects.all()
    transfer_letters_objects = create_paginator(request, transfer_letters, 12)
    return render(request, 'services/get_transfer_letters.html', {
        'transfer_letters_objects': transfer_letters_objects
    })


def put_transfer_letters(request, transfer_id):
    get_transfer_letter = get_object_or_404(TransferLetters, transfer_id=transfer_id)

    if request.method == 'POST':
        form_transfer_letter = TransferLettersForm(data=request.POST, instance=get_transfer_letter)
        if form_transfer_letter.is_valid():
            form_transfer_letter.save()
            return HttpResponse("save transfer letters")
        else:
            return HttpResponse(form_transfer_letter.errors)
    else:
        form_transfer_letter = TransferLettersForm(instance=get_transfer_letter)
    return render(request, 'services/post_transfer_letters.html', {
        'form_transfer_letter': form_transfer_letter
    })


def delete_transfer_letters(request, transfer_id):
    delete_transfer_letter = TransferLetters.objects.get(transfer_id=transfer_id).delete()
    return redirect('get_transfer_letters')


def post_company(request):
    if request.method == 'POST':
        form_company = CompanyForm(request.POST)
        if form_company.is_valid():
            form_company.save()
            return redirect('post_company')
        else:
            return HttpResponse(form_company.errors)
    else:
        form_company = CompanyForm()
    return render(request, 'services/post_company.html', {
        'form_company': form_company
    })


def get_company(request):
    company = Company.objects.all()
    company_objects = create_paginator(request, company, 12)
    return render(request, 'services/get_company.html', {
        'company_objects': company_objects
    })


def put_company(request, company_id):
    get_company_info = get_object_or_404(Company, company_id=company_id)
    if request.method == 'POST':
        form_company = CompanyForm(data=request.POST, instance=get_company_info)
        if form_company.is_valid():
            form_company.save()
            return HttpResponse('Update success')
        else:
            return HttpResponse(form_company.errors)
    else:
        form_company = CompanyForm(instance=get_company_info)
    return render(request, 'services/update_company.html', {
        'form_company': form_company
    })


def post_medical_reports(request, patient_id):
    patient = Patient.objects.get(patient_id=patient_id)
    if request.method == 'POST':
        form_medical_reports = MedicalReportsForm(request.POST)
        if form_medical_reports.is_valid():
            save_medical_reports = form_medical_reports.save(commit=False)
            save_medical_reports.patient_id = patient_id
            save_medical_reports.save()
            return HttpResponse("save success")
        else:
            return HttpResponse(form_medical_reports.errors)
    else:
        doctor = MedicalStaff.objects.get(user=request.user).medicalStaff_id
        form_medical_reports = MedicalReportsForm(default_medical=f"{doctor}")
    return render(request, 'services/post_medical_reports.html',
                  {'form_medical_reports': form_medical_reports, 'patient': patient})
