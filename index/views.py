from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from . import db_logic as db


class LoginForm(forms.Form):
    """
    Login form used in login and sign_up views
    """
    username = forms.CharField(label="Username", max_length=80)
    password = forms.CharField(label="Password", max_length=100)


def index(request):
    top_crops = db.get_top_crops()
    new_crops = db.get_new_crops()

    # todo rework call of page rendering
    try:
        return render(request, "index/index.html", {"logged_in": request.session["user"],
                                                    "top_crops": top_crops,
                                                    "new_crops": new_crops})
    except KeyError:
        return render(request, "index/index.html", {"logged_in": False,
                                                    "top_crops": top_crops,
                                                    "new_crops": new_crops})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = db.password_check(form.cleaned_data["username"], form.cleaned_data["password"])
            if user:
                # set session and go back to index page
                request.session["user"] = user.id
                return redirect("/")
            else:
                error_msg = "Nesprávna kombinácia uživateľského mena a hesla"
                return render(request, "index/login.html", {"form": form, "error": error_msg})
    else:
        request.session.clear()
        form = LoginForm()
    return render(request, "index/login.html", {"form": form})


def sign_up(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = db.user_create(form.cleaned_data["username"], form.cleaned_data["password"])
            # set session and go back to index page
            if not user:
                error_msg = "Uživateľ už existuje."
                return render(request, "index/sign_up.html", {"form": form, "error": error_msg})

            request.session["user"] = user.id
            return redirect("/")
    else:
        form = LoginForm()
    return render(request, "index/sign_up.html", {"form": form})


def offers(request):
    all_crops = []
    all_categories = db.get_all_categories()

    cat_filter = request.GET.keys()

    if len(cat_filter) == 0:
        all_crops = db.get_all_crops()
    else:
        all_crops = db.get_all_crops()

    return render(request, "index/offers.html", {"crops": all_crops, "categories": all_categories})


def harvests(request):
    return render(request, "index/harvests.html")


def product_detail(request, product_id):
    return render(request, "index/product_detail.html")


def harvest_detail(request, harvest_id):
    return render(request, "index/harvest_detail.html")

