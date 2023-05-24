from django.http import HttpResponse
from django.shortcuts import render
from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from api.core.process import *


def index(request):
    return render(request, "./api/index.html")


@csrf_exempt
def process_linkedin(request):
    link = request.POST.get('link', None)
    if link is None:
        return render(request, "./api/index.html")
    else:
        context = download_from_linkedin(post_link=link)
        template = loader.get_template('./api/index.html')
        return HttpResponse(template.render(context, request))


@csrf_exempt
def process_instagram(request):
    link = request.POST.get('link', None)
    if link is None:
        return render(request, "./api/instagram.html")
    else:
        context = download_from_instagram(post_link=link)
        template = loader.get_template('./api/instagram.html')
        return HttpResponse(template.render(context, request))


@csrf_exempt
def process_twitter(request):
    link = request.POST.get('link', None)
    if link is None:
        return render(request, "./api/twitter.html")
    else:
        context = download_from_twitter(post_link=link)
        template = loader.get_template('./api/twitter.html')
        return HttpResponse(template.render(context, request))


@csrf_exempt
def process_tiktok(request):
    link = request.POST.get('link', None)
    if link is None:
        return render(request, "./api/tiktok.html")
    else:
        context = download_from_tiktok(post_link=link)
        template = loader.get_template('./api/tiktok.html')
        return HttpResponse(template.render(context, request))


@csrf_exempt
def process_youtube(request):
    link = request.POST.get('link', None)
    if link is None:
        return render(request, "./api/youtube.html")
    else:
        context = download_from_youtube(post_link=link)
        template = loader.get_template('./api/youtube.html')
        return HttpResponse(template.render(context, request))


