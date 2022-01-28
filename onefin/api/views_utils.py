from .models import Collection, AppUser
from rest_framework.parsers import JSONParser
from requests.auth import HTTPBasicAuth

from django.contrib.auth.hashers import make_password
from .serializers import CollectionSerializer, UserSerializer
from django.http import JsonResponse

import jwt

from urllib import parse

import requests

key = 'secretblabla'

def handle_get_all_collections(request, user):
    try:
        collections = Collection.objects.filter(user=user)
        serializer = CollectionSerializer(collections, many=True)

        # finding top three genres and deleting movies field  
        genres = []
        for coll in serializer.data:
            print(coll)
            for movie in coll['movies']:
                genres += movie['genres']
            del coll['movies']
        
        genre_count = {}
        for genre in set(genres):
            genre_count[genre] = genres.count(genre)  
        

        genres = sorted(genre_count, key=genre_count.get, reverse=True)[:3]

        res = {
            "is_success" : True,
            "data" : serializer.data,
            "favorite_genres" : ",".join(genres)
        }

        return JsonResponse(res, safe=False)
    except:
        return JsonResponse(data={"is_success" : Fail})

def handle_post_collection(request, user):
    try:
        data = JSONParser().parse(request)
        serializer = CollectionSerializer(data = data)
        coll_data = dict(serializer.initial_data)

        for movie in coll_data['movies']:
            if (movie['genres']):
                movie['genres'] = movie['genres'].split(",")

        if serializer.is_valid():
            serializer.save(user=user)
            return JsonResponse(serializer.data, status=201)
        else :
            return JsonResponse(data={"is_success" : False},status=400)
    except:
        return JsonResponse(data={"is_success" : False})

def handle_delete_collection(request, user, id):
    try:
        collection = Collection.objects.filter(pk=id)
        coll = collection[0]
        if coll.user == user:
            coll.delete()
            return JsonResponse(data={"is_success" : True}, status=404)
    except:
        return JsonResponse(data={"is_success" : False})

def handle_put_collection(request, user, id):
    try :
        data = JSONParser().parse(request)
        serializer = CollectionSerializer(data = data)
        
        for movie in serializer.initial_data['movies']:
            if (movie['genres']):
                movie['genres'] = movie['genres'].split(",")

        if serializer.is_valid():
            obj, created = Collection.objects.update_or_create(
                uuid = id,
                defaults = {
                    "title" : serializer.data['title'],
                    "description" :serializer.data['description'],
                    "movies" : serializer.data['movies']
                },
            )
        return JsonResponse(data={"is_success" :  True}, status=202)
    except:
        return JsonResponse(data={"is_success" : True}, status=400)

def handle_get_single_collection(request, user, id):
    try:
        collection = Collection.objects.filter(pk=id)
        coll = collection[0]
        print(coll.title)
        if coll.user == user:
            serialized_obj = CollectionSerializer(collection[0])
            return JsonResponse(data={"is_success" : True, "data" : serialized_obj.data}, status=200)
        else:
            return JsonResponse(data={"is_success" : True})
    except:
        return JsonResponse(data={"is_success" : True, "reason" : "resource does not exist"})

def handle_register_user(request):
    try:
        data = JSONParser().parse(request)
        
        username = data['name']
        password = make_password(data['password'])
        
        user = AppUser.objects.filter(name = username)
        
        data['password'] = password
        
        serializer = UserSerializer(data = data)
        
        token = jwt.encode({
            'name' : serializer.initial_data['name'],

        }, key=key)
        
        if user :
            return JsonResponse(data={"is_success" : True, "token" : token})
        elif serializer.is_valid():
            return JsonResponse(data={"is_success" : True, "token" : token})
        else:
            return JsonResponse(data={"is_success" : False})
    except:
        return JsonResponse(data={"is_success" : False})

def handle_get_movies(request, user):
    try:
        page_no = request.GET.get('page', '')

        print(type(page_no))

        if (page_no == ''):
            page = ""
        else:
            page = "?page=" + request.GET.get('page', '')

        url = "https://demo.credy.in/api/v1/maya/movies/" + page

        print(url)
        
        username = "iNd3jDMYRKsN1pjQPMRz2nrq7N99q4Tsp9EY9cM0"
        password  = "Ne5DoTQt7p8qrgkPdtenTK8zd6MorcCR5vXZIJNfJwvfafZfcOs4reyasVYddTyXCz9hcL5FGGIVxw3q02ibnBLhblivqQTp4BIC93LZHj4OppuHQUzwugcYu7TIC5H1"
        response = requests.get(
            url,
            auth=HTTPBasicAuth(username, password)
        )

        res = response.json()

        base_url = "http://localhost:8000/api/movies/"

        if page_no == '':
            next_page = base_url + "?page=1"
            previous_page = None
        elif page_no == "1":
            next_page = base_url + "?page=2"
            previous_page = base_url
        else:
            next_page = base_url + "?page=" + str(int(page_no) + 1)
            previous_page = base_url + "?page=" + str(int(page_no) - 1) 


        res['next'] = next_page
        res['previous'] = previous_page

        return JsonResponse(res)
    except:
        return JsonResponse(data={"is_success" : False})
