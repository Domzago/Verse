from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login

from chat.models import Item, Chat, Chatext
from chat.forms import ItemForm, ChatextForm, ProfileForm, ProfileIForm

def home(request):
    p = Paginator(Item.objects.all(), 8)
    page = request.GET.get('page')
    items = p.get_page(page)

    search = request.GET.get('search')

    if search:
        items = Item.objects.filter(Q(name__icontains = search) | Q(description__icontains = search))
    return render(request, 'home.html', {'items':items, 'search':search})


def detailitem(request, pk):
    item = get_object_or_404(Item, pk=pk)
    return render(request, 'detail.html', {'item':item})

@login_required
def createitem(request):
    form = ItemForm()
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)

        if form.is_valid():
            item = form.save(commit=False)
            item.created_by = request.user
            item.save()
            messages.success(request, 'Your Item was created successfully')
            return redirect('home')
    else:
        form = ItemForm()
    return render(request, 'create.html', {'form':form})

@login_required
def updateitem(request, pk):
    item = get_object_or_404(Item, pk=pk)
    form = ItemForm()

    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES, instance=item)

        if form.is_valid():
            form.save()
            messages.success(request, 'Your Item was updated successfully')
            return redirect('detail', pk=pk)
    else:
        form = ItemForm(instance=item)
    return render(request, 'update.html', {'item':item, 'form':form})


@login_required
def deleteitem(request, pk):
    item = get_object_or_404(Item, pk=pk)

    if request.method == 'POST':
        item.delete()
        messages.success(request, 'The Item was deleted')
        return redirect('home')
    return render(request, 'delete.html', {'item':item})

def signup(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, f'Hello {username} welcome to Verse')
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form':form})

def loginuser(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back {username}')
            return redirect('home')
    return render(request, 'login.html')

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = ProfileForm(request.POST, instance=request.user)
        p_form = ProfileIForm(request.POST, request.FILES, instance=request.user)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account was updated successfully')
            return redirect('profile')
    else:
        u_form = ProfileForm(instance=request.user)
        p_form = ProfileIForm(instance=request.user)

    return render(request, 'profile.html', {'u_form':u_form, 'p_form': p_form})

@login_required
def newchat(request, item_pk):
    item = get_object_or_404(Item, pk=item_pk)

    if request.user == item.created_by:
        return redirect('home')

    chats = Chat.objects.filter(item=item).filter(members__in=[request.user.id])

    if chats:
        return redirect('detailchat', pk=chats.first().id)

    
    if request.method == 'POST':
        form = ChatextForm(request.POST)

        if form.is_valid():
            chat = Chat.objects.create(item=item)
            chat.members.add(request.user)
            chat.members.add(item.created_by)
            chat.save()

            chat_message = form.save(commit=False)
            chat_message.chat = chat
            chat_message.created_by = request.user
            chat_message.save()
            return redirect('detail', pk=item_pk)
        
    else:
        form = ChatextForm()
    return render(request, 'newchat.html', {'form':form, 'item':item})


def inbox(request):
    chats = Chat.objects.filter(members__in=[request.user.id])
    return render(request, 'inbox.html', {'chats':chats})

def detailchat(request, pk):
    chat = Chat.objects.filter(members__in=[request.user.id]).get(pk=pk)
    form = ChatextForm()

    if request.method == 'POST':
        form = ChatextForm(request.POST, request.FILES)
        if form.is_valid():
            chat_message = form.save(commit=False)
            chat_message.chat = chat
            chat_message.created_by = request.user
            chat_message.save()

            chat.save()
            return redirect('detailchat', pk=pk)
    return render(request, 'detailchat.html', {'form':form, 'chat':chat})