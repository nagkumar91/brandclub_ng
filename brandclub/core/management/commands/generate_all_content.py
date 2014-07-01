from annoying.functions import get_object_or_None
from django.conf import settings
from django.core.management import BaseCommand
from optparse import make_option
import os
import sys
from core.models import Cluster, Brand, Store, Content
import shutil


class Command(BaseCommand):
    help = "Lists all the assets that are used for a specific cluster to enable rsync with box"

    @staticmethod
    def _get_all_file_names(cluster):
        # cluster = get_object_or_None(Cluster, pk=cluster_id)
        print "Fetching all files for cluster - %s" % cluster.name
        contents = Content.active_objects.filter(store__in=cluster.stores.all()).all().select_subclasses()
        files = []
        for content in contents:
            files.append(content.thumbnail)
            if content.content_type.name == "Wallpaper":
                files.append(content.file)
            if content.content_type.name == "Video":
                files.append(content.file)
            if content.content_type.name == "Offer":
                files.append(content.file)
            if content.content_type.name == 'Slide Show':
                if content.image.all() is None:
                    continue
                images = content.image.all()
                for image in images:
                    files.append(image.image)
        stores = cluster.stores.all()
        for store in stores:
            files.append(store.brand.logo)
            if store.map_name is not None:
                files.append(os.path.join(settings.STORE_MAPS_DIRECTORY, store.map_name))
        return files

    @staticmethod
    def _get_all_cluster_file_names(cluster, files):
        # cluster = get_object_or_None(Cluster, pk=cluster_id)
        print "Fetching all cluster files for cluster - %s" % cluster.name
        contents = cluster.content.all().select_subclasses()
        for content in contents:
            files.append(content.thumbnail)
            if content.content_type.name == "Wallpaper":
                files.append(content.file.name.replace("/media/",""))
            if content.content_type.name == "Video":
                files.append(content.file)
            if content.content_type.name == "Offer":
                files.append(content.file)
            if content.content_type.name == 'Slide Show':
                if content.image.all() is None:
                    continue
                images = content.image.all()
                for image in images:
                    files.append(image.image)
        return files

    @staticmethod
    def _create_sym_links(cluster_id, files):
        media_path = os.path.join(settings.CONTENT_CACHE_DIRECTORY, cluster_id)
        if os.path.exists(media_path):
            shutil.rmtree(media_path)
        os.makedirs(media_path)
        for file_name in files:
            file_loc = "%s/%s" % (settings.MEDIA_ROOT, file_name)
            # new_path = '%s/media/%s' % (media_path, file_name)
            new_path = '%s/%s' % (media_path, file_name)
            mdir = os.path.dirname(new_path)
            if not os.path.exists(mdir):
                os.makedirs(mdir)
            if not os.path.exists(new_path):
                print "%s - %s" % (file_loc, new_path)
                os.symlink(file_loc, new_path)

    def handle(self, *args, **options):
        clusters = Cluster.objects.all()
        for cluster in clusters:
            cluster_id = "%s" % cluster.id
            files = self._get_all_file_names(cluster)
            self._get_all_cluster_file_names(cluster, files)
            self._create_sym_links(cluster_id, files)
            static_dir = os.path.join(settings.CONTENT_CACHE_DIRECTORY, cluster_id, "static")
            if not os.path.exists(static_dir):
                os.makedirs(static_dir)
            dirs = ["css", "img", "js", "fonts", "updates"]
            for dir_name in dirs:
                path = os.path.join(settings.STATIC_ROOT, dir_name)
                link_path = os.path.join(static_dir, dir_name)
                if not os.path.exists(link_path):
                    os.symlink(path, link_path)


    @staticmethod
    def error(message, code=1):
        print(message)
        sys.exit(code)

