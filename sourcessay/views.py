from django.db.models import Count
from django.shortcuts import render
from sourcessay.models import Item, Author, Outlet

def index(request):
    articles = Item.objects.all()[:200]
    top_authors = Author.objects.all().annotate(Count('item')).order_by('-item__count')[:5]
    top_outlets = Outlet.objects.all().annotate(Count('item')).order_by('-item__count')[:5]
    context = dict(
        object_list = articles,
        top_authors = top_authors,
        top_outlets = top_outlets
    )
    return render(request, "index.html", context)
