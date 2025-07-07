from django.db.models.signals import m2m_changed
from django.dispatch import receiver
from .models import Opportunity, TagSubscription
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

@receiver(m2m_changed, sender=Opportunity.tags.through)
def notify_subscribers_on_tag_added(instance, action, **kwargs):
    if action != "post_add":
        return  # Only trigger when tags are added

    opportunity_tags = instance.tags.all()
    subscriptions = TagSubscription.objects.filter(tags__in=opportunity_tags).distinct()

    for subscription in subscriptions:
        context = {
            'opportunity': instance,
            'recipient': subscription.email,
            'tags': subscription.tags.all(),
            'domain': settings.SITE_DOMAIN,
        }

        subject = f"New Opportunity: {instance.title}"
        from_email = None  # uses DEFAULT_FROM_EMAIL
        to = [subscription.email]

        text_body = render_to_string('emails/opportunity_notification.txt', context)
        html_body = render_to_string('emails/opportunity_notification.html', context)

        email = EmailMultiAlternatives(subject, text_body, from_email, to)
        email.attach_alternative(html_body, "text/html")
        email.send()
