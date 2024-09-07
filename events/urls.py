from django.urls import path
from .views.event_views import (
    event_create, event_list, event_update, event_delete, 
    own_events, participated_events, available_events
)
from .views.user_views import register, login_view
from .views.request_event_views import (
    join_event, cancel_request, manage_requests, leave_event
)

from django.contrib import admin
from django.contrib.auth import views as auth_views

urlpatterns = [
    # path('admin/', admin.site.urls),

    # Event views
    path('', event_list, name='event_list'),
    path('events/create/', event_create, name='event_create'),
    path('events/<int:pk>/update/', event_update, name='event_update'),
    path('events/<int:pk>/delete/', event_delete, name='event_delete'),
    path('own-events/', own_events, name='own_events'),
    path('participated-events/', participated_events, name='participated_events'),
    path('available-events/', available_events, name='available_events'),

    # User views
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),


    # Request views
    path('events/<int:pk>/join/', join_event, name='join_event'),
    path('events/<int:event_id>/cancel/', cancel_request, name='cancel_request'),
    path('events/<int:event_id>/manage-requests/', manage_requests, name='manage_requests'),
    path('events/<int:pk>/leave/', leave_event, name='leave_event'),

    # path('', views.event_views.event_list, name='event_list'), 

    # path('own-events/', views.event_views.own_events, name='own_events'),
    # path('participated-events/', views.event_views.participated_events, name='participated_events'),
    # path('available-events/', views.event_views.available_events, name='available_events'),

    # path('event/new/', views.event_views.event_create, name='event_create'),
    # path('event/<int:pk>/edit/', views.event_views.event_update, name='event_update'),
    # path('event/<int:pk>/delete/', views.event_views.event_delete, name='event_delete'),

    # path('register/', views.user_views.register, name='register'),
    # path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),

    # path('event/<int:pk>/join/', views.request_event_views.join_event, name='join_event'),
    # path('event/<int:pk>/leave/', views.request_event_views.leave_event, name='leave_event'),

    # path('event/<int:event_id>/manage-requests/', views.request_event_views.manage_requests, name='manage_requests'),
    # path('event/<int:event_id>/cancel-request/', views.request_event_views.cancel_request, name='cancel_request'),

]
