import sys
import telethon
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerChannel, InputPeerEmpty, InputPeerUser, InputPhoneContact, PeerUser
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import AddChatUserRequest
from telethon.tl.functions.contacts import ImportContactsRequest
import pandas as pd
import datetime
from tqdm import tqdm
from base_app.models import UserRecord
from django.db.models import Q


# -- CLIENT INITIALIZATION
api_id = 1238868
api_hash = "299435e6d3e9689589180dd71beb06e8"
phone = "+919488006888"
telegram_channel_name = "https://t.me/joinchat/AAAAAFQEmxBonLdyQvsvGQ"


client = TelegramClient(phone, api_id=api_id, api_hash=api_hash)
# -- CLIENT INITIATED --


# -- unUSED FUNCTION FOR NOW. --
async def get_telegram_channel(telegram_channel_name):
    dialogs = await client.get_dialogs()

    for dialog in dialogs:
        try:
            title = dialog.entity.title
            if(title == telegram_channel_name):
                return dialog.entity.id
        except:
            continue


# -- UNUSED FUNCTION FOR NOW.  FOR SENDING MESSAGE TO A USER  ---


async def send_message(username=None, message="", myself=False):
    print("sending message")
    print(message)
    if(username is not None):
        await client.send_message(username, message)
    elif(myself == True):
        me = await client.get_me()
        me.stringify()
        print(me.username)
        await client.send_message(me, message)
    else:
        print("no message given")

# --- IMPORTING CSV FILE AND GIVING DATA ---


def csv_import(file_name):
    df = pd.read_csv(file_name)
    number_list = list(df["phone_number"])
    number_list = list(map(lambda num: "+"+str(num), number_list))
    return number_list

# ---- MAIN CODE IS HERE . CLIENT CONNECTS AND ADDS USERS ----


async def main():

    await client.connect()
    flag = await client.is_user_authorized()
    print(flag, "<-- Is aiuthorized", end="\n")
    if not flag:
        client.send_code_request(phone)
        client.sign_in(phone, input('Enter the code: '))

    print("connected", end="\n")


    telegram_test_channel = await client.get_entity(telegram_channel_name)

    print(telegram_test_channel, " <-- Channel obtained", end="\n")

    user_list = list(UserRecord.objects.filter( ~Q(telegram_number='') & ~Q(telegram_number=None) & Q(is_added_to_group=False)))

    for user_record in tqdm(user_list):
        num = user_record.telegram_number
        try:

            contact = InputPhoneContact(client_id=0, phone=num,
                                        first_name=f"{user_record.rollno}", last_name=f"{user_record.name}")

            result = await client(ImportContactsRequest([contact]))

            user_full = await client(GetFullUserRequest(num))

            print(user_full.user, "<-- Obtained User", end="\n")

            await client(InviteToChannelRequest(
                telegram_test_channel,
                [user_full.user]
            ))
            user_record.is_added_to_group = True
            user_record.time_added_to_group = datetime.datetime.now()
            user_record.save()
        except telethon.errors.rpcerrorlist.UserAlreadyParticipantError as e:
            print(e, "<-- Error. User Already participant", end="\n")
        except Exception as e:
            print(e, "<-- Error Occurred", end="\n")

# --- MAIN FUNCITON CALLED HERE DUE TO ASYNCHRONOUS NATURE ---
with client:
    client.loop.run_until_complete(main())

