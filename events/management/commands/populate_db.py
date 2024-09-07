from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from events.models import Event, EventRequest
from datetime import datetime, timedelta
import random
from faker import Faker

class Command(BaseCommand):
    help = 'Populate the database with users, events, and event requests'

    def handle(self, *args, **kwargs):
        faker = Faker()

        self.stdout.write("Creating users...")
        users = self.create_users(faker, n=5)
        
        self.stdout.write("Creating events...")
        events = self.create_events(faker, users, n=3)
        
        self.stdout.write("Creating event requests...")
        self.create_event_requests(users, events)
        
        self.stdout.write("Database populated successfully!")

    def create_users(self, faker, n=5):
        users = []
        for _ in range(n):
            username = f"{faker.first_name()}_{faker.last_name()}"
            email = faker.email()
            password = 'password123'
            
            user, created = User.objects.get_or_create(username=username, email=email)
            if created:
                user.set_password(password)
                user.save()
            users.append(user)
        return users

    def create_events(self, faker, users, n=5):
        events = []
        for i in range(n):
            event = Event.objects.create(
                title=faker.sentence(nb_words=4),
                description=faker.paragraph(nb_sentences=3),
                date=datetime.now() + timedelta(days=i),
                location=faker.address(),
                organizer=random.choice(users)
            )
            events.append(event)
        return events

    def create_event_requests(self, users, events):
        for event in events:
            for user in users:
                if user != event.organizer:
                    EventRequest.objects.create(
                        event=event,
                        user=user,
                        is_approved=random.choice([True, False])
                    )
