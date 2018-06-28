from django.shortcuts import get_object_or_404, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.urls import reverse
from django.utils import timezone

from webchat.forms import RegForm , LoginForm ,InvateForm
from webchat.models import Profile , Rooms , Message , Invite


@login_required
def room(request):
    invites = Invite.objects.filter(recipient__user=request.user)
    rooms=Rooms.objects.filter(users__user = request.user, create_date__lte=timezone.now()).order_by('-create_date')
    return render(request, 'webchat/room.html', {'rooms':rooms, 'invites':invites})

def auth(request):
        if request.method == 'POST':
            form = LoginForm(request.POST)
            url = reverse('webchat:room')
            if form.is_valid():
                # if request.user.is_authenticated():
                #     logout(request)
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username = username, password = password)
                if user is not None:
                    print('lol')
                    login(request, user)
                    return HttpResponseRedirect(url)
                
            print(form.errors)
        else:
            form = LoginForm()
        return render(request, 'webchat/auth.html', {
            'form': form,
            # 'next': url
            })

def reg(request):
    if request.method == 'POST':
        form = RegForm(request.POST)
        if form.is_valid():
            form.save()

            url = reverse('webchat:room')
            return HttpResponseRedirect(url)
    else:
        form = RegForm()
    return render(request, 'webchat/registration.html', {'form' : form})

def mylogout(request):
    logout(request)
    url = reverse('webchat:auth')
    return HttpResponseRedirect(url)

def open_chat(request, pk):
    form = invite(request, pk)
    open_chat=get_object_or_404(Rooms, pk=pk )
    return render(request, 'webchat/index.html', { 'open_chat':open_chat , 'form':form })



def create_chat(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if name == '':
            return HttpResponseRedirect(reverse('webchat:room'))
        room = Rooms()
        room.admin = get_object_or_404(Profile, user=request.user)
        room.name = name
        room.save()

        room.users.add(get_object_or_404(Profile, user=request.user))
        room.save()

    return HttpResponseRedirect(reverse('webchat:open_chat', args=(room.pk,)))

def send_message(request, pk):
    if request.method == 'POST':
        room = get_object_or_404(Rooms, pk = pk)
        text = request.POST.get('text')
        if text == '':
            return HttpResponseRedirect(reverse('webchat:open_chat', args=(pk,)))
        message = Message()
        message.room = room
        message.text = text
        message.author = get_object_or_404(Profile, user = request.user)
        message.save()
    return HttpResponseRedirect(reverse('webchat:open_chat', args=(pk,))) 

def join(request, pk):
    room = get_object_or_404(Rooms, pk = pk)
    room.users.add(get_object_or_404(Profile, user=request.user))

    invite = Invite.objects.filter(room__pk=pk)
    invite.delete()

    return HttpResponseRedirect(reverse('webchat:open_chat', args=(pk,)))

def invite(request, pk):
    if request.method == 'POST':
        form = InvateForm(request.POST)
        if form.is_valid():
            form.save(request, pk)
            pass
    else:
        form = InvateForm()
    return form

# Create your views here.
