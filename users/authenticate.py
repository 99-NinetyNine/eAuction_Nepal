from django.conf import settings

class EmailAuthbackend(object):
    def authenticate(self, username=None, password=None):
        """ authenticate usgin phone number(verified) and email(verified during signup process)"""
    
        user = settings.AUTH_USER_MODEL.objects.get(email=username)
        if(user): 
            if(user.check_password(password)):
                return user
            return None
        else:
            user = settings.AUTH_USER_MODEL.objects.get(phone_num=username)
            if(user):
                if(user.has_verified_phone() and user.check_password(password)):
                    return user
                return None
        return None

    
    def get_user(self, user_id):
        try:
            return settings.AUTH_USER_MODEL.objects.get(pk=user_id)
        except user.DoesNotExist:
            return None