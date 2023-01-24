from mailqueue.models import MailerMessage

from guester import settings
from general.models import Location


def get_auto_id(model):
    auto_id = 1
    latest_auto_id =  model.objects.all().order_by("-auto_id").first() if model.objects.exists() else None
    if latest_auto_id:
        auto_id = latest_auto_id.auto_id + 1
    return auto_id


def get_or_create_location(request,location_form, location_name, latitude, longitude):
    # try:
    if Location.objects.filter(location=location_name,latitude=latitude,longitude=longitude).exists():
        location = Location.objects.filter(location=location_name,latitude=latitude,longitude=longitude)[0]
    else:
        short_location = location_name.split(",")
        short_name = short_location[0]
        location = location_form.save(commit=False)
        location.creator = request.user
        location.updater = request.user
        location.auto_id = get_auto_id(Location)
        location.short_name = short_name
        location.save()
    # except:
        # location = None

    return location


def validate_password(password):
        
        special_symbols =['$', '@', '#', '%']
        
        if len(password) < 8:
                message = 'Password must have at least 8 characters.'
                print(message)
                return {
                    "error" : True,
                    "message" : message,
                }
                
        if len(password) > 20:
                message = 'Password cannot have more than 20 characters.'
                return
        
        if not any(characters.isdigit() for characters in password):
                message = 'Password must have at least one numeric character.'
                return {
                    "error" : True,
                    "message" : message,
                }
                
        if not any(characters.isupper() for characters in password):
                message = 'Password must have at least one uppercase character'
                return {
                    "error" : True,
                    "message" : message,
                }
        
        if not any(characters.islower() for characters in password):
                message = 'Password must have at least one lowercase character'
                return {
                    "error" : True,
                    "message" : message,
                }
                
        if not any(characters in special_symbols for characters in password):
                message = 'Password should have at least one of the symbols $@#%'
                return {
                    "error" : True,
                    "message" : message,
                }
        else:
            message = "Password is Valid."
            
            return {
                    "error" : False,
                    "message" : message,
                }
            
            
def send_email(subject,to_address,content,bcc_address=settings.DEFAULT_BCC_EMAIL,app="guester",reply_to_address=settings.DEFAULT_REPLY_TO_EMAIL,attachment=None):
    # print("send fun")
    new_message = MailerMessage()
    new_message.subject = subject
    new_message.to_address = to_address
    if bcc_address:
        new_message.bcc_address = bcc_address
    new_message.from_address = settings.DEFAULT_FROM_EMAIL
    new_message.content = content
    # new_message.html_content = html_content
    new_message.app = app
    if attachment:
        new_message.add_attachment(attachment)
    new_message.reply_to = reply_to_address
    new_message.save()