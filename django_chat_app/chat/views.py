from django.http.response import HttpResponseRedirect
from django.shortcuts import render, redirect
from .models import Chat, Message
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.core import serializers

@login_required(login_url='/login/')
def index(request):
    if request.method == 'POST':
        print("Received data " + request.POST['textmessage'])
        myChat = Chat.objects.get(id=1)
        new_message = Message.objects.create(text=request.POST['textmessage'], chat=myChat, author=request.user, receiver=request.user)
        serialized_obj = serializers.serialize('json', [new_message, ])
        #return JsonResponse(serialized_obj[1:-1], safe=False)
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'messages': chatMessages})


def login_view(request):
    redirect = request.GET.get('next')
    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))

        if user:
            login(request, user)
            return HttpResponseRedirect(request.POST.get('redirect'))
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
    return render(request, 'auth/login.html', {'redirect': redirect})


def register_view(request):
    if request.method == 'POST':
        userName = request.POST.get('username', None)
        userPass = request.POST.get('password', None)
        userPassConfirm = request.POST.get('password-confirm', None)
        userMail = request.POST.get('email', None)

        if userName and userPass and userPassConfirm and userPass == userPassConfirm:
            try:
                newUser = User.objects.create_user(username=userName, email=userMail, password=userPass)
                if newUser:
                    return redirect('/chat/')
                else:
                    return render(request, 'auth/register.html')
            except Exception as e:
                return render(request, 'auth/register.html', {'message': str(e)})
        else:
            return render(request, 'auth/register.html', {'wrongInsert': True})
    return render(request, 'auth/register.html')


def logout_view(request):
    logout(request)
    return redirect('/chat/')
