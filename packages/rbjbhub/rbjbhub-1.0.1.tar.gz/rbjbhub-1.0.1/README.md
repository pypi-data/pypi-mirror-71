# Review Board Jetbrains Hub

This is a plugin for [Review Board](https://reviewboard.org) that allows you to
use [Jet Brains Hub](https://jetbrains.com/hub) as an authentication source.

Since Review Board 3 does not yet support OAuth2 for authentication, this uses
the Resource Owner Password Credentials OAuth2 flow in Hub.  This means that
users will use their normal JetBrains Hub username and password to login.  This
also means that two factor authentication methods are not supported and users
with 2FA on will need to create an application password in their Hub settings.

# Prerequisites

To setup this plugin you will of course need both Review Board and JetBrains
Hub up and running.

## Review Board

You can find the official documentation for installing Review Board
[here](https://www.reviewboard.org/docs/manual/3.0/admin/).

## JetBrains Hub

You can find documentation for installing JetBrains Hub
[here](https://www.jetbrains.com/help/hub/installation-and-upgrade.html).

Once JetBrains Hub is up and running, you'll need to create a Service for
Review Board.  A service in JetBrains Hub's terms is another service that is
using JetBrains Hub for authentication.  You can find documentation on creating
JetBrains Hub services in the
[official documentation](https://www.jetbrains.com/help/hub/add-service.html).

# Installation

Installation should be done via:

```
pip install rbjbhub
```

Once the plugin is installed, just make sure to rescan for extension in Review
Board and you should be able to enable it.

![review board admin extensions page with the plugin enabled](images/admin_extension.png)

Once you have enabled the extension, head over to the Authentication settings
and configure the plugin to match your settings from JetBrains Hub.

![review board admin settings authentication page](images/admin_settings_authentication.png)

All of these settings should be the values of the service you created in
JetBrains Hub above, with the exception that value for `Scope` is the ID of the
Hub service in your JetBrains Hub instance, which in my experience has always
been `0-0-0-0-0`.

When you're all done, go ahead and save your settings.  Then try to login as a
user that exists in your JetBrains Hub instance.  If you're able to log in, you
are good to go!

# Caveats

User email addresses are **ONLY** set, if the email address has been verified
in JetBrains Hub.

User information is **ONLY** synchronized when a user logs in.  This means that
if a user has changed their email address in Hub and are added to a review
request before they log into Review Board, the user will not receive an email
for that review request.

If a user has 2FA turned on, they will have to use an application password to
login.

If a user changes their username in JetBrains Hub a new Review Board account
will be created for them on their next login.  To avoid this, they should have
a Review Board administrator change their username in Review Board.

If a user already existed before logging in with JetBrains Hub, they will still
be able to login via that password.  As a Review Board administrator you can
change this password to something that the user does not know.

