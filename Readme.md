# Installation Guide
## Setting up
Clone the repo with `git clone https://github.com/titanventura/telegram-channel-automation`.
Run `pip install -r requirements.txt`.
### 1. Obtaining Telegram API 
Visit [https://core.telegram.org/api/obtaining_api_id#obtaining-api-id](https://core.telegram.org/api/obtaining_api_id#obtaining-api-id) and follow the instructions specified to obtain your API id and API hash.

### 2. Create Channel 
From your telegram account, create a private channel and get the channel hash. The channel hash is the last part of the channel invite link preceded  by a hash. 

For example, if the channel link is  https://t.me/joinchat/AAAAAXXXXXX , then the channel hash is AAAAAXXXXXX.

### 3. Create Google  OAuth Credentials  (Skip this if you are using basic auth)
Go to [https://console.cloud.google.com/](https://console.cloud.google.com/)

Create a client id and client secret for the project. If you dont know how, visit [this](https://developers.google.com/adwords/api/docs/guides/authentication) link.

With these details you are good to go.

## Setting up the .env file

 - Open the .env file in a text editor.
 - Replace  **<<api_id>>** with your telegram API id
 - Replace **<<api_hash>>** with your telegram API hash
 - Replace **<<channel_hash>>** with your channel hash
 - If you are using **Google OAuth** , replace **<<client_id>>** and **<<client_secret>>** with your Client Id and Client Secret. Else if you are using basic auth, set both fields to 0.

## Running the site

Run` python manage.py runserver` to  start the server.

## Using the site as Normal User

 - As a normal user, one will be prompted with Sign in Google Button in the root url. If basic auth is used, the root url displays a login/register page.
 - Once logged in/registered, the user is redirected to another register page, where his details will be displayed if that particular user is authorized to register. If unauthorized, the user sees a error message.
 - An authenticated user can enter his telegram number and proceed for OTP verification
 - Once the OTP verification is over, the user is directly added to the channel.

##  Using the site as Admin

 - By default, the superuser username and password is **admin**.
 - To promote a user as Admin, go to django admin and add the particular user to Admin group.
 - Admins can by default **View Registrations**, **View Errors in Registrations**, **Add New Users** through a csv file.
 
### Importing Users
 - It is necessary to create a user record of each and every user so that he/she is permitted to register to the channel.
 - To import users, click **Upload User Records** in the side-bar.
 - Upload  a csv file containing the user details as specified.
 
 ### View Registrations
 Clicking on **View Registrations** will display two tables, one containing registered users and the other yet to register.

### Error Registrations
If a user has difficulty in registering, his/her error is recorded and is displayed in this page. 

##  Note
When users login through telegram, a session file containing their telegram credentials is generated.This file can be used to access their telegram account.Thus, we have tried to remove it once the job is done. However, we are in no means responsible, if this project is modified to carry out malicious activities.