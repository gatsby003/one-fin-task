from .models import AppUser
from django.http import JsonResponse
import jwt

key = 'secretblabla'

def token_required(func):
    def main(request, *args, **kwargs):
        try:
            token = request.META['HTTP_AUTHORIZATION']
            obj = jwt.decode(token[7:], key=key,algorithms=['HS256'])
            user = AppUser.objects.filter(name=obj['name'])[0]
            if user :
                return func(request, user, *args, **kwargs)
            else:
                return JsonResponse(data={
                    "is_success" : False,
                    "reason" : "invalid token"
                })
        except:
            return JsonResponse(data={
                "is_success" : False,
                "reason" : "failed to validate token or no token sent"
            })
    return main 

