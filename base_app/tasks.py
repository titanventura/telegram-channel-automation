from telethon import TelegramClient
from telethon.tl.types import InputPhoneContact
from telethon.tl.functions.contacts import ImportContactsRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
from django.contrib import messages
import datetime
import os
from telethon.errors import SessionPasswordNeededError,PhoneCodeEmptyError,PhoneCodeExpiredError,PhoneCodeInvalidError,FloodWaitError,PhoneNumberFloodError,PhoneNumberUnoccupiedError,PhoneNumberInvalidError,AuthKeyUnregisteredError,PasswordEmptyError,PasswordHashInvalidError
from django.conf import settings
api_id =settings.API_ID
api_hash = settings.API_HASH
channel_hash = settings.CHANNEL_HASH

async def verify_code(req,phone,pin,hash,password):
    client = TelegramClient(phone, api_id=api_id, api_hash=api_hash)
    await client.connect()
    flag = await client.is_user_authorized()
    if not flag:
        try:
            await client.sign_in(phone, pin, phone_code_hash=hash)
        except SessionPasswordNeededError:
            await client.sign_in(password=password)

        except ValueError as e:

            messages.error(req, 'You have 2FA enabled. Enter the password below the OTP while validating.')
            err = 'You must provide a phone and a code the first time, and a password only if an RPCError was raised before. |' + str(
                datetime.datetime.now())

            try:
                await client.disconnect()
            except Exception as e:
               pass

            try:
                print(os.listdir())
                os.remove(os.getcwd() + '/' + f"{phone}.session")
                print(os.listdir())
            except Exception as e:
                pass
            return (err,'verify')



        except PhoneNumberFloodError:
            err = 'Phone number floodwait error |' + str(datetime.datetime.now())
            messages.error(req, 'You have reached maximum number of attempts.Try after 24Hours.')
            try:
                await client.disconnect()
            except Exception as e:
               pass

            try:
                print(os.listdir())
                os.remove(os.getcwd() + '/' + f"{phone}.session")
                print(os.listdir())
            except Exception as e:
                pass
            return (err,'logout')


        except FloodWaitError:
            err = 'Phone number floodwait error |' + str(datetime.datetime.now())
            messages.error(req,'You have reached maximum number of attempts.Try after 24Hours.')
            try:
                await client.disconnect()
            except Exception as e:
                pass

            try:
                print(os.listdir())
                os.remove(os.getcwd() + '/' + f"{phone}.session")
                print(os.listdir())
            except Exception as e:
                pass

            return (err, 'logout')

        except PhoneNumberUnoccupiedError:
            messages.error(req, 'Please provide a number associated with telegram.')
            err = 'Phone Number Unoccupied |'+str(datetime.datetime.now())
            try:
                await client.disconnect()
            except Exception as e:
                pass

            try:
                print(os.listdir())
                os.remove(os.getcwd() + '/' + f"{phone}.session")
                print(os.listdir())
            except Exception as e:
                pass

            return (err,'register')


        except PhoneCodeInvalidError:

            messages.error(req,'Please enter a valid OTP')
            err = 'Invalid Phone Code error |'+str(datetime.datetime.now())
            try:
                await client.disconnect()
            except Exception as e:
                pass

            try:
                print(os.listdir())
                os.remove(os.getcwd() + '/' + f"{phone}.session")
                print(os.listdir())
            except Exception as e:
                pass
            return (err, 'verify')


        except PhoneCodeEmptyError:

            messages.error(req,'Please enter a valid OTP')
            err = 'Empty Phone Code error |'+str(datetime.datetime.now())
            try:
                await client.disconnect()
            except Exception as e:
                pass

            try:
                print(os.listdir())
                os.remove(os.getcwd() + '/' + f"{phone}.session")
                print(os.listdir())
            except Exception as e:
                pass
            return (err, 'verify')


        except PhoneCodeExpiredError:

            messages.error(req,'Your OTP  has expired.')
            err = 'Expired OTP error |'+str(datetime.datetime.now())
            try:
                await client.disconnect()
            except Exception as e:
                pass

            try:
                print(os.listdir())
                os.remove(os.getcwd() + '/' + f"{phone}.session")
                print(os.listdir())
            except Exception as e:
                pass
            return (err ,'register')


        except PasswordHashInvalidError:

            messages.error(req, 'You have enetered an invalid 2FA password.')
            err = 'Password Hash Invalid error |' + str(datetime.datetime.now())
            try:
                await client.disconnect()
            except Exception as e:
                pass

            try:
                print(os.listdir())
                os.remove(os.getcwd() + '/' + f"{phone}.session")
                print(os.listdir())
            except Exception as e:
                pass
            return (err, 'verify')


        except PasswordEmptyError:

            messages.error(req, 'Please enter your 2FA password.')
            err = 'Expired OTP error |' + str(datetime.datetime.now())
            try:
                await client.disconnect()
            except Exception as e:
                pass

            try:
                print(os.listdir())
                os.remove(os.getcwd() + '/' + f"{phone}.session")
                print(os.listdir())
            except Exception as e:
                pass

            return (err, 'verify')


    # Joining the channel
    try:
        updates = await client(ImportChatInviteRequest(channel_hash))
        if updates:
            val = True
    except AuthKeyUnregisteredError:
        return 'retry'
    except Exception as e:
        print(e)
        err = str(e) + '|' + str(datetime.datetime.now())
        pass
        return err,'retry'


    # Disconnecting client
    try:
        await client.disconnect()
    except Exception as e:
        pass

    # Removing corresponding session file
    try:
        print(os.listdir())
        os.remove(os.getcwd() + '/' + f"{phone}.session")
        print(os.listdir())
    except Exception as e:
        pass

    return '',val


