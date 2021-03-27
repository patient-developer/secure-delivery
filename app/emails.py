from flask_mail import Message
from app import mail


def send_mail(subject, sender, recipients, text_body, attachment_name, attachment):
    message = Message(subject=subject, sender=sender, recipients=recipients)
    message.body = text_body
    message.attach(attachment_name, 'application/octect-stream', attachment)
    mail.send(message)
