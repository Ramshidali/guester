import datetime
import decimal
import random
import re
import string

import requests
from customers.models import Customer



def generate_serializer_errors(args):
    message = ''
    for key, values in args.items():
        error_message = ""
        for value in values:
            error_message += value + ","
        error_message = error_message[:-1]

        message += "%s : %s |" % (key, error_message)
        
    return message[:-3]


def get_user_token(request, user_name, password):
    headers = {'Content-Type': 'application/json', }
    data = '{"username": "' + user_name + '", "password":"' + password + '"}'
    # print(data, "--data")
    protocol = "http://"
    if request.is_secure():
        protocol = "https://"

    web_host = request.get_host()
    request_url = protocol + web_host + "/api/v1/auth/token/"

    # print(request_url, "--------request_url")

    response = requests.post(request_url, headers=headers, data=data)
    # print(response, "------response2")
    return (response)


def get_otp(size=4, chars=string.digits):
    
    return ''.join(random.choice(chars) for _ in range(size))


def check_paswword_strength(password):
    if (len(password) >= 8):
        if (bool(re.match('((?=.*\d)(?=.*[a-z])(?=.*[A-Z])(?=.*[!@#$%^&*]).{8,30})', password)) == True):
            
            return True
        elif (bool(re.match('((\d*)([a-z]*)([A-Z]*)([!@#$%^&*]*).{8,30})', password)) == True):
            
            return "Password is weak"
    else:
        
        return "Password is weak"


def get_current_date():
    
    return datetime.date.today()


def get_user(user):
    user = Customer.objects.get(phone=user)
    
    return user




