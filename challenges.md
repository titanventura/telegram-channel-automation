<h1>Challenges</h1>
<font size="3">
So , These are some of the challenges that we ( the developers ) faced while building this project.
</font>

## AsyncIO
<font size="3">
Dealing with asyncio can be quite problematic especially if you have no prior experience.
Using High Level APIs directly instead of fiddling with the low level ones as presented in most tutorials will be a wise choice while developing applications of this kind.
The Reason is that the abstraction provided by telethon is capable enough to handle event loops and asynchronous oprations.
</font>


## Corner Case Scenarios ( Exceptions )
<font size="3">
Dealing with RPC errors of the telethon API and covering corner cases can be a bit of a hassle.
Here is a <a href="https://docs.telethon.dev/en/latest/concepts/errors.html">link</a> to the documentation of Telethon where you can find all the known RPC errors while dealing with methods.
Exceptions that arise while registering of users will be registered in the DB as a field of the UserRecord table. Although you may use an external entity like sentry to log errors that you might face.
</font>