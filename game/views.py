from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from game.models import Room, RoomLobby

# Create your views here.

def index(request):
    return render(request, 'index.html')

def login_view(request):
    if request.session.has_key('username'):
        return redirect('/game/home/')
    elif request.method == "POST":
        username = request.POST.get('email')
        password = request.POST.get('password')

        print(username)
        print(password)

        user = authenticate(username=username, password=password)
        if user is not None:
            print("logged in successfully")
            login(request, user)
            request.session['username'] = username
            return redirect('/game/home/')
            # messages.success(request, "Loggedin successfully")
        else:
            messages.success(request, "Invalid username or Password")

    return render(request, 'login.html')

def register_view(request):
    if request.session.has_key('username'):
        return redirect('/game/home/')
    elif request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        username = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        print(firstname, lastname, username, password, confirm_password)

        User = get_user_model()
        user = User.objects.filter(username=username)
        print(user)
        if len(user) > 0:
            print("Email already registered!!")
            messages.success(request, "Email already registered!!")
        else:
            if password == confirm_password:
                print("Registration Successful")
                user = User.objects.create_user(username=username, first_name=firstname, last_name=lastname, email=username, password=password)
                user.save()
                return redirect('/game/login/')
            else:
                print("password mis-match")
                messages.success(request, "Password Mis-match!!")

    return render(request, 'register.html')

@login_required(login_url='/game/login/')
def home_view(request):
    username = request.session.get('username')
    print(username)
    if request.method == "POST":
        room_event = request.POST.get('event')
        room_code = request.POST.get('room_code')
        room_size = request.POST.get('room_size')
        print(room_code)
        print(room_event)
        if room_event == "Create":
            existing_room = Room.objects.filter(room_code=room_code)
            if len(existing_room) == 0:
                print(f"Room : {room_code}Created Successfully")
                room = Room(room_code=room_code, room_host=username, room_size=room_size)
                room.save()
                roomlobby = RoomLobby(room=room, room_code=room_code, room_user=username, score=0, is_online=False, user_id=0)
                roomlobby.save()
                return redirect('/game/play/' + room_code)
            else:
                print("Room code already existed!! Create a new one.")
                messages.success(request, "Room code already existed!! Create a new one.")
        elif room_event == "Join":  
            existing_room = Room.objects.filter(room_code=room_code)
            if len(existing_room) == 0:
                print(f"No such room_code : {room_code} exists!!")
                messages.success(request, "No such room_code exists!!")
            elif existing_room[0].game_started == True:
                messages.success(request, "Game has been started!! You can't join in between!!")
            else:
                room_user_existed = RoomLobby.objects.filter(room_code=room_code, room_user=username)
                if len(room_user_existed) == 0:
                    room_users = RoomLobby.objects.filter(room_code=room_code)
                    room_size = Room.objects.filter(room_code=room_code)[0].room_size
                    if len(room_users) < room_size:
                        roomlobby = RoomLobby(room=existing_room[0], room_code=room_code, room_user=username, score=0, is_online=False, user_id=len(room_users))
                        roomlobby.save()
                        print(f"Room : {room_code} joined successfully!")
                        return redirect('/game/play/' + room_code)
                    else:
                        messages.success(request, "room is full!! Join another room.")
                        print("room is full!! Join another room.")        
                else:
                    print(f"Room : {room_code} joined successfully!")
                    return redirect('/game/play/' + room_code)

    context = {'username' : username}
    return render(request, 'home.html', context)

@login_required(login_url='/game/login/')
def play_view(request, room_code):
    room = Room.objects.filter(room_code=room_code)[0]
    username = request.session['username']
    room_host = room.room_host
    roomlobby = RoomLobby.objects.filter(room_code=room_code, room_user=username)[0]
    user_id = roomlobby.user_id
    if room.game_started == True:
        if roomlobby.is_online == True:
            roomlobby.is_online = False
            roomlobby.save()
        return redirect('/game/home/')
    
    context = {'room_code' : room_code, 'room_host' : room_host, 'username' : username, 'user_id' : user_id}
    return render(request, 'play.html', context)

def logout_view(request):
    logout(request)
    return redirect('/game/login/')
