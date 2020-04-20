# WorkFlow
<font size="3">
Here is a workflow depicting how the application works exactly.
</font>

1. The DB of the application contains a table called UserRecord.
2. It has a ForeignKey to the main user table.
    * User (ForeignKey)
    * mobile_number
    * telegram_number
    * email
    * is_added
    * time_added_to_channel
    * errors
3. The fields mobile_number, telegram_number, email are populated when the CSV related to the users are imported.
4. The Users will be able to register themselves into the application through normal authentication or through google OAuth and after that they can register themselves to the telegram channel with 2FA. 
5. Once the user registers in the application and tries to join the channel with his registered user account, the User (ForeignKey) field gets populated then.
6. In this way all the data related to the users is present in the database and the admin (which is you) will be able to view the people added to the channel and people whose registration has gone wrong (errors).