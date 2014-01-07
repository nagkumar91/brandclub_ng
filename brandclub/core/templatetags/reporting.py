from django import template
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

register = template.Library()


@register.inclusion_tag('piwik/tracking_code.html', takes_context=True)
def tracking_code(context):
    try:
        piwik_id = settings.PIWIK_SITE_ID
    except AttributeError:
        raise ImproperlyConfigured('PIWIK_SITE_ID does not exist')

    try:
        url = settings.PIWIK_URL
    except AttributeError:
        raise ImproperlyConfigured('PIWIK_URL does not exist')

    try:
        cookie_domain = settings.PIWIK_COOKIE_DOMAIN
    except AttributeError:
        raise ImproperlyConfigured("PIWIK_COOKIE_DOMAIN does not exist in settings")

    store = context['home_store']
    cluster = context['home_cluster']
    device = context['home_device']
    brand = context['home_brand']
    return {'id': piwik_id, 'url': url, 'cookie_domain': cookie_domain,
            'home_store': store, 'home_cluster': cluster, 'home_device': device,
            'home_brand': brand}
