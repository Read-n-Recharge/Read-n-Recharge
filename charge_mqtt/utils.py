from django.core.mail import send_mail
from django.conf import settings


def send_password_email(user, relayID, password):
    """Helper function to send email with relay password."""
    send_mail(
        subject='Your Charging Station Password',
        message=f'Your password for the charging station is: {password} for socket-ID: {relayID}',
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email],
        fail_silently=False
    )

def validate_password(password):
    """Validate that password is a 6-digit number."""
    return len(password) == 6 and password.isdigit()