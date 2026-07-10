from django.core.mail import send_mail

from biller.config import Configurations


class EmailService:
    def __init__(self, subject: str, body: str, to: list):
        self.subject = subject
        self.body = body
        self.to = to

    @staticmethod
    def check_email(func):
        def check(*args, **kwargs):
            if Configurations.email_service_enable:
                result = func(*args, **kwargs)
                return result
            return 'email is not enabled'

        return check

    @check_email
    def send_email(self):
        send_mail(subject=self.subject,message='', from_email=Configurations.email_host_user, recipient_list=self.to,html_message=self.body)
