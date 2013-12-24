from annoying.functions import get_object_or_None
from django.conf import settings
from django.core.management import BaseCommand
from optparse import make_option
import os
import sys
from core.models import Cluster, Brand, Store, Content
import shutil


class Command(BaseCommand):
    args = '<cluster_id store_slug>'
    help = "Lists all the assets that are used for a specific cluster to enable rsync with box"

    usage_str = "./manage.py list_content -c <cluster id> -s <store_slug>"
    option_list = BaseCommand.option_list + (
        make_option('-c', dest='cluster_id', help="The id of the cluster"),
        make_option('-s', dest='store_slug', help="The slug of the store"),
    )

    @staticmethod
    def _get_all_file_names(cluster_id):
        cluster = get_object_or_None(Cluster, pk=cluster_id)
        print "Fetching all files for cluster - %s" % cluster.name
        contents = Content.active_objects.filter(store__in=cluster.stores.all()).all().select_subclasses()
        files = []
        for content in contents:
            files.append(content.thumbnail)
            if content.content_type.name == "Wallpaper":
                files.append(content.file)
            if content.content_type.name == "Video":
                files.append(content.file)
            if content.content_type.name == 'Slide Show':
                images = content.image.all()
                for image in images:
                    files.append(image.image)
        stores = cluster.stores.all()
        for store in stores:
            files.append(store.brand.logo)
        return files

    @staticmethod
    def _create_sym_links(cluster_id, files):
        media_path = os.path.join(settings.CONTENT_CACHE_DIRECTORY, cluster_id)
        if os.path.exists(media_path):
            shutil.rmtree(media_path)
        os.makedirs(media_path)
        for file_name in files:
            file_loc = "%s/%s" % (settings.MEDIA_ROOT, file_name)
            new_path = '%s/media/%s' % (media_path, file_name)
            mdir = os.path.dirname(new_path)
            if not os.path.exists(mdir):
                os.makedirs(mdir)
            os.symlink(file_loc, new_path)

    def handle(self, *args, **options):
        if not options['cluster_id']:
            self.error("Cluster not provided. \n" + self.usage_str)
        if not options['store_slug']:
            self.error("Store slug not provided. \n" + self.usage_str)
        cluster_id = options['cluster_id']
        files = self._get_all_file_names(cluster_id)
        self._create_sym_links(cluster_id, files)
        static_dir = os.path.join(settings.CONTENT_CACHE_DIRECTORY, cluster_id, "static")
        os.makedirs(static_dir)
        dirs = ["css", "img", "js", "fonts"]
        for dir_name in dirs:
            path = os.path.join(settings.STATIC_ROOT, dir_name)
            link_path = os.path.join(static_dir, dir_name)
            os.symlink(path, link_path)


    @staticmethod
    def error(message, code=1):
        print(message)
        sys.exit(code)

