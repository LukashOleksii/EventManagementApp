from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from ..models import Event
from ..serializers import EventSerializer

@swagger_auto_schema(method='post',
                     manual_parameters=[
                        openapi.Parameter('title', in_=openapi.IN_PATH,
                            description="Title of the event", type=openapi.TYPE_STRING,
                            required=True,
                        ),
                        openapi.Parameter('description', in_=openapi.IN_QUERY,
                            description="Description of the event",
                            type=openapi.TYPE_STRING, required=True,
                        ),
                        openapi.Parameter('date', in_=openapi.IN_QUERY,
                            description="Date and time of the event (YYYY-MM-DDThh:mm)",
                            type=openapi.TYPE_STRING, required=True,
                        ),
                        openapi.Parameter('location', in_=openapi.IN_QUERY,
                            description="Location of the event",
                            type=openapi.TYPE_STRING, required=True,
                        ),
                        openapi.Parameter('organizer', in_=openapi.IN_QUERY,
                            description="Organizer of the event(user_id)",
                            type=openapi.TYPE_STRING, required=True,
                        ),
                        openapi.Parameter('member', in_=openapi.IN_QUERY,
                            description="Users of the event(user_id)",
                            type=openapi.TYPE_INTEGER, required=False,
                        )
                    ],
)
@api_view(['GET', 'POST'])
def event_list(request):
    if request.method == 'GET':
        events = Event.objects.all()
        serializer = EventSerializer(events, many=True)

        return Response(serializer.data)

    if request.method == 'POST':
        serializer = EventSerializer(data=request.data)

        if serializer.is_valid():
            event = serializer.save(organizer=request.user)
            return Response(EventSerializer(event).data, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def own_events(request):
    events = Event.objects.filter(organizer=request.user)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def participated_events(request):
    events = Event.objects.filter(members=request.user)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def available_events(request):
    events = Event.objects.exclude(members=request.user).exclude(organizer=request.user)
    serializer = EventSerializer(events, many=True)
    return Response(serializer.data)

@swagger_auto_schema(method='put',
                     manual_parameters=[
                        openapi.Parameter('title', in_=openapi.IN_PATH,
                            description="Title of the event", type=openapi.TYPE_STRING,
                            required=True,
                        ),
                        openapi.Parameter('description', in_=openapi.IN_QUERY,
                            description="Description of the event",
                            type=openapi.TYPE_STRING, required=True,
                        ),
                        openapi.Parameter('date', in_=openapi.IN_QUERY,
                            description="Date and time of the event (YYYY-MM-DDThh:mm)",
                            type=openapi.TYPE_STRING, required=True,
                        ),
                        openapi.Parameter('location', in_=openapi.IN_QUERY,
                            description="Location of the event",
                            type=openapi.TYPE_STRING, required=True,
                        ),
                        openapi.Parameter('organizer', in_=openapi.IN_QUERY,
                            description="Organizer of the event(user_id)",
                            type=openapi.TYPE_STRING, required=True,
                        ),
                        openapi.Parameter('member', in_=openapi.IN_QUERY,
                            description="Users of the event(user_id)",
                            type=openapi.TYPE_INTEGER, required=False,
                        )
                    ],
)
@api_view(['GET', 'PUT', 'DELETE'])
def event_detail(request, pk):
    """
    Retrieve, update or delete an event.
    """
    try:
        event = Event.objects.get(pk=pk)
    except Event.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'GET':
        serializer = EventSerializer(event)
        return Response(serializer.data)
    
    elif request.method == 'PUT':
        serializer = EventSerializer(event, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'DELETE':
        event.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

