from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from ..models import Event
from django.utils import timezone
from django.contrib.auth import get_user_model

class EventViewsTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.client.login(username='testuser', password='testpassword')
        self.event = Event.objects.create(
            title='Test Event',
            description='This is a test event',
            date=timezone.now(),
            location='This is some location',
            organizer=self.user
        )
    
    def test_event_list_view(self):
        response = self.client.get(reverse('event_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/event_list.html')
        self.assertContains(response, 'Test Event')

    def test_event_create_view(self):
        response = self.client.post(reverse('event_create'), {
            'title': 'New Event',
            'description': 'This is a new event',
            'date': timezone.now().date(),
            'time': timezone.now().time(),
            'location': 'This is some location',
        })

        self.assertEqual(response.status_code, 302) 
        self.assertEqual(Event.objects.count(), 2)  

    def test_event_update_view(self):
        response = self.client.post(reverse('event_update', args=[self.event.pk]), {
            'title': 'Updated Event',
            'description': 'This is an updated event',
            'date': timezone.now().date(),
            'time': timezone.now().time(),
            'location': 'Updated location',
        })

        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertEqual(self.event.title, 'Updated Event')
        self.assertEqual(self.event.location, 'Updated location')

    def test_event_delete_view(self):
        response = self.client.post(reverse('event_delete', args=[self.event.pk]))
        self.assertEqual(response.status_code, 302)  
        self.assertEqual(Event.objects.count(), 0)  

    def test_own_events_view(self):
        response = self.client.get(reverse('own_events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/own_events.html')
        self.assertContains(response, 'Test Event')

    def test_participated_events_view(self):
        response = self.client.get(reverse('participated_events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/participated_events.html')

    def test_available_events_view(self):
        response = self.client.get(reverse('available_events'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/available_events.html')

    def test_cancel_request_view(self):
        response = self.client.post(reverse('cancel_request', args=[self.event.pk]))
        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertNotIn(self.user, self.event.members.all())

    def test_manage_requests_view(self):
        response = self.client.get(reverse('manage_requests', args=[self.event.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'events/manage_requests.html')

    def test_leave_event_view(self):
        self.event.members.add(self.user) 
        response = self.client.post(reverse('leave_event', args=[self.event.pk]))
        self.assertEqual(response.status_code, 302)
        self.event.refresh_from_db()
        self.assertNotIn(self.user, self.event.members.all())
