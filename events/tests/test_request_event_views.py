from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
from ..models import Event, EventRequest

class EventRequestViewsTestCase(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.other_user = User.objects.create_user(username='otheruser', password='password')
        self.client.login(username='testuser', password='testpassword')
        
        self.event = Event.objects.create(
            title='Test Event',
            description='This is a test event',
            date=timezone.now(),
            location='This is some location',
            organizer=self.user
        )
        
    def test_join_event_view(self):
        response = self.client.post(reverse('join_event', args=[self.event.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertTrue(EventRequest.objects.filter(event=self.event, user=self.user).exists())
        
    def test_cancel_join_request_view(self):
        t = EventRequest.objects.create(event=self.event, user=self.other_user, is_approved=False)
        self.assertTrue(EventRequest.objects.filter(event=self.event, user=self.other_user, is_approved=False).exists())
        self.client.force_login(self.other_user)
        response = self.client.post(reverse('cancel_request', args=[self.event.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(EventRequest.objects.filter(event=self.event, user=self.other_user, is_approved=False).exists())
    
    def test_manage_requests_approve_view(self):
        self.client.login(username='otheruser', password='password')
        self.client.post(reverse('join_event', args=[self.event.pk]))
        self.client.login(username='testuser', password='testpassword')
        
        event_request = EventRequest.objects.get(event=self.event, user=self.other_user)
        
        response = self.client.post(reverse('manage_requests', args=[self.event.pk]), {
            'request_id': event_request.id,
            'action': 'approve',
        })
        
        self.assertEqual(response.status_code, 302)
        
        self.event.refresh_from_db()
        self.assertIn(self.other_user, self.event.members.all())

    def test_manage_requests_decline_view(self):
        self.client.login(username='otheruser', password='password')
        self.client.post(reverse('join_event', args=[self.event.pk]))
        self.client.login(username='testuser', password='testpassword')
        
        event_request = EventRequest.objects.get(event=self.event, user=self.other_user)
        
        response = self.client.post(reverse('manage_requests', args=[self.event.pk]), {
            'request_id': event_request.id,
            'action': 'decline',
        })
        
        self.assertEqual(response.status_code, 302)
        
        self.event.refresh_from_db()
        self.assertNotIn(self.other_user, self.event.members.all())
        
        self.assertFalse(EventRequest.objects.filter(event=self.event, user=self.other_user).exists())

