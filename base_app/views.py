from django.shortcuts import render,redirect,HttpResponse
import json
from django.contrib.auth.decorators import login_required,user_passes_test
from base_app.models import UserRecord
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages
import datetime
from django.contrib.auth import logout,authenticate,login
from base_app.permissions import check_viewing_rights_admin
import asyncio
from base_app.tasks import send_code,verify_code
from django.contrib.auth.models import User
import random
from django.core.files.storage import FileSystemStorage
import csv,os

@login_required(login_url="/")
def home(request):
    if request.method == "POST":
        telegram_number = request.POST['countryCode']+request.POST["telegram_number"]
        user_record = request.user.userrecord
        err,hash = asyncio.run(send_code(request,telegram_number))
        if err=='':
            request.session["hash"] = hash
            return render(request, "base_app/code_validator.html", {'num': telegram_number})
        else:
            user_record.reason_for_error = err
            user_record.save()
            if hash == 'register':
                return redirect('register')
            if hash == 'logout':
                return redirect('logout')
            if hash == 'unknown':
                return redirect('register')

    if request.user.is_authenticated:
        try:
            record = get_object_or_404(UserRecord,email=request.user.email)
            if record.time_added_to_group:
                if request.user.groups.filter(name='Admin').exists():
                    return redirect('/view')
                logout(request)
                messages.error(request, "Already added to group")
                messages.warning(request, "Logged out successfully")
                return redirect('/')
            if record.time_registered:
                if request.user.groups.filter(name='Admin').exists():
                    return redirect('/view')
                logout(request)
                messages.warning(request,"Logging out...")
                return render(request, "base_app/notify_user.html", {})
            if not record.user:
                record.user = request.user
                record.save()
            context = {"name": record.name, "email": record.email, "phone": record.phone,"is_authorized":True}
        except Exception as e:
            context = {"is_authorized":False}
    else:
         context = {"is_authorized":False}
    return render(request, "base_app/index.html", context)

@login_required(login_url="/")
def verify(request):
    if request.method == "POST":
        pin = request.POST["OTP"]
        phone = request.POST["ph_num"]
        hash = request.session["hash"]
        password = request.POST["password"]
        user_record_obj = UserRecord.objects.get(id=request.user.userrecord.id)
        flag = asyncio.run(verify_code(request,phone,pin,hash,password))

        if flag[0] == '' and flag[1] == True:
            user_record_obj.telegram_number = phone
            user_record_obj.time_registered = datetime.datetime.now()
            user_record_obj.time_added_to_group = datetime.datetime.now()
            user_record_obj.is_added_to_group = True
            user_record_obj.save()
            logout(request)


        if flag[1] == 'logout':
            user_record_obj.reason_for_error = flag[0]
            user_record_obj.save()
            logout(request)

        if flag[1] == 'register':
            user_record_obj.reason_for_error = flag[0]
            user_record_obj.save()
            return redirect('register')


        if flag[1] == 'verify':
            user_record_obj.reason_for_error = flag[0]
            user_record_obj.save()
            return render(request, "base_app/code_validator.html", {'num': phone})


        if flag[1]=='retry':
            flag2 = asyncio.run(verify_code(request, phone, pin, hash, password))
            if flag2[1] == 'logout':
                user_record_obj.reason_for_error = flag2[0]
                user_record_obj.save()
                return redirect('logout')
            if flag2[1] == 'register':
                user_record_obj.reason_for_error = flag2[0]
                user_record_obj.save()
                return redirect('register')
            if flag2[1] == True:
                user_record_obj.telegram_number = f"+91{phone}"
                user_record_obj.time_registered = datetime.datetime.now()
                user_record_obj.time_added_to_group = datetime.datetime.now()
                user_record_obj.is_added_to_group = True
                user_record_obj.save()
                logout(request)
            else:
                user_record_obj.reason_for_error = flag2[0]
                user_record_obj.save()
                return render(request, "base_app/error.html")


        if flag[1] ==False:
            return render(request,"base_app/error.html")
        return render(request,"base_app/notify_user.html",{})
    else:
        return HttpResponse('<b>GET not allowed for this url.</b>')

@login_required(login_url="/")
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("/")


@login_required(login_url="/")
@user_passes_test(check_viewing_rights_admin)
def view(request):
    added_records = UserRecord.objects.filter(is_added_to_group=True)
    registered_records = UserRecord.objects.filter(
        ~Q(telegram_number='') & ~Q(telegram_number=None) & Q(is_added_to_group=False))
    unregistered_records = UserRecord.objects.filter(Q(user=None) | Q(telegram_number=None) | Q(telegram_number=''))
    return render(request,'base_app/view.html',{'added_records':added_records,"registered_records":registered_records,"unregistered_records":unregistered_records})


@login_required(login_url="/")
@user_passes_test(check_viewing_rights_admin)
def check_errors(request):
    error_records = UserRecord.objects.filter(Q(is_added_to_group=False) & ~Q(reason_for_error=''))
    return render(request,'base_app/error_view.html',{'error_records':error_records})


def check_user(request):
    if(request.method == "GET"):
        email = request.GET["email"]
        if(User.objects.filter(email=email).exists()):
            return HttpResponse(json.dumps({'message':'exists'}), content_type='application/json')
        return HttpResponse(json.dumps({'message':'does_not_exist'}), content_type='application/json')

def login_user(request):
    if request.method=='POST':
        email = request.POST['email']
        pwd = request.POST['pwd']
        user_username = User.objects.get(email=email).username
        user = authenticate(request,username=user_username,password=pwd)
        if user:
            login(request,user)
            messages.success(request,"Successfully logged in.")
            return redirect('/home')
        else:
            messages.error(request,"Invalid Credentials.")
            return redirect('/')

def register_user(request):
    if request.method=='POST':
        email = request.POST['email']
        pwd1 = request.POST['password1']
        pwd2 = request.POST['password2']
        if pwd1 == pwd2:
            try:
                user = User(username=email.split('@')[0],email=email)
                user.set_password(pwd1)
                user.save()
            except:
                user = User(username=email.split('@')[0]+random.randint(1,10), email=email)
                user.set_password(pwd1)
                user.save()
            finally:
                messages.success(request, "Successfully registered.")
                return redirect('/home')
        else:
                messages.error(request,"Passwords dont match")
                return redirect('/')

@user_passes_test(check_viewing_rights_admin)
def import_users(request):
    if request.method == 'POST' and request.FILES['file']:
        file = request.FILES['file']
        if str(file).endswith('.csv'):
            fs = FileSystemStorage()
            fname = random.randint(1,10000)
            fs.save(f'{fname}.csv', file)
            try:
                input_file = csv.DictReader(open(f"media/{fname}.csv"))
                records = list(input_file)
                for record in records:
                    try:
                        UserRecord.objects.create(name=record['name'], phone=record['phone'], email=record['email'])
                    except Exception as e:
                        messages.error(request,"Error adding "+record['email']+" "+str(e))
                messages.success(request, 'Users added successfully')
            except:
                messages.error(request,'Please check the csv file has the correct fields.')
            finally:
                del input_file
                try:
                    os.remove(f'media/{fname}.csv')
                except Exception as e:
                    print(e)

        else:
            messages.error(request,'Please import a csv file')
    return render(request, 'base_app/import_users.html')