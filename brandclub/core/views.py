from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template.loader import get_template
from django.template import Context
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .forms import FeedbackForm

from .models import Brand, Cluster, Store, Content, SlideShow, StoreFeedback


def slug_view(request, slug):
    cluster_id = request.cluster_id
    home_cluster = get_object_or_404(Cluster, id=cluster_id)
    all_contents = home_cluster.get_all_home_content()
    home_brand = get_object_or_404(Brand, slug_name=slug)
    return render_to_response('home.html', {'contents': all_contents, 'cluster': home_cluster, 'brand': home_brand})


def store_home(request, slug):
    store = get_object_or_404(Store, slug_name=slug)
    contents = Content.active_objects.filter(show_on_home=False, store=store).select_subclasses()
    return render_to_response('store_home.html', {'contents': contents, 'brand': store.brand, 'store': store})


@csrf_exempt
def submit_feedback(request):
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        # form.clean()
        name = request.POST["name"]
        phone_number = request.POST["phone_number"]
        email_id = request.POST["email_id"]
        message = request.POST["message"]
        store = request.POST["store"]
        store_obj = get_object_or_404(Store, pk=store)
        sfb = StoreFeedback(name=name, phone_number=phone_number,
                            email_id=email_id, message=message, store=store_obj)
        # sfb.save()
        url = '/home/%s' % store_obj.slug_name
        return HttpResponseRedirect(url)
    return render_to_response("success.html")


@csrf_exempt
def store_feedback(request, slug):
    store = get_object_or_404(Store, slug_name=slug)
    if request.method == 'POST':
        print request.POST
        form = FeedbackForm(request.POST)
        return HttpResponseRedirect('.')
    else:
        form = FeedbackForm()
        c = {}
        c.update(csrf(request))
    print form
    return render_to_response("store_feedback.html",
                              {'form': form,
                               'brand': store.brand,
                               'store': store
                              })