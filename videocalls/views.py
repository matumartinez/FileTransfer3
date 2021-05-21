from django.shortcuts import render, get_object_or_404, redirect
from .models import Videocall
import requests
from time import sleep
from threading import Thread

def videocall_index_view(request):
    queryset = Videocall.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "videocall/index.html", context)

def videocall_create():
    sleep(1)
    req = requests.get('http://<DIRECCIÓN_IP_RED_LOCAL>:3000/API')
    link = "http://localhost:3000/" + str(req.content).replace("b", "", 1).strip("'")

    new_call = Videocall(url=link)
    new_call.save()

def videocall_middleware(request):
    create = Thread(target=videocall_create)
    create.start()
    return redirect('http://localhost:3000')

def videocall_delete(request, data):
    obj = Videocall.objects.get(pk=data)
    url = obj.url
    obj.delete()
    return redirect(url)
