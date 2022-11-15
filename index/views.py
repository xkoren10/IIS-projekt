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


class ProfileForm(forms.Form):
    """
    Profile form used in profile view
    """
    username = forms.CharField(max_length=80, initial='')
    email = forms.CharField(max_length=100, initial='')


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
    # todo properly test and check incoming data
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


def profile(request):

    user_profile = db.user_get_by_id(request.session['user'])   # ziskame usera so session
    if not user_profile:
        return False

    if request.method == "POST":                        # zmena
        if request.POST['form_type'] == 'save':         # zmena udajov
            form = ProfileForm(request.POST)
            if form.is_valid():
                user = db.user_update(request.session['user'], form.cleaned_data["username"], form.cleaned_data["email"], user_profile['mod'])
                if user:
                    user_profile = db.user_get_by_id(request.session['user'])
                    error_msg = " Údaje úspešne zmenené"
                    return render(request, "index/profile.html", {"user": user_profile, "form": form,  "error": error_msg})
                else:
                    return False
            else:
                return False
        else:                                           # mazanie profilu
            delete = db.user_delete(request.session['user'])
            if delete:
                request.session.clear()
                form = LoginForm()
                error_msg = "Váš účet bol úspešne odstránený."
                return render(request, "index/sign_up.html", {"form": form, "error": error_msg})
            else:
                return False
    else:                       # prístup z indexu alebo cez redirect
        form = ProfileForm()
        form.fields['email'].initial = user_profile['email']
        form.fields['username'].initial = user_profile['user_name']

        return render(request, "index/profile.html", {"user": user_profile, "form": form})


def product_detail(request, product_id):
    return render(request, "index/product_detail.html")


def harvest_detail(request, harvest_id):
    return render(request, "index/harvest_detail.html")

