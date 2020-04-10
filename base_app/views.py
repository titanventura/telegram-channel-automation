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

# Create your views here.

loop = asyncio.get_event_loop()
api_id = 1238868 #Telegram Admin ID
api_hash = "299435e6d3e9689589180dd71beb06e8" #Telegram Admin Hash
ph_no = "9488006888"

async def get_client():

    client = TelegramClient(f"+91{ph_no}",api_id=api_id,api_hash=api_hash)
    await client.connect()
    flag = await client.is_user_authorized()
    if flag:
        return (client,True)
    
    return (client,False)

# async def get_user_details(ph_no,user):
#     try:
#         # client = TelegramClient(f"${}")
#         full = await client(GetFullUserRequest(f'+91{ph_no}'))
#         print(full.user)
#         if full != None:
#             return True
#         else:
#             return False
#     except Exception as e:
#             contact = InputPhoneContact(client_id=0, phone=f"+91{ph_no}",
#                                         first_name=f"{user.name}",last_name=f"{user.rollno}")
#             result = await client(ImportContactsRequest([contact]))
#             print(result[0].user)
#             return True
#     except Exception:
#         return False
#         # return False

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
        # request.session["user_record_id"] = request.user.id
        telegram_number = request.POST["telegram_number"]
        user_obj = request.user
        user_record = user_obj.userrecord
        # user_record.telegram_number = telegram_number
        # (client,flag) = loop.run_until_complete(get_client())
        # print(client)
        # print(flag)

        # means the admin in server has not logged in due to some session error.
        # if not flag:
        #     messages.error(request,'Server error.Contact admin.')
        #     return redirect("/home")

        # if(flag):
        #     user_exists = loop.run_until_complete(get_user_details(telegram_number,user_record))
        # else:
        #     return HttpResponse("<center><h1>Server down. Try after some time.</h1></center>")

        # if(user_exists):
        # if flaag is false add error message. haha flag can never be false... we have session file for admin here --<. i know, but stii do it . KKK
        try:
            hash = loop.run_until_complete(send_code(telegram_number))
            request.session["hash"] = hash
            # user_record.telegram_number = telegram_number
            # user_record.save()
        except Exception as e:
            print(e)
            return HttpResponse("<center><h1>The Number does not have an associated telegram account. Please Verify. </h1></center>")
            print(telegram_number)# ur brother number free ??
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


async def verify_code(phone,pin,hash):
    client = TelegramClient(f"+91{phone}",api_id=api_id,api_hash=api_hash)
    await client.connect()
    flag = await client.is_user_authorized()

    if not flag:
        await client.sign_in(f"+91{phone}",pin,phone_code_hash=hash)

    # if client.is_user_authorized():
    try:
        contact = InputPhoneContact(client_id=0, phone=f"+91{ph_no}",
        first_name="KCT_TELEGRAM_BOT_2.0",last_name="")
        result = await client(ImportContactsRequest([contact]))
        update = await client(ImportChatInviteRequest('AAAAAFQEmxBonLdyQvsvGQ'))
        # print(result[0].user)
        await client.disconnect()
        print(client.is_connected(),"client connection")
        os.chdir("D:\\Projects\\telegram\\aswath\\env\\Scripts\\telegram_users_add\\base_app")
        os.listdir()
        os.remove(f"+91{phone}.session")
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
        flag = loop.run_until_complete(verify_code(phone,pin,hash))
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
# async def sign_admin(pin,hash,client):
#     await client.sign_in(f"+91{ph_no}", pin, hash) # Ithu admin thane.. INtha contact la than add ayirkum contacts la athane...dok do session create agala
#
# async def add_contacts(client,contacts):
#     try:
#         telegram_channel = await client.get_entity("https://t.me/joinchat/AAAAAEJB9G7XKb3MklJWlg")
#
#     except Exception as e:
#         print("error here")
#         print(e)
#         return
#
#     print(telegram_channel)
#     for contact in contacts:
#         try:
#             await client(ImportContactsRequest([contact]))
#             full_user = await client(GetFullUserRequest(f"{contact.phone}"))
#             user_obj = full_user.user
#
#             try:
#                 await client(InviteToChannelRequest(telegram_channel, [user_obj]))
#             except Exception as e:
#                 print(1)
#                 print(e)
#             record = UserRecord.objects.get(telegram_number=contact.phone)
#             record.is_added_to_group = True
#             record.time_added_to_group = datetime.datetime.now()
#             record.save()
#         except Exception as e:
#             record = UserRecord.objects.get(telegram_number=contact.phone)
#             record.is_added_to_group = False
#             record.reason_for_error = str(e)
#             full_user = await client(GetFullUserRequest(f"{contact.phone}"))
#             user_obj = full_user.user
#             try:
#                 await client(InviteToChannelRequest(telegram_channel, [user_obj]))
#             except Exception as e:
#                 print(2)
#                 print(e)
#             record.is_added_to_group=True
#             record.time_added_to_group = datetime.datetime.now()
#             record.save()


@login_required(login_url="/")
@user_passes_test(check_viewing_rights_admin)
def view(request):
    added_records = UserRecord.objects.filter(is_added_to_group=True)
    registered_records = UserRecord.objects.filter(
        ~Q(telegram_number='') & ~Q(telegram_number=None) & Q(is_added_to_group=False))
    print(registered_records)
    unregistered_records = UserRecord.objects.filter(Q(user=None) | Q(telegram_number=None) | Q(telegram_number=''))
    return render(request,'base_app/view.html',{'added_records':added_records,"registered_records":registered_records,"unregistered_records":unregistered_records})



