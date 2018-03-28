hello = """
Hello. I am an Instapaper bot that'll help you save articles to your Instapaper account directly from Telegram.

In the current version (v0.2) I can authorize you and save your urls to your Instapaper account.

Availible commands:
    /start — shows this hello message
    /auth  — authorizes you
    /add   — adds url to an Instapaper account
"""

auth = """
First, you need to authorize your Instapaper account.

Just use the /auth command to do this.
"""

auth_warning = """
*Attention!*

You are already authorized. If you add a new account, the last one will be rewrited.
"""

auth_requirement = """
You can't add urls to your Instapaper account without authorization.

To authorize use /auth command.
"""