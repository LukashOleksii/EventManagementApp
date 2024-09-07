from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from ..models import Event, EventRequest
from ..forms import EventForm

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
    events = Event.objects.all().order_by('date')

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
    events = Event.objects.filter(organizer=request.user).order_by('date')

    for event in events:
        event.pending_requests_count = EventRequest.objects.filter(event=event, is_approved=False).count()

    return render(request, 'events/own_events.html', {'events': events})

@login_required
def participated_events(request):
    events = Event.objects.filter(members=request.user).order_by('date')

    return render(request, 'events/participated_events.html', {'events': events})

@login_required
def available_events(request):
    events = Event.objects.exclude(members=request.user).exclude(organizer=request.user).order_by('date')

    for event in events:
        event.pending_request = EventRequest.objects.filter(
            event=event, user=request.user, is_approved=False
        ).exists()
        
    return render(request, 'events/available_events.html', {'events': events})
