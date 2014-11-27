from automated_emails.models import AutomatedEmail
from django.template import Context, Template
from django.core.mail import send_mail

def send_email(recipient, subject, template, context=None):
    from_email = "info@pleasuresallmine.co.uk"
    context = Context(context)
    text = template.render(context)

    send_mail(
            subject=subject,
            message=text,
            from_email=from_email,
            recipient_list=[recipient],
    )


def send_welcome_email(user):
    template = Template(AutomatedEmail.objects.get(title="Account Welcome").content)
    recipient = user.email
    send_email(
            recipient,
            "Pleasures All Mine Registration",
            template
            )

def send_order_confirmation_email(order):
    send_email(
        recipient = order.user.email,
        subject = "Pleasures All Mine Order Confirmation",
        template = Template(AutomatedEmail.objects.get(title="Order Confirmation").content),
        context = {
                'order': order,
        }
    )



def send_admin_welcome_email(user, password):
    template = Template(AutomatedEmail.objects.get(title="Admin Create Account").content)
    recipient = user.email
    send_email(
            recipient,
            "Pleasures All Mine Registration",
            template,
            context = {
                    'password': password,
            }
    )
