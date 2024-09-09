import os
import random

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from core.dataclasses.user_dataclass import User
from core.services.jwt_service import ActivateToken, ApprovalToken, JWTService, RecoveryToken

UserModel = get_user_model()


class EmailService:
    @staticmethod
    def __send_email(to: str, template_name: str, context: dict, subject='') -> None:
        template = get_template(template_name)
        html_content = template.render(context)
        msg = EmailMultiAlternatives(subject=subject, from_email=os.environ.get('EMAIL_HOST_USER'), to=[to])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

    @classmethod
    def register_email(cls, user: User):
        token = JWTService.create_token(user, ActivateToken)
        url = f'http://localhost:3000/activate/{token}'
        cls.__send_email(
            user.email,
            template_name='register.html',
            context={'name': user.profile.name, 'url': url},
            subject='Register'
        )

    @classmethod
    def recovery_email(cls, user: User):
        token = JWTService.create_token(user, RecoveryToken)
        url = f'http://localhost:3000/recovery/{token}'
        cls.__send_email(user.email, 'recovery.html', {'url': url}, 'Recovery password')

    @classmethod
    def approve_email_change(cls, user: User, new_email: str):
        token = JWTService.create_token(user, ApprovalToken)
        url = f'http://localhost:3000/approve/{token}'
        cls.__send_email(new_email, 'approve.html', {'url': url}, 'Approval password')

    @classmethod
    def warning_email(cls, user: User):
        cls.__send_email(user.email, 'warning.html', {}, 'Warning')

    @classmethod
    def check_badwords_email(cls, user_id: int, car_id: int):
        managers = UserModel.objects.filter(is_active=True, is_staff=True, is_superuser=False)
        manager = random.choice(managers)
        cls.__send_email(
            manager.email,
            'badwords.html',
            {'user_id': f'{user_id}', 'car_id': f'{car_id}'},
            'Badwords'
        )
