# coding=utf-8

authorized_hello = """
We've already met :)

What do wo want to do next?
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

help = """
Available commands:
    /start			— shows hello message
    /auth 			— authorizes you
    /add			— adds urls to an Instapaper account
    /adding_mode 	— adds urls without command
    /cancel 		— cancels any action
    /help           — lists all the commands
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
