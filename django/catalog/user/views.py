from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
# Create your views here.

def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            messages.add_message(request,messages.SUCCESS,'Login Success')
            return redirect('index')
        else:
            messages.add_message(request,messages.ERROR,'Bilgiler Hatalı!')
            return redirect('login')
        

    else:
        return render(request, "user/login.html")

def register(request):

    if request.method == 'POST':

        #get form values
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        repassword = request.POST['repassword']

        if password == repassword:
            # username
            if User.objects.filter(username = username).exists():
                messages.add_message(request,messages.WARNING,'Bu kullanıcı adı zaten alınmış.')
                return redirect('register')
            else:
                if User.objects.filter(email = email).exists():
                    messages.add_message(request,messages.WARNING,'Bu E-Mail kayıtlı bir kullanıcıya ait!')
                    return redirect('register')
                else:
                    #her şey yolunda
                    user = User.objects.create_user(username=username,password=password,email=email)
                    user.save()
                    messages.add_message(request,messages.WARNING,'Kullanıcı oluşturuldu')
                    return redirect('login')

        else:
            print('Parolalar Eşleşmiyor')
            return redirect('register')
    else:
        return render(request, "user/register.html")

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        messages.add_message(request,messages.SUCCESS,"Oturum kapatıldı.")
        return redirect("index")