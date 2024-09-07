from django.shortcuts import render, get_object_or_404, redirect
from .models import Event, EventRequest
from .forms import EventForm, CustomUserCreationForm
from django.contrib.auth import login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

@login_required
def event_create(request):
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False)
            event.organizer = request.user 
            event.save()
            return redirect('own_events')
    else:
        form = EventForm(current_user=request.user)
    return render(request, 'events/event_form.html', {'form': form})

def event_list(request):
    events = Event.objects.all()
    
    return render(request, 'events/event_list.html', {'events': events})

@login_required
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if event.organizer != request.user:
        return redirect('own_events')
    
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            form.save()
            return redirect('own_events')
    else:
        form = EventForm(instance=event, current_user=request.user)
    return render(request, 'events/event_form.html', {'form': form})

@login_required
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if event.organizer == request.user:
        event.delete()
    
    return redirect('own_events')


@login_required
def own_events(request):
    events = Event.objects.filter(organizer=request.user)

    for event in events:
        event.pending_requests_count = EventRequest.objects.filter(event=event, is_approved=False).count()


    return render(request, 'events/own_events.html', {'events': events})

@login_required
def participated_events(request):
    events = Event.objects.filter(members=request.user)
    return render(request, 'events/participated_events.html', {'events': events})

@login_required
def available_events(request):
    events = Event.objects.exclude(members=request.user).exclude(organizer=request.user)

    for event in events:
        event.pending_request = EventRequest.objects.filter(
                event=event, user=request.user, is_approved=False
            ).exists()

    return render(request, 'events/available_events.html', {'events': events})

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('event_list') 
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('event_list') 
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.method == 'POST':
        EventRequest.objects.create(event=event, user=request.user)
        send_request_notification(event, event.organizer)

        return redirect('available_events')

    return redirect('available_events')

@login_required
def cancel_request(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    pending_request = EventRequest.objects.filter(event=event, user=request.user, is_approved=False).first()

    if pending_request:
        pending_request.delete()

    return redirect('available_events')


@login_required
def manage_requests(request, event_id):
    event = get_object_or_404(Event, id=event_id)

    if request.user != event.organizer:
        return redirect('own_events')

    requests = EventRequest.objects.filter(event=event, is_approved=False)

    if request.method == 'POST':
        request_id = request.POST.get('request_id')
        action = request.POST.get('action')

        event_request = get_object_or_404(EventRequest, id=request_id)

        if action == 'approve':
            event_request.is_approved = True
            event_request.save()
            event.members.add(event_request.user)
            send_request_status(event_request.user, event_request.event, 'approved')
        elif action == 'decline':
            send_request_status(event_request.user, event_request.event, 'declined')
            event_request.delete()

        return redirect('manage_requests', event_id=event.id)

    return render(request, 'events/manage_requests.html', {'requests': requests, 'event': event})


@login_required
def leave_event(request, pk):
    event = get_object_or_404(Event, pk=pk)

    if request.user in event.members.all():  
        event.members.remove(request.user)

    return redirect('participated_events') 

def send_request_notification(event, recipient):
    subject = 'New Event Request'
    html_message = render_to_string('emails/request_notification.html', {
        'event': event,
        'recipient': recipient,
        'request_url': 'http://example.com/manage-requests/{}'.format(event.pk),
    })
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [recipient.email], html_message=html_message)

def send_request_status(user, event, status):
    subject = 'Event Request Status'
    html_message = render_to_string('emails/request_status.html', {
        'user': user,
        'event': event,
        'status': status,
    })
    plain_message = strip_tags(html_message)
    send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [user.email], html_message=html_message)
