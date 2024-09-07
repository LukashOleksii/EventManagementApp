from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from ..models import Event, EventRequest
from ..serializers import EventRequestSerializer
from django.shortcuts import get_object_or_404


@api_view(['POST'])
def join_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event_request, created = EventRequest.objects.get_or_create(event=event, user=request.user)
    if created:
        return Response(EventRequestSerializer(event_request).data, status=status.HTTP_201_CREATED)
    return Response({"detail": "Request already exists"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['DELETE'])
def cancel_request(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    try:
        event_request = EventRequest.objects.get(event=event, user=request.user, is_approved=False)
        event_request.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except EventRequest.DoesNotExist:
        return Response({"detail": "Request does not exist"}, status=status.HTTP_404_NOT_FOUND)

@swagger_auto_schema(method='post', 
                     manual_parameters=[
                        openapi.Parameter('request_id', in_=openapi.IN_PATH,
                            description="ID of the request", type=openapi.TYPE_STRING,
                            required=True,
                        ),
                        openapi.Parameter('action', in_=openapi.IN_QUERY,
                            description="Status of the event request",
                            type=openapi.TYPE_STRING, enum=['approve', 'decline'],
                            required=True,
                        )
                    ],
)
@api_view(['POST', 'GET'])
def manage_requests(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user != event.organizer:
        return Response({"detail": "Not authorized"}, status=status.HTTP_403_FORBIDDEN)
    
    if request.method == 'GET':
        event_requests = EventRequest.objects.filter(event_id=event_id, is_approved=False)
        serializer = EventRequestSerializer(event_requests, many=True)

        return Response(serializer.data)
    
    if request.method == 'POST':
        request_id = request.data.get('request_id')
        action = request.data.get('action')
        try:
            event_request = EventRequest.objects.get(id=request_id)
            if action == 'approve':
                event_request.is_approved = True
                event_request.save()
                event.members.add(event_request.user)
                return Response(EventRequestSerializer(event_request).data)
            elif action == 'decline':
                event_request.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
        except EventRequest.DoesNotExist:
            return Response({"detail": "Request does not exist"}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def leave_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.user in event.members.all():
        event.members.remove(request.user)
        return Response(status=status.HTTP_204_NO_CONTENT)
    return Response({"detail": "Not a member"}, status=status.HTTP_400_BAD_REQUEST)
