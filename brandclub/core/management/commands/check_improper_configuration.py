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
        count = 0
        all_contents = Content.active_objects.all()
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
            print c.content_location
            if c.content_location != '3':
                stores = []
                stores.append(c.store)
                # print "len of stores %s" % len(stores)
                if len(stores) is 0:
                    # print "store is none"
                    count = 1
                    error_type = "Content Not assigned to any store"
                    row = '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>' % \
                          (c.id, c.name, c.content_type, content_type_mapping[int(c.content_location)], c.end_date, error_type)
                    content_table += row
                else:
                    stores = c.store.all()
                    # print stores
            else:
                print "Cluster info content %s" % c.name

        content_table += '</tbody></table>'
        self.send_complex_message(content_table, count)

    def send_complex_message(self, content_table, count):
        if count == 1 and None:
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


