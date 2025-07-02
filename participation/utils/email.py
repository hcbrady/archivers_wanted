from django.core.mail import send_mail
from django.conf import settings
from participation.models import TagSubscription

def notify_subscribers(opportunity):
    for tag in opportunity.tags.all():
        subscriptions = TagSubscription.objects.filter(tag=tag.name)

        for sub in subscriptions:
            send_mail(
                subject=f"New Opportunity Tagged: {tag.name}",
                message=(
                    f"A new opportunity has been posted that matches your interest in '{tag.name}':\n\n"
                    f"{opportunity.title}\n\n"
                    f"{opportunity.summary}\n\n"
                    f"Visit the site to learn more."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[sub.email],
                fail_silently=False,
            )
