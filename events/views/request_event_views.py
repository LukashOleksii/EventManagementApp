from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from ..models import Event, EventRequest
from ..services.email_service import send_request_notification, send_request_status

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
