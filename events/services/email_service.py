from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings

def send_request_notification(event, recipient):
    """Send notification for a new event request."""
    subject = 'New Event Request'

    html_message = render_to_string('emails/request_notification.html', {
        'event': event,
        'recipient': recipient,
        'request_url': f'http://example.com/manage-requests/{event.pk}',
    })
    
    plain_message = strip_tags(html_message)

    send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [recipient.email], html_message=html_message)

def send_request_status(user, event, status):
    """Send email to notify the user about the status of their event request."""
    subject = 'Event Request Status'

    html_message = render_to_string('emails/request_status.html', {
        'user': user,
        'event': event,
        'status': status,
    })

    plain_message = strip_tags(html_message)

    send_mail(subject, plain_message, settings.EMAIL_HOST_USER, [user.email], html_message=html_message)
