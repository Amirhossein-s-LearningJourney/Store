from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from django.shortcuts import render
from templated_mail.mail import BaseEmailMessage


def say_hello(request):
    try:
        # sending regular mail
        # send_mail("subject", "message", "info@store.com", ["jack@store.com"])
        # sending mail to admin
        # mail_admins("subj", "message", html_message="message233")
        # attaching files
        # mess = EmailMessage("sub", "message", "from@store.com", ["john@store.com"])
        # mess.attach_file("playground/static/images/dog.jpg")
        # mess.send()
        message = BaseEmailMessage(
            template_name="emails/hello.html", context={"name": "Amir"}
        )
        message.send(["john@store.com"])
    except BadHeaderError:
        pass
    return render(request, "hello.html", {"name": "Mosh"})
