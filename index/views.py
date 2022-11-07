from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from . import db_logic as db


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=80)
    password = forms.CharField(label="Password", max_length=100)


def index(request):
    # plus context = dict with data supposed
    top_crops = db.get_top_crops()
    try:
        return render(request, "index/index.html", {"logged_in": request.session["user"], "top_crops": top_crops})
    except KeyError:
        return render(request, "index/index.html", {"logged_in": False})


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            db_check = db.password_check(form.cleaned_data["username"], form.cleaned_data["password"])
            if db_check:
                # set session
                request.session["user"] = True
                request.session["user_id"] = db_check
                request.session["username"] = form.cleaned_data["username"]
                return render(request, "index/index.html", {"logged_in": request.session["user"]})
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
            user_id = db.user_create(form.cleaned_data["username"], form.cleaned_data["password"])
            # set session
            request.session["user"] = True
            request.session["user_id"] = user_id
            request.session["username"] = form.cleaned_data["username"]
            return render(request, "index/index.html", {"logged_in": request.session["user"]})
    else:
        form = LoginForm()
    return render(request, "index/sign_up.html", {"form": form})


def offers(request):
    return render(request, "index/offers.html")


def farmers(request):
    return render(request, "index/farmers.html")


def harvests(request):
    return render(request, "index/harvests.html")


def product_detail(request, product_id):
    return render(request, "index/product_detail.html")


def farmer_detail(request, user_id):
    return render(request, "index/farmer_detail.html")


def harvest_detail(request, harvest_id):
    return render(request, "index/harvest_detail.html")

