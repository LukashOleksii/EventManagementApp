from rest_framework import serializers
from .models import Event, EventRequest

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'description', 'date', 'location', 'organizer', 'members']

class EventRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventRequest
        fields = ['id', 'event', 'user', 'is_approved', 'requested_at']
