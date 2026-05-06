from secrets import token_urlsafe
import hashlib

from celery import shared_task

def generate_reset_token():
    raw_token = token_urlsafe(32)
    hashed_token = hashlib.sha256(raw_token.encode()).hexdigest()

    return raw_token, hashed_token



@shared_task(bind=True, max_retries=3)
def send_email_task(self, subject, html_content, to_email):
    from django.core.mail import EmailMultiAlternatives

    try:
        msg = EmailMultiAlternatives(subject=subject, to=[to_email])
        msg.attach_alternative(html_content, "text/html")
        msg.send()
    except Exception as e:
        raise self.retry(exc=e, countdown=10)