# from users.models import Notification
from main.functions import get_current_role
import datetime



def main_context(request):
    today = datetime.date.today()
    # if get_current_role(request)=='shop_admin':
    #     current_role = "shop-admin"
        
    current_role = get_current_role(request)  
    
    if current_role == 'superadmin':
        user_type = 'Admin User'
    elif current_role == 'shop_admin':
        user_type = 'Shop User'
        current_role = "shop-admin"
    else :
        user_type = 'user'

    is_superuser = False
    if "set_user_timezone" in request.session:
        user_session_ok = True
        user_time_zone = request.session['set_user_timezone']
    else:
        user_session_ok = False
        user_time_zone = "Asia/Kolkata"


    active_parent = request.GET.get('active_parent')
    active = request.GET.get('active')

    return {
        'current_role': current_role,
        'user_type': user_type,
        "user_session_ok" : user_session_ok,
        "user_time_zone" : user_time_zone,
        "confirm_delete_message" : "Are you sure want to delete this item. All associated data may be removed.",
        "confirm_verify_message" : "Are you sure want to verify this item.",
        "revoke_access_message" : "Are you sure to revoke this user's login access",
        "grant_access_message" : "Are you sure to grant this user's login access",
        "confirm_shop_delete_message" : "Your shop will deleted permanently. All data will lost.",
        "confirm_delete_selected_message" : "Are you sure to delete all selected items.",
        "confirm_read_message" : "Are you sure want to mark as read this item.",
        "confirm_read_selected_message" : "Are you sure to mark as read all selected items.",
        'domain' : request.META['HTTP_HOST'],
        "active_parent" : active_parent,
        "active_menu" : active,
    }