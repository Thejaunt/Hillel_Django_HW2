from bookstore.tasks import email_sender_task

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import dateformat, timezone


class ContactForm(forms.Form):
    mail = forms.EmailField(max_length=200, required=True, widget=forms.EmailInput())
    date = forms.DateTimeField(
        input_formats="Y-m-d H:i:s",
        help_text="Date and time (YYYY-MM-DD HH:MM:SS) you would like to receive the notification",
    )
    message = forms.CharField(max_length=500, required=True, widget=forms.Textarea(attrs={"rows": 3}))

    def clean_date(self):
        send_date = self.cleaned_data.get("date")
        if send_date > timezone.now() + timezone.timedelta(days=2):
            raise ValidationError(
                f"Shouldn't be later than 2 days, current UTC time {dateformat.format(timezone.now(), 'Y-m-d H:i:s')}"
            )
        if send_date < timezone.now():
            raise ValidationError(
                f"Can't be in the past. Check UTC current time {dateformat.format(timezone.now(), 'Y-m-d H:i:s')}"
            )
        return self.cleaned_data.get("date")

    def send_email(self):
        recipient = self.cleaned_data.get("mail")
        subject = "celery task"
        text = self.cleaned_data.get("message")
        from_email = settings.EMAIL
        email_sender_task.apply_async(
            (
                subject,
                text,
                from_email,
                recipient,
            ),
            eta=self.cleaned_data.get("date"),
        )
