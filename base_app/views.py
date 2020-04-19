from django.shortcuts import render,redirect,HttpResponse
import json
from django.contrib.auth.decorators import login_required,user_passes_test
from base_app.models import UserRecord
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib import messages
import datetime
from django.contrib.auth import logout
from base_app.permissions import check_viewing_rights_admin
import asyncio
from base_app.tasks import send_code,verify_code
from django.contrib.auth.models import User

@login_required(login_url="/")
def home(request):
    if request.method == "POST":
        telegram_number = request.POST["telegram_number"]
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
            if not record.time_added_to_group:
                if request.user.groups.filter(name='Admin').exists():
                    return redirect('/view')
                logout(request)
                messages.error(request, "Already added to group")
                messages.warning(request, "Logged out successfully")
                return redirect('/')
            if not record.time_registered:
                if request.user.groups.filter(name='Admin').exists():
                    return redirect('/view')
                logout(request)
                messages.warning(request,"Logging out...")
                return render(request, "base_app/notify_user.html", {})
            if not record.user:
                record.user = request.user
                record.save()
            context = {"name": record.name, "rollno": record.rollno,
                    "email": record.email, "phone": record.phone,"is_authorized":True}
        except:
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
            user_record_obj.telegram_number = f"+91{phone}"
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