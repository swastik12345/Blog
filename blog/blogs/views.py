from urllib import quote_plus

from django.http import Http404
from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from .forms import PostForm
from models import Post



def post_create(request):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    form=PostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request,"Successfully Created")
        return HttpResponseRedirect(instance.get_absolute_url())
    context={
        'form': form,
    }
    return render(request, "post_form.html", context)

def post_detail(request , slug):

    instance = get_object_or_404(Post, slug=slug)
    share_string=quote_plus(instance.content)
    context = {
        "title": "detail",
        "instance": instance,
        "share_string" : share_string
    }
    return render(request, "post_detail.html", context)

def post_list(request):

    quearyset_list= Post.objects.all().order_by("-timestamp")
      # Show 25 contacts per page
    query= request.GET.get("q")
    if query:
        quearyset_list=quearyset_list.filter(title__icontains=query)
    paginator = Paginator(quearyset_list, 10)
    page = request.GET.get('page')
    try:
        quearyset  = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        quearyset = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        quearyset = paginator.page(paginator.num_pages)

    context = {
         "object_list": quearyset,
         "title": "list"
      }
    return render(request,"index.html", context)



def post_update(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    form = PostForm(request.POST or None, request.FILES or None, instance=instance)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()
        messages.success(request, "Successfully Saved")
        return HttpResponseRedirect(instance.get_absolute_url())

    context = {
        "title": "detail",
        "instance": instance,
        "form": form
    }
    return render(request, "post_form.html", context)


def post_delete(request, slug=None):
    if not request.user.is_staff or not request.user.is_superuser:
        raise Http404
    instance = get_object_or_404(Post, slug=slug)
    instance.delete()
    messages.success(request, "Successfully Saved")
    #return render(request,"index.html", {})
    return redirect("list")





# if request.user.is_authenticated():
    #    context = {
     #       "title": "My user list"
     #   }
    #else:
     #   context = {
      #      "title": "list"
       # }