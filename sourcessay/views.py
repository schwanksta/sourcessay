from django.db.models import Count
from django.shortcuts import render, get_object_or_404
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


def author(request, outlet, slug):
    byline = get_object_or_404(Author, news_outlet=outlet, slug=slug)
    articles = byline.item_set.all()

    top_authors = Author.objects.all().annotate(Count('item')).order_by('-item__count')[:5]
    top_outlets = Outlet.objects.all().annotate(Count('item')).order_by('-item__count')[:5]

    context = dict(
        author - byline,
        object_list = articles,
        top_authors = top_authors,
        top_outlets = top_outlets
    )
    return render(request, "author.html", context)

