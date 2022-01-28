from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .utils import token_required
from .views_utils import *


# Create your views here.

@csrf_exempt
@token_required
def collection_get_post(request, user):
    if request.method == 'GET':
        return handle_get_all_collections(request, user)
    elif request.method == 'POST':
        return handle_post_collection(request, user)
       
@csrf_exempt
@token_required
def collection_get_delete(request, user, id):
    if request.method == 'DELETE':
        return handle_delete_collection(request, user, id)
    elif request.method == 'PUT':
        return handle_put(request, user, id)
    elif request.method == 'GET':
        return handle_get_single_collection(request, user, id)
        

@csrf_exempt    
def register(request):
    return handle_register_user(request)
    
@token_required
def get_movies(request, user):
    return handle_get_movies(request, user)




       

