from celery import shared_task

from django.core.mail import send_mail
from django.template import loader


@shared_task()
def email_sender_task(subject, text, from_email, recipient):
    message = loader.render_to_string("email.html", {"message": text, "recipient": recipient})
    send_mail(
        subject=subject or "celery task",
        message=message,
        from_email=from_email,
        recipient_list=[recipient],
        fail_silently=False,
    )
