import datetime
from django.core.management import BaseCommand
import sys
from core.models import Content
from django.conf import settings
import requests
content_type_mapping = {
    1: 'Store Home',
    2: 'Cluster Home',
    3: 'Cluster Info',
    4: 'Store Info',
}


class Command(BaseCommand):
    def check_expiring(self):
        after_2_days = datetime.datetime.now() + datetime.timedelta(days=2)
        today = datetime.datetime.now()
        count = 0
        all_contents = Content.objects.filter(end_date__lte=after_2_days, active=True, archived=False)\
            .filter(end_date__gte=today)
        content_table = '<table border><thead><tr>' \
                        '<th>Content ID</th>' \
                        '<th>Content Name</th>' \
                        '<th>Content Type</th>' \
                        '<th>Content Location</th>' \
                        '<th>End Date</th>' \
                        '<th>Assigned Stores</th>' \
                        '<th>Assigned Brand</th>' \
                        '</tr></thead><tbody>'
        for c in all_contents:
            count = 1
            print "Content is %s" % c.name
            print "Content Location %s" % c.content_location
            assigned_brand = None
            store_name_list = ''
            if c.store is not None:
                stores = c.store.all()
                for st in stores:
                    store_name_list += "%s, " % st.name
                if int(c.content_location) is not 3:
                    try:
                        assigned_brand = stores[0].brand.name
                    except IndexError:
                        pass
            row = '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % \
                  (c.id, c.name, c.content_type, content_type_mapping[int(c.content_location)], c.end_date,
                   store_name_list, assigned_brand)
            content_table += row

        content_table += '</tbody></table>'
        self.send_complex_message(content_table, count)

    def send_complex_message(self, content_table, count):
        if count == 1:
            print "Emailing expiring Contents to"
            print settings.MAILING_LIST
            r = requests.post(settings.MAILGUN_HOST,
                                 auth=("api", settings.MAILGUN_API_KEY),
                                 data={"from": "Brandclub <brandclub@brandclub.mobi>",
                                       "to": settings.MAILING_LIST,
                                       "subject": "Expiring Contents",
                                       "text": "Expiring content(s)",
                                       "html": content_table})
            print "Response is"
            print r.text
            print "Status %s" % r.status_code
        else:
            print "No contents matching the criteria"


    def handle(self, *args, **options):
        self.check_expiring()

    @staticmethod
    def error(message, code=1):
        print message
        sys.exit(code)

