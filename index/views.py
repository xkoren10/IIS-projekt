from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from . import db_logic as db


class LoginForm(forms.Form):
    """
    Login form used in login and sign_up views
    """
    username = forms.CharField(label="Username", max_length=80)
    password = forms.CharField(label="Password", max_length=100, widget=forms.PasswordInput)


class ProfileForm(forms.Form):
    """
    Profile form used in profile view
    """
    username = forms.CharField(label="Meno", max_length=80, initial='')
    email = forms.CharField(label="Email", max_length=100, initial='')
    password = forms.CharField(label="Password", max_length=100, initial='', widget=forms.PasswordInput)


class CropForm(forms.Form):
    """
    Crop form used in new_crop view
    """
    crop_name = forms.CharField(label="Názov", max_length=80, initial='')
    description = forms.CharField(label="Popis", max_length=100, initial='')
    price = forms.FloatField(label="Cena")
    amount = forms.IntegerField(label="Počet")
    origin = forms.CharField(label="Pôvod", max_length=80, initial='')
    crop_year = forms.IntegerField(label="Rok")
    price_type = forms.CharField(label="Typ predaju", max_length=80, initial='')
    category_id = forms.IntegerField(label="Kategória", widget=forms.Select(choices=db.get_list_of_categories()))


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

    if (len(cat_filter) == 0) or ('1' in cat_filter):
        all_crops = db.get_all_crops()
    else:
        for category in cat_filter:
            filtered_crops = db.crop_get_by_category(int(category))
            all_crops.extend(filtered_crops)

    return render(request, "index/offers.html", {"crops": all_crops, "categories": all_categories})


def harvests(request):
    return render(request, "index/harvests.html")


def new_crop(request, crop_id: int):
    if request.method == "POST":
        form = CropForm(request.POST)
        if form.is_valid():
            if request.POST['form_type'] == 'save':
                crop = db.crop_create(form.cleaned_data["crop_name"], form.cleaned_data["description"],
                                  form.cleaned_data["price"], form.cleaned_data["amount"],
                                  form.cleaned_data["origin"], form.cleaned_data["crop_year"],
                                  form.cleaned_data["price_type"], form.cleaned_data["category_id"],
                                  request.session["user"])
                if not crop:
                    error_msg = "Plodina nebola vytvorená"
                    return render(request, "index/new_crop.html", {"form": form, "error": error_msg})
                else:
                    error_msg = "Plodina bola vytvorená"
                    return render(request, "index/new_crop.html", {"form": form, "error": error_msg})

            elif request.POST['form_type'] == 'update':
                crop = db.crop_update(crop_id, form.cleaned_data["crop_name"], form.cleaned_data["description"],
                                      form.cleaned_data["price"], form.cleaned_data["amount"],
                                      form.cleaned_data["origin"], form.cleaned_data["crop_year"],
                                      form.cleaned_data["price_type"], form.cleaned_data["category_id"],
                                      request.session["user"])
                if not crop:
                    error_msg = "Plodina nebola upravená"
                    return render(request, "index/new_crop.html", {"form": form, "error": error_msg})
                else:
                    error_msg = "Plodina bola upravená"
                    return render(request, "index/new_crop.html", {"form": form, "error": error_msg})

    elif crop_id == 0:
        form = CropForm()
        return render(request, "index/new_crop.html", {"form": form})

    else:
        crop_to_update = db.crop_get_by_id(crop_id)
        # initial hodnoty z práve prehľadávanej plodiny
        form = CropForm()
        form.fields["crop_name"].initial = crop_to_update["crop_name"]
        form.fields["description"].initial = crop_to_update["description"]
        form.fields["price"].initial = crop_to_update["price"]
        form.fields["amount"].initial = crop_to_update["amount"]
        form.fields["origin"].initial = crop_to_update["origin"]
        form.fields["crop_year"].initial = crop_to_update["crop_year"]
        form.fields["price_type"].initial = crop_to_update["price_type"]
        form.fields["category_id"].initial = crop_to_update["category"]

        return render(request, "index/new_crop.html", {"form": form})


def profile(request):

    user_profile = db.user_get_by_id(request.session['user'])   # ziskame usera so session
    farmer_crops = db.get_crops_from_farmer(request.session['user'])
    orders = db.get_order_by_person_id(request.session['user'])
    if not user_profile:
        return False

    if request.method == "POST":                        # zmena
        if request.POST['form_type'] == 'save':         # zmena udajov
            form = ProfileForm(request.POST)
            if form.is_valid():
                user = db.user_update(request.session['user'], form.cleaned_data["username"], form.cleaned_data["email"], form.cleaned_data["password"], user_profile['mod'])
                if user:
                    error_msg = " Údaje úspešne zmenené"
                    return render(request, "index/profile.html", {"user": user_profile, "form": form,  "error": error_msg, "crops": farmer_crops, "orders": orders})
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
                return render(request, "index/sign_up.html", {"form": form, "error": error_msg, "crops": farmer_crops, "orders":orders})
            else:
                return False
    else:                       # prístup z indexu alebo cez redirect
        form = ProfileForm()
        form.fields['email'].initial = user_profile['email']
        form.fields['username'].initial = user_profile['user_name']
        form.fields['password'].initial = user_profile['password']

        return render(request, "index/profile.html", {"user": user_profile, "form": form, "crops": farmer_crops, "orders": orders})


def product_detail(request, product_id):
    crop_to_show = db.crop_get_by_id(product_id)

    try:
        if request.session['user'] == crop_to_show["farmer"]:
            return render(request, "index/product_detail.html",
                          {"crop": crop_to_show, "user": request.session['user'], "farmer": True})
        else:
            return render(request, "index/product_detail.html",
                          {"crop": crop_to_show, "user": request.session['user'], "farmer": False})

    except KeyError:
        return render(request, "index/product_detail.html",
                      {"crop": crop_to_show, "user": False, "farmer": False})


def harvest_detail(request, harvest_id):
    return render(request, "index/harvest_detail.html")


