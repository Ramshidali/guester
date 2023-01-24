import base64

from django.contrib.auth.models import User
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage

from rest_framework import status
from rest_framework.decorators import (api_view, permission_classes, renderer_classes)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from api.v1.general.functions import get_otp, get_user_token, generate_serializer_errors, get_user
from api.v1.registrations.serializers import  OtpVerifySerializer, RegisterSerializer, CustomerSerializer
from api.v1.users.serializers import ProfileImageSerializer
from customers.models import Customer, Otp, OtpMail
from general.functions import get_auto_id, send_email, validate_password
from users.functions import encrypt_message, decrypt_message
from general.utils.sms import SMS


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def register(request):
    otp = get_otp()
    message = ""
    error = False

    serialized = RegisterSerializer(data=request.data)

    phone = request.data['phone']
    name = request.data['name']
    location = request.data['location']
    latitude = request.data['latitude']
    longitude = request.data['longitude']


    if User.objects.filter(username=phone, is_active=True).exists():
        error = True
        message += "A User with this Phone Number already exists."

    if Customer.objects.filter(phone=phone, is_deleted=False, user__is_active=True).exists():
        error = True
        message += "This Phone Number already exists."

    if not error:
        if serialized.is_valid():
            # password = make_password(password)
            if Otp.objects.filter(phone=phone).exists():
                otp = Otp.objects.get(phone=phone).otp

            data = User.objects.create_user(
                username=phone,
                password=phone,
                is_active=True,
            )

            instance = data

            customer = Customer.objects.create(
                user=instance,
                auto_id=get_auto_id(Customer),
                creator=instance,
                updater=instance,

                name=name,
                location=location,
                latitude=latitude,
                longitude=longitude,
                phone=phone,
                otp=otp,
                password=encrypt_message(phone),
            )

            response = get_user_token(request, phone, phone)

            customer_instance = Customer.objects.get(phone=phone)
            user_serializer = CustomerSerializer(customer_instance, context={"request": request})

            response_data = {
                "StatusCode": 6000,
                "token": response.json(),
                "data": serialized.data,
                "user_details" : user_serializer.data,
                "otp": str(otp),
                "message": "Account Created Successfully"
            }
        else:
            response_data = {
                "StatusCode": 6001,
                "message": generate_serializer_errors(serialized._errors)
            }
    else:
        response_data = {
            "StatusCode": 6001,
            "message": message
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def register_number(request):
    """
    The first signup functions
    :param request:
    :return:
    """
    serialized = OtpVerifySerializer(data=request.data)
    s = request.data
    data = request.data
    phone = data['phone']

    if serialized.is_valid():
        otp = get_otp()
        sms_manager = SMS(phone)

        if Customer.objects.filter(phone=phone).exists():

            response_data = {
                "StatusCode": 6001,
                "message": "User Already Registered, Please Sign in"
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            sms_manager.send_otp(otp)
            if Otp.objects.filter(phone=phone).exists():
                serialized.updateOtp(phone,otp)
            else:
                serialized.save(otp=otp)

            response_data = {
                "StatusCode": 6000,
                'data': serialized.data,
                'otp': str(otp),
                "message": "OTP Sent Successfully"
            }

            return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode": 6001,
            "message": serialized.errors
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def verify_otp(request):
    serialized = OtpVerifySerializer(data=request.data)
    otp = serialized.verify_otp(request.data)
    if otp is True:
        response_data = {
            "StatusCode": 6000,
            "message": "OTP verified"
        }

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode": 6001,
            "message": "Invalid OTP or timeout"
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def send_otp(request):
    data = request.data
    phone = data['phone']
    new_otp = get_otp()

    sms_manager = SMS(phone)

    if Customer.objects.filter(phone=phone).exists():
        sms_manager.send_otp(new_otp)
        Customer.objects.filter(phone=phone).update(otp=new_otp)

        response_data = {
            "StatusCode": 6000,
            "otp": new_otp,
            "message": "OTP Send Successfully"
        }

        return Response(response_data, status=status.HTTP_200_OK)
    else:
        response_data = {
            "StatusCode": 6001,
            "message": "Phone Number not found"
        }

        return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def login_with_otp(request):
    data = request.data
    phone = data['phone']
    otp = data['otp']
    customer_instance = None

    if Customer.objects.filter(phone=phone).exists():
        customer_instance = Customer.objects.get(phone=phone)
    if customer_instance.otp == otp:
        # response = get_user_token(request, phone, phone)
        response = get_user_token(
            request, customer_instance.phone, decrypt_message(customer_instance.password))

        user_serializer = CustomerSerializer(customer_instance, context={"request": request})

        response_data = {
            "StatusCode": 6000,
            "user_details" : user_serializer.data,
            "token": response.json(),
            "message": "Successfully logged in"
        }

        return Response(response_data, status=status.HTTP_200_OK)

    else:
        response_data = {
            "StatusCode": 6001,
            "message": "Invalid OTP"
        }

        return Response(response_data, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes((AllowAny,))
# @renderer_classes((JSONRenderer,))
# def login_with_password(request):
#     data = request.data
#     username = data['phone']
#     password = data['password']
#     customer_instance = None
#     user = User.objects.get(username=username)

#     if Customer.objects.filter(phone=username).exists():
#         customer_instance = Customer.objects.get(phone=username)
#         if decrypt_message(customer_instance.password) == password :
#             # response = get_user_token(request, phone, phone)
#             response = get_user_token(
#                 request, customer_instance.phone, decrypt_message(customer_instance.password))

#             response_data = {
#                 "StatusCode": 6000,
#                 "token": response.json(),
#                 "message": "Successfully logged in"
#             }

#             return Response(response_data, status=status.HTTP_200_OK)

#         else:
#             response_data = {
#                 "StatusCode": 6001,
#                 "message": "Invalid Password"
#             }

#             return Response(response_data, status=status.HTTP_200_OK)

#     else:
#             response_data = {
#                 "StatusCode": 6001,
#                 "message": "Invalid Phone Number"
#             }

#             return Response(response_data, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes((AllowAny,))
# @renderer_classes((JSONRenderer,))
# def reset_password(request):
#     data = request.data
#     phone = data['phone']
#     new_password = data['password']

#     valid = validate_password(new_password)
#     if valid["error"] == False :

#         customer_instance = None
#         user = User.objects.get(username=phone)

#         if Customer.objects.filter(phone=phone).exists():
#             customer_instance = Customer.objects.get(phone=phone)
#             customer_instance.password = encrypt_message(new_password)
#             customer_instance.save()


#         user.set_password(new_password)
#         user.save()

#         response = get_user_token(request, customer_instance.phone, new_password)

#         response_data = {
#             "StatusCode": 6000,
#             "token": response.json(),
#             "message": "Password Successfully Resets "
#         }
#     else :
#         message = valid["message"]
#         response_data = {
#             "StatusCode": 6001,
#             "message": message,
#         }

#     return Response(response_data, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# @renderer_classes((JSONRenderer,))
# def change_password(request):
#     user = get_user(request.user)
#     req_user = User.objects.get(username=user.phone)

#     old_password = request.data['old_password']
#     new_password = request.data['new_password']
#     valid = validate_password(new_password)

#     if req_user.check_password(old_password):

#         if valid["error"] == False :

#             req_user.set_password(new_password)
#             req_user.save()

#             response_data = {
#                 "StatusCode": 6000,
#                 "message": "Password Changed Successfully"
#             }

#             return Response(response_data, status=status.HTTP_200_OK)

#         else :
#             message = valid["message"]
#             response_data = {
#                 "StatusCode": 6001,
#                 "message": message,
#             }

#             return Response(response_data, status=status.HTTP_200_OK)
#     else:
#         response_data = {
#             "StatusCode": 6001,
#             "message": "Invalid Existing Password"
#         }

#         return Response(response_data, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# @renderer_classes((JSONRenderer,))
# def change_number(request):
#     user = get_user(request.user)
#     req_user = User.objects.get(username=user.phone)
#     old_phone = Customer.objects.get(phone=user.phone)
#     new_phone = request.data['new_phone']

#     if Otp.objects.filter(phone=new_phone).exists():
#         new_otp = get_otp()
#         Otp.objects.filter(phone=new_phone).update(otp=new_otp)
#     else:
#         otp = get_otp()
#         Otp.objects.create(phone=new_phone, otp=otp)

#     old_phone_otp = get_otp()
#     Customer.objects.filter(phone=old_phone.phone).update(otp=old_phone_otp)

#     response_data = {
#         "StatusCode": 6000,
#         "message": "OTP sended"
#     }

#     return Response(response_data, status=status.HTTP_200_OK)


# @api_view(['POST'])
# @permission_classes((IsAuthenticated,))
# @renderer_classes((JSONRenderer,))
# def change_number_update(request):
#     message = ""
#     error = False

#     user = get_user(request.user)
#     req_user = User.objects.get(username=user.phone)
#     old_phone = Customer.objects.get(phone=user.phone)

#     new_phone = request.data['new_phone']
#     new_phone_instance = Otp.objects.get(phone=new_phone)

#     data = request.data
#     new_otp = data['new_otp']
#     old_otp = data['old_otp']
#     password = data['password']

#     old_phone_otp = old_phone.otp
#     new_phone_otp = new_phone_instance.otp

#     if new_otp != new_phone_otp:
#         error = True
#         message += "OTP incorrect " + new_phone

#     if old_phone_otp != old_otp:
#         error = True
#         message += "OTP incorrect " + old_phone.phone

#     if password != decrypt_message(old_phone.password):
#         error = True
#         message += "Invalid Password"

#     if not error:
#         Customer.objects.filter(phone=user.phone).update(phone=new_phone)
#         req_user.username = new_phone
#         req_user.save()

#         response_data = {
#             "StatusCode": 6000,
#             "message": "Phone Number Updated"
#         }

#         return Response(response_data, status=status.HTTP_200_OK)
#     else:

#         response_data = {
#             "StatusCode": 6001,
#             "message": message
#         }

#         return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def get_profile(request):
    user = get_user(request.user)
    instances = None
    if Customer.objects.filter(phone=user).exists():
        instances = Customer.objects.get(phone=user)

    serialized = CustomerSerializer(instances, context={"request": request})

    response_data = {
        "StatusCode": 6000,
        "data": serialized.data
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def check_email(request):
    user = get_user(request.user)
    email = request.data['email']
    new_otp = get_otp()

    if OtpMail.objects.filter(email=email).exists():
        OtpMail.objects.filter(email=email).update(otp=new_otp)
    else:
        OtpMail.objects.create(email=email, otp=new_otp)

    message = f"Dear customer, {new_otp} is your OTP from GUESTER. Don't share your OTP with anyone."

    send_email("GUESTER user varification",email,message)

    response_data = {
        "StatusCode": 6000,
        "message": "OTP sended to the mail"
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def verify_email(request):
    email = request.data['email']
    otp = request.data['otp']

    if OtpMail.objects.filter(email=email).exists() :
        if OtpMail.objects.filter(email=email,otp=otp).exists():
            response_data = {
                "StatusCode": 6000,
                "message": "Email Verified",
                "Verified": True,
            }
        else:
            response_data = {
                "StatusCode": 6001,
                "message": "Invalid OTP",
                "Verified": False,
            }
    else:
        response_data = {
        "StatusCode": 6001,
        "message": "Invalid Email ID"
    }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def update_profile(request):
    try:
        name = request.data['name']
    except:
        name = ""
    try:
        email = request.data['email']
    except:
        email = ""

    # print(name)
    # print(email)
    if not name == "" :
        if email != "" :
            Customer.objects.filter(user=request.user).update(name=name,email=email)
        else :
            Customer.objects.filter(user=request.user).update(name=name)

        response_data = {
            "StatusCode": 6000,
            "message": "Profile Updated"
        }
    else :
        response_data = {
            "StatusCode": 6001,
            "message": "Enter Your Name"
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes((IsAuthenticated,))
@renderer_classes((JSONRenderer,))
def update_profile_image(request):
    image = request.data['photo']
    # print(image)
    try:
        image = ContentFile(base64.b64decode(image), name="image.png")
        request.data["photo"] = image
    except:
        pass

    # Save and take image uri
    if (image):
        name = request.data["photo"].name
        fs = FileSystemStorage()
        # print(type(fs.base_location),"--fs.base_location")

        fs.base_location = f"{fs.base_location}/Customer/profile/"
        filename = fs.save(name, image)
        uploaded_file_url = 'Customer/profile/' + filename

    else:
        uploaded_file_url = ""

    # print(image,"---image")

    if Customer.objects.filter(user=request.user).exists():
        Customer.objects.filter(user=request.user,is_deleted=False).update(photo=uploaded_file_url)

        instances = Customer.objects.get(user=request.user,is_deleted=False)
        serialized = ProfileImageSerializer(instances, context={"request": request})

    response_data = {
        "StatusCode": 6000,
        "message": "Profile pic updated",
        "data": serialized.data,
    }

    return Response(response_data, status=status.HTTP_200_OK)