async def send_code(req,phone):
    client = TelegramClient(phone, api_id=api_id, api_hash=api_hash)
    await client.connect()
    auth_client = await client.is_user_authorized()
    print(auth_client)
    if not auth_client:
        try:
            sent = await client.send_code_request(phone)
            return '',sent.phone_code_hash
        except PhoneNumberFloodError:
            messages.error(req,'You have reached maximum number of attempts.Try after 24Hours.')
            err = 'Floodwait error(PhoneNumberFloodError) |'+str(datetime.datetime.now())
            try:
                await client.disconnect()
            except Exception as e:
                pass

            try:
                print(os.listdir())
                os.remove(os.getcwd() + '/' + f"{phone}.session")
                print(os.listdir())
            except Exception as e:
                pass
            return err,'logout'
        except FloodWaitError:
            messages.error(req, 'You have reached maximum number of attempts.Try after 24Hours.')
            err = 'Floodwait error |'+str(datetime.datetime.now())
            try:
                await client.disconnect()
            except Exception as e:
                pass

            try:
                print(os.listdir())
                os.remove(os.getcwd() + '/' + f"{phone}.session")
                print(os.listdir())
            except Exception as e:
                pass
            return err,'logout'

        except PhoneNumberUnoccupiedError:
            messages.error(req,'Please provide a number associated with telegram.')
            err = 'Phone number Unoccupied error |'+str(datetime.datetime.now())
            try:
                await client.disconnect()
            except Exception as e:
                pass

            try:
                print(os.listdir())
                os.remove(os.getcwd() + '/' + f"{phone}.session")
                print(os.listdir())
            except Exception as e:
                pass
            return err,'register'

        except PhoneNumberInvalidError:
            messages.error(req,'Please enter a valid Phone number')
            err = 'Invalid Phone Number error |'+str(datetime.datetime.now())
            try:
                await client.disconnect()
            except Exception as e:
                pass

            try:
                print(os.listdir())
                os.remove(os.getcwd() + '/' + f"{phone}.session")
                print(os.listdir())
            except Exception as e:
                pass
            return err,'register'

        except PhoneCodeEmptyError:
            messages.error(req,'Please enter a valid OTP')
            err = 'Invalid Phone Code error |' + str(datetime.datetime.now())
            try:
                await client.disconnect()
            except Exception as e:
                pass

            try:
                print(os.listdir())
                os.remove(os.getcwd() + '/' + f"{phone}.session")
                print(os.listdir())
            except Exception as e:
                pass
            return err,'register'

        except PhoneCodeExpiredError:
            messages.error(req,'Your OTP  has expired.')
            err = 'OTP expired error |' + str(datetime.datetime.now())
            try:
                await client.disconnect()
            except Exception as e:
                pass

            try:
                print(os.listdir())
                os.remove(os.getcwd() + '/' + f"{phone}.session")
                print(os.listdir())
            except Exception as e:
                pass
            return err,'register'

        except Exception as e:
            messages.error(req, 'An unknown error has occurred.')
            err = str(e) + '|' + str(datetime.datetime.now())
            try:
                await client.disconnect()
            except Exception as e:
                pass

            try:
                print(os.listdir())
                os.remove(os.getcwd() + '/' + f"+{phone}.session")
                print(os.listdir())
            except Exception as e:
                pass
            return err, 'unknown'