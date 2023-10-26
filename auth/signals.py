import logging
from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver


user_logger = logging.getLogger("auth")


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):
    ip = request.META.get('REMOTE_ADDR')

    user_logger.info('Login: {user.username} via ip: {ip}'.format(
        user=user,
        ip=ip
    ))


@receiver(user_login_failed)
def user_login_failed_callback(sender, request, credentials, **kwargs):
    ip = request.META.get('REMOTE_ADDR')
    credentials.pop("password", None)
    user_logger.warning('Login Failed: {credentials} via ip: {ip}'.format(
        credentials=credentials, ip=ip
    ))