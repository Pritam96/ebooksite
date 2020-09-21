from django.shortcuts import render, redirect, get_object_or_404
from ebook.models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ebook.forms import CreateEbookPostForm, UpdateEbookPostForm
from django.db.models import Q
from operator import attrgetter
from account_manager.models import Account
from django.http import HttpResponseRedirect
# from django.urls import reverse


# Create your views here.

EBOOK_POSTS_PER_PAGE = 4


def ebook_posts(request, *args, **kwargs):
    context = {}

    # Q lookup (search query)
    query = ""
    if request.GET:
        query = request.GET.get("q", "")
        context["query"] = str(query)

    ebook_posts = sorted(
        get_ebook_queryset(query), key=attrgetter("date_updated"), reverse=True
    )

    # Pagination
    page = int(request.GET.get("page", "1"))
    ebook_posts_paginator = Paginator(ebook_posts, EBOOK_POSTS_PER_PAGE)

    try:
        ebook_posts = ebook_posts_paginator.page(page)
    except PageNotAnInteger:
        ebook_posts = ebook_posts_paginator.page(EBOOK_POSTS_PER_PAGE)
    except EmptyPage:
        ebook_posts = ebook_posts_paginator.page(ebook_posts_paginator.num_pages)
    context["ebook_posts"] = ebook_posts
    return render(request, "ebook/ebooks.html", context)


def get_ebook_queryset(query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = EbookPost.objects.filter(
            Q(title__icontains=q) | Q(description__icontains=q) | Q(author__icontains=q)
        ).distinct()
        for post in posts:
            queryset.append(post)
    return list(set(queryset))


def create_ebook(request):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect("login")

    form = CreateEbookPostForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        obj = form.save(commit=False)
        posted_by = Account.objects.filter(email=user.email).first()
        obj.posted_by = posted_by
        obj.save()
        form = CreateEbookPostForm()
    context["form"] = form
    return render(request, "ebook/create.html", context)


def detail_ebook(request, slug):
    context = {}
    ebook_post = get_object_or_404(EbookPost, slug=slug)
    context["ebook_post"] = ebook_post
    return render(request, "ebook/detail_ebook.html", context)


def edit_ebook(request, slug):
    context = {}
    user = request.user
    if not user.is_authenticated:
        return redirect("login")
    ebook_post = get_object_or_404(EbookPost, slug=slug)
    if request.POST:
        form = UpdateEbookPostForm(
            request.POST or None, request.FILES or None, instance=ebook_post
        )
        if form.is_valid():
            obj = form.save(commit=False)
            obj.save()
            context["success_message"] = "Updated"
            ebook_post = obj
    form = UpdateEbookPostForm(
        initial={
            "title": ebook_post.title,
            "description": ebook_post.description,
            "author": ebook_post.author,
            "image": ebook_post.image,
            "pdf": ebook_post.pdf,
        }
    )
    context["form"] = form
    return render(request, "ebook/edit_ebook.html", context)


def like(request, slug):
    context = {}
    post = get_object_or_404(EbookPost, slug=slug)
    if request.user in post.likes.all():
        post.likes.remove(request.user.id)  # If user exists, Then User can remove
    else:
        post.likes.add(request.user.id)  # If user not exists, Then User can add
    context["ebook_post"] = post
    # return render(request, "ebook/detail_ebook.html", context)
    # return HttpResponseRedirect(reverse('detail_ebook'), context)
    return HttpResponseRedirect(request.META.get("HTTP_REFERER"))
    # return HttpResponseRedirect('detail', context)


def favourites(request, *args, **kwargs):
    context = {}

    # Q lookup (search query)
    query = ""
    if request.GET:
        query = request.GET.get("q", "")
        context["query"] = str(query)
    user = request.user
    ebook_posts = sorted(
        get_favourites_queryset(user, query),
        key=attrgetter("date_updated"),
        reverse=True,
    )

    # Pagination
    page = int(request.GET.get("page", "1"))
    ebook_posts_paginator = Paginator(ebook_posts, EBOOK_POSTS_PER_PAGE)

    try:
        ebook_posts = ebook_posts_paginator.page(page)
    except PageNotAnInteger:
        ebook_posts = ebook_posts_paginator.page(EBOOK_POSTS_PER_PAGE)
    except EmptyPage:
        ebook_posts = ebook_posts_paginator.page(ebook_posts_paginator.num_pages)
    context["ebook_posts"] = ebook_posts
    return render(request, "ebook/favourites.html", context)


def get_favourites_queryset(user, query=None):
    queryset = []
    queries = query.split(" ")
    for q in queries:
        posts = (
            EbookPost.objects.filter(
                Q(title__icontains=q)
                | Q(description__icontains=q)
                | Q(author__icontains=q)
            )
            .distinct()
            .filter(likes=user)
        )
        for post in posts:
            queryset.append(post)
    return list(set(queryset))
