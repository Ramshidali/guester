from django.conf import settings
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
from cryptography.fernet import Fernet
from django.conf import settings


def load_key():
    key = getattr(settings, "PASSWORD_ENCRYPTION_KEY", None)
    if key:
        return key
    else:
        raise ImproperlyConfigured("No configuration  found in your PASSWORD_ENCRYPTION_KEY setting.")


def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return(encrypted_message.decode("utf-8"))


def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message.encode())
    return decrypted_message.decode()


def generate_form_errors(args,formset=False):
    message = ''
    if not formset:
        for field in args:
            if field.errors:
                message += field.errors  + "|"
        for err in args.non_field_errors():
            message += str(err) + "|"

    elif formset:
        for form in args:
            for field in form:
                if field.errors:
                    message +=field.errors + "|"
            for err in form.non_field_errors():
                message += str(err) + "|"
    return message[:-1]
