from django.urls import path
from .api_views.api_event_views import (
    event_list, event_detail, own_events, participated_events, available_events, 
)
from .api_views.api_request_event_views import (
    join_event, cancel_request, manage_requests, leave_event
)

urlpatterns = [
    path('events/', event_list, name='api_event_list'),
    path('events/<int:pk>/', event_detail, name='api_event_detail'),

    path('events/own-events/', own_events, name='api_own_events'),
    path('events/participated-events/', participated_events, name='api_participated_events'),
    path('events/available-events/', available_events, name='api_available_events'),
    
    path('events/<int:pk>/join/', join_event, name='api_join_event'),
    path('events/<int:pk>/leave/', leave_event, name='api_leave_event'),

    path('events-request/<int:event_id>/cancel/', cancel_request, name='api_cancel_request'),
    path('events-request/<int:event_id>/manage-requests/', manage_requests, name='api_manage_requests'),
]
