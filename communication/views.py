from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from communication.forms import LoginForm
from services.forms import ExaminationForm, MedicalRapContentForm
from services.models import StartExamination, MedicalRapContent, Examination
from communication.models import Queue, Chat
from django.contrib.auth.models import User
from django.utils import timezone
import pytz

from visitors.models import MedicalRap


# Create your views here.
def create_paginator(request, query_dict, number_page=6):
    paginator = Paginator(query_dict, number_page)
    page = request.GET.get('page')
    query_dict_objects = paginator.get_page(page)
    return query_dict_objects


def test_doctor_busy(Doctor):
    if StartExamination.objects.filter(
            queue__activate_doctor=True, medical__user__username=Doctor
    ).exists():
        return StartExamination.objects.filter(
            queue__activate_doctor=True, medical__user__username=Doctor
        ).exists()
    elif MedicalRapContent.objects.filter(
            queue__activate_doctor=True, medical__user__username=Doctor
    ).exists():
        return MedicalRapContent.objects.filter(
            queue__activate_doctor=True, medical__user__username=Doctor
        ).exists()
    else:
        return False


def get_examinations__patient_for_assistant(assistant):
    return StartExamination.objects.filter(queue__end_work=False, queue__activate_doctor=False,
                                           assistant__user__username=assistant)


def get_examinations_not_end_for_doctor(doctor):
    local_timezone = pytz.timezone('Africa/Cairo')
    today = timezone.now().astimezone(local_timezone).date()
    return StartExamination.objects.filter(queue__end_work=False,
                                           queue__start_at__date=today,
                                           medical__user__username=doctor)


def get_examinations_end_for_doctor(doctor):
    local_timezone = pytz.timezone('Africa/Cairo')
    today = timezone.now().astimezone(local_timezone).date()
    return Examination.objects.filter(start_examination__queue__end_work=True,
                                      start_examination__queue__start_at__date=today,
                                      start_examination__medical__user__username=doctor)


def get_medical_rap_for_assistant(assistant):
    return MedicalRapContent.objects.filter(queue__end_work=False, queue__activate_doctor=False,
                                            assistant__user__username=assistant)


@login_required
def show_index_for_doctor(request):
    examinations_not_end = get_examinations_not_end_for_doctor(request.user.username)
    examinations_end = get_examinations_end_for_doctor(request.user.username)
    examinations_not_end_objects = create_paginator(request, examinations_not_end, 5)
    examinations_end_objects = create_paginator(request, examinations_end, 5)
    return render(request, 'index/show_index_for_doctor.html', {
        'examinations_not_end_objects': examinations_not_end_objects,
        'examinations_end_objects': examinations_end_objects
    })


@login_required
def show_index_for_assistant(request):
    sendSignal = False
    get_examinations_for_patients = get_examinations__patient_for_assistant(request.user.username)
    get_medical_rap = get_medical_rap_for_assistant(request.user.username)
    examinations_for_patients = create_paginator(request, get_examinations_for_patients, 5)
    medical_raps = create_paginator(request, get_medical_rap, 5)
    return render(request, 'index/show_index_for_assistant.html', {
        'examinations_for_patients': examinations_for_patients, 'medical_raps': medical_raps, 'sendSignal': sendSignal
    })


def open_examination(request, startExamination_id, Doctor):
    sendSignal = test_doctor_busy(Doctor)
    get_examinations_for_patients = get_examinations__patient_for_assistant(request.user.username)
    paginator = Paginator(get_examinations_for_patients, 6)
    page = request.GET.get('page')
    examinations_for_patients = paginator.get_page(page)

    data = StartExamination.objects.get(startExamination_id=startExamination_id)
    return render(request, 'index/show_index_for_assistant.html',
                  {'examinations_for_patients': examinations_for_patients,
                   'data': data, 'sendSignal': sendSignal
                   })


def open_medical_rap(request, content_id, Doctor):
    sendSignal = test_doctor_busy(Doctor)
    get_medical_rap = get_medical_rap_for_assistant(request.user.username)
    paginator = Paginator(get_medical_rap, 6)
    page = request.GET.get('page')
    medical_raps = paginator.get_page(page)

    medical_content = MedicalRapContent.objects.get(content_id=content_id)
    return render(request, 'index/show_index_for_assistant.html',
                  {'medical_raps': medical_raps,
                   'medical_content': medical_content, 'sendSignal': sendSignal
                   })


def send_examination_to_doctor(request, startExamination_id):
    examination = StartExamination.objects.get(startExamination_id=startExamination_id)
    queue_end = get_object_or_404(Queue, queue_id=examination.queue.queue_id)
    if request.method == 'POST':
        examination_form = ExaminationForm(data=request.POST)
        if examination_form.is_valid():
            examination_save = examination_form.save(commit=False)
            examination_save.start_examination_id = startExamination_id
            queue_end.end_work = True
            queue_end.activate_doctor = False
            examination_save.save()
            queue_end.save()
            return render(request, 'index/prescribed_view.html', {'examination': examination})
    else:
        examination_form = ExaminationForm()
    return render(request, 'index/send_examination_to_doctor.html', {'examination': examination,
                                                                     'examination_form': examination_form})


def send_medical_rap_to_doctor(request, content_id):
    get_medical_rap = get_object_or_404(MedicalRapContent, content_id=content_id)
    queue_id = get_medical_rap.queue.queue_id
    get_queue = get_object_or_404(Queue, queue_id=queue_id)

    if request.method == "POST":
        form_medical_rap = MedicalRapContentForm(data=request.POST, instance=get_medical_rap)
        if form_medical_rap.is_valid():
            get_queue.end_work = True
            get_queue.activate_doctor = False
            get_queue.save()
            form_medical_rap.save()
        else:
            return HttpResponse(form_medical_rap.errors)
    else:
        form_medical_rap = MedicalRapContentForm(instance=get_medical_rap)
    return render(request, 'index/send_medical_rap_to_doctor.html', {
        'form_medical_rap': form_medical_rap, 'get_medical_rap': get_medical_rap
    })


def staff_login(request):
    if request.method == 'POST':
        form_login = LoginForm(request.POST)
        if form_login.is_valid():
            user = authenticate(request, username=form_login.cleaned_data['username'],
                                password=form_login.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('show_index_for_doctor')
                elif user.is_staff:
                    return redirect('show_examination_for_assistant')
            else:
                return HttpResponse("Invalid login details", status=401)
        else:
            return HttpResponse(form_login.errors.as_json(), content_type="application/json", status=400)
    else:
        form_login = LoginForm()
    return render(request, 'index/login.html', {'form_login': form_login})


def load_user_chat(request):
    chats = User.objects.all()
    return render(request, 'index/chatapp.html', {'chats': chats})


def message(request, username):
    chats = User.objects.all()
    message_user = User.objects.get(username=username)
    messages = Chat.objects.filter(Q(room_receiving__username=username, room_send__username=request.user.username) |
                                   Q(room_receiving__username=request.user.username, room_send__username=username))
    return render(request, 'index/chatapp.html', {'message_user': message_user, 'messages': messages, 'chats': chats})
