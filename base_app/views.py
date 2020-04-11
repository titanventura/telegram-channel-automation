from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required,user_passes_test
from base_app.models import UserRecord
from django.shortcuts import get_object_or_404
import asyncio
#from telethon.tl.functions.users import GetFullUserRequest
from telethon import TelegramClient
from telethon.tl.types import InputPhoneContact
#from telethon.tl.types import InputPeerChannel, InputPeerEmpty, InputPeerUser, InputPhoneContact, PeerUser
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
#from telethon.tl.functions.channels import InviteToChannelRequest
from django.db.models import Q
from django.contrib import messages
import datetime
import os
from django.contrib.auth import logout
from base_app.permissions import check_viewing_rights_admin


loop = asyncio.get_event_loop()
api_id = 1238868 #Telegram Admin ID
api_hash = "299435e6d3e9689589180dd71beb06e8"
ph_no = "9488006888"

async def get_client():

    client = TelegramClient(f"+91{ph_no}",api_id=api_id,api_hash=api_hash)
    await client.connect()
    flag = await client.is_user_authorized()
    if flag:
        return (client,True)
    
    return (client,False)

async def send_code(ph_no):
    client = TelegramClient(f"+91{ph_no}",api_id=api_id,api_hash=api_hash)
    await client.connect()
    auth_client = await client.is_user_authorized()
    print(auth_client)
    if not auth_client:
        sent = await client.send_code_request(f"+91{ph_no}")
        return sent.phone_code_hash



@login_required(login_url="/")
def home(request):
    if request.method == "POST":
        telegram_number = request.POST["telegram_number"]
        try:
            hash = loop.run_until_complete(send_code(telegram_number))
            request.session["hash"] = hash
        except Exception as e:
            print(e)
            return HttpResponse("<center><h1>The Number does not have an associated telegram account. Please Verify. </h1></center>")
        return render(request,"base_app/code_validator.html",{'num':telegram_number})

    if request.user.is_authenticated:
        try:
            record = get_object_or_404(UserRecord,email=request.user.email)
            if str(record.time_added_to_group) != "2001-03-18 18:30:00+00:00":
                if request.user.groups.filter(name='Admin').exists():
                    return redirect('/view')
                logout(request)
                messages.error(request, "Already added to group")
                messages.warning(request, "Logged out successfully")
                return redirect('/')
            if str(record.time_registered) != "2001-03-18 18:30:00+00:00":
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


async def verify_code(phone,pin,hash,password):
    client = TelegramClient(f"+91{phone}",api_id=api_id,api_hash=api_hash)
    await client.connect()
    flag = await client.is_user_authorized()
    if not flag:
        if password != "" and password != None:
            await client.sign_in(f"+91{phone}",pin,phone_code_hash=hash,password=password)
        else:
            await client.sign_in(f"+91{phone}",pin,phone_code_hash=hash)

    try:
        contact = InputPhoneContact(client_id=0, phone=f"+91{ph_no}",
        first_name="KCT_TELEGRAM_BOT_2.0",last_name="")
        await client(ImportContactsRequest([contact]))
        await client(ImportChatInviteRequest('AAAAAFQEmxBonLdyQvsvGQ'))
        await client.disconnect()

        print(os.listdir())
        os.remove(os.getcwd()+'/'+f"+91{phone}.session")
        print(os.listdir())
        return True
    except Exception as e:
        print(e)
        return False




@login_required(login_url="/")
def verify(request):
    if request.method == "POST":
        pin = request.POST["OTP"]
        phone = request.POST["ph_num"]
        hash = request.session["hash"]
        password = request.POST["password"]
        flag = loop.run_until_complete(verify_code(phone,pin,hash,password))
        user_record_obj = UserRecord.objects.get(id=request.user.userrecord.id)
        user_record_obj.telegram_number = f"+91{phone}"
        user_record_obj.time_registered = datetime.datetime.now()
        user_record_obj.time_added_to_group = datetime.datetime.now()
        user_record_obj.is_added_to_group = True
        user_record_obj.save()
        logout(request)
        return render(request,"base_app/notify_user.html",{})

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
    print(registered_records)
    unregistered_records = UserRecord.objects.filter(Q(user=None) | Q(telegram_number=None) | Q(telegram_number=''))
    return render(request,'base_app/view.html',{'added_records':added_records,"registered_records":registered_records,"unregistered_records":unregistered_records})



