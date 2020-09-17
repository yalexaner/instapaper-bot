# coding=utf-8

what_next = """
What do you want to do next?
"""

authorized_hello = """
We've already met :)

What do you want to do next?
"""

unauthorized_hello = """
Hi, I am going to help you save the articles that you will send me to your Instapaper account.

There are several useful commands that I'm going to tell you about a little bit later, but first, I need to get you authorized, so I can do my job :)
"""

username_request = """
Send me your *username* or *email address*:
"""

password_request = """
And now send me your *password*, if you **have** one:
"""

authorized = """
You are authorized. So shall we start now?
"""

finish_authorization = """
And, as I promised, here are all the available commands you can use. If you want to know what all of them do, use the "See help message" button. So, what do we do next?
"""

help = """
I can work in two modes: *add urls once* and *adding mode*.

First mode is for one-use cases: when you want me to add some urls that you will send me in one message to Instapaper and then get you back to the main menu.

Second one is just like the first: you send me urls, I save them, but then I wait for more of them, unlike in first mode — get you to the main menu. To get off the mode you just press the "Stop Adding mode" button.

That's it, for now that's all I can do. Now let me tell you what buttons to press to use those modes and what other buttons mean:
    — The very first button — "Add urls" — enables first mode.
    — The second one — "Authorize" button — goes through an authorization process once again. That's useful when you change the password or created a new account and you want to use this one.
    — The big button on the next row — "Go to Adding mode" — lets you use the mode that I just told you about.
    — The last button — "See help message" button — shows you this help message.

If you got used to using commands, not buttons, you can use those commands:
    /start			— shows hello message
    /auth 			— authorizes you (like "Authorize" button)
    /add			— adds urls to an instapaper account (like "Add urls" button, first mode)
    /adding_mode 	— adds urls without command (like "Go to Adding mode" button, second mode)
    /help           — shows this help message (like "See help message" button)
    /cancel 		— cancels any action and returns you to main menu
"""

auth_first = """
To start using me you need to authorize your Instapaper account.

Just use the /auth command to do this.
"""

auth_warning = """
*Attention!*

You are already authorized. To cancel use /cancel command.
"""

auth_requirement = """
You can't add urls to your Instapaper account without authorization.

To authorize use /auth command.
"""
