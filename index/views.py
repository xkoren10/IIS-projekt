from django.shortcuts import render
from django import forms
from django.http import HttpResponse
from . import db_logic as db


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=80)
    password = forms.CharField(label="Password", max_length=100)


def index(request):
    # plus context = dict with data supposed
    print(db.get_user_by_id(1))
    return render(request, "index/index.html")


def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            if db.password_check(form.cleaned_data["username"], form.cleaned_data["password"]):
                # set session
                return render(request, "index/index.html")
            else:
                error_msg = "Nesprávna kombinácia uživateľského mena a hesla"
                return render(request, "index/login.html", {"form": form, "error": error_msg})
    else:
        form = LoginForm()
    return render(request, "index/login.html", {"form": form})


def sign_up(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            db.user_create(form.cleaned_data["username"], form.cleaned_data["password"])
            # set session
            return render(request, "index/index.html")
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

