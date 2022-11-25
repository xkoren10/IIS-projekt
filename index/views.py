import datetime

from django.shortcuts import render, redirect
from django import forms
from django.http import HttpResponse
from . import db_logic as db
from . import cookie_logic as cookie


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


class HarvestForm(forms.Form):
    """
    Harvest form used in new_harvest view
    """
    date = forms.DateField(label="Dátum", initial=datetime.date.today())
    place = forms.CharField(label="Miesto", max_length=80, initial='')
    description = forms.CharField(label="Popis", max_length=80, initial='')
    max_occupancy = forms.IntegerField(label="Kapacita")
    current_occupation = forms.IntegerField(label="Obsadenosť")
    crop_id = forms.IntegerField(label="Plodina", widget=forms.Select())    # db.get_list_of_farmer_crops(famer id)


def user_logged_in(request):
    # first check if session_user was init
    try:
        user = request.session["user"]
    except KeyError:
        # set
        request.session["user"] = False
        return False

    # then check if is set to logged
    if user:
        return user
    return False


def index(request):
    top_crops = db.get_top_crops()
    new_crops = db.get_new_crops()

    user = user_logged_in(request)
    if user:
        return render(request, "index/index.html", {"logged_in": request.session["user"],
                                                    "top_crops": top_crops,
                                                    "new_crops": new_crops})
    # else
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
    user = user_logged_in(request)
    all_categories = db.get_all_categories()

    cat_filter = request.GET.keys()

    if (len(cat_filter) == 0) or ('1' in cat_filter):
        all_crops = db.get_all_crops()
    else:
        for category in cat_filter:
            filtered_crops = db.crop_get_by_category(int(category))
            all_crops.extend(filtered_crops)

    if user:
        return render(request, "index/offers.html", {"crops": all_crops, "categories": all_categories,
                                                     "logged_in": user})
    # else
    return render(request, "index/offers.html", {"crops": all_crops, "categories": all_categories,
                                                     "logged_in": False})


def harvests(request):
    harvests_models = db.harvest_get_all()
    user_id = user_logged_in(request)

    my_harvests = []
    if user_id:
        my_harvests = db.harvests_attended(user_id)
        return render(request, "index/harvests.html", {"harvests": harvests_models, "my_harvests": my_harvests,
                                                        "logged_in": user_id})
    # else
    return render(request, "index/harvests.html", {"harvests": harvests_models, "my_harvests": my_harvests,
                                                    "logged_in": False})


def new_crop(request, crop_id: int):
    if request.method == "POST":
        form = CropForm(request.POST)
        if form.is_valid():
            if request.POST['form_type'] == 'save':
                if crop_id == 0:        # nová plodina bude mať vždy id 0
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

                else:
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

    elif request.method == "GET" and crop_id == 0:
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


def profile(request, err=''):

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

        return render(request, "index/profile.html", {"user": user_profile, "form": form, "crops": farmer_crops, "orders": orders, "error": err})


def product_detail(request, product_id):
    crop_to_show = db.crop_get_by_id(product_id)
    if request.method == "POST":
        operation = request.POST.keys()
        if "delete" in operation:
            delete = db.crop_delete(product_id)
            if delete:
                err_msg = "Plodina zmazaná."
                request.method = "GET"
                return profile(request, err_msg)
        elif "add_to_cart" in operation:
            cart = cookie.add_to_cart(request, product_id, request.POST["amount"])
            response = render(request, "index/product_detail.html",
                              {"crop": crop_to_show, "user": request.session['user'], "farmer": False})
            response.set_cookie("cart", cart)
            return response

    # else
    user = user_logged_in(request)
    if user:
        if user == crop_to_show["farmer"]:
            return render(request, "index/product_detail.html",
                          {"crop": crop_to_show, "user": user, "farmer": True})
        else:
            return render(request, "index/product_detail.html",
                          {"crop": crop_to_show, "user": user, "farmer": False})

    # else
    return render(request, "index/product_detail.html",
                  {"crop": crop_to_show, "user": False, "farmer": False})


def cart_detail(request):
    user = user_logged_in(request)
    if user:
        cart = cookie.try_cookie(request, "cart")
        if request.method == "POST":
            operation = request.POST.keys()
            if "delete_one" in operation:
                cart = cookie.delete_from_cart(request, request.POST["crop_id"])
            elif "delete_order" in operation:
                cart = None
            elif "order" in operation:
                pass

        orders = cookie.get_cart(request)
        response = render(request, "index/cart_detail.html", {"user": user, "orders": orders})
        response.set_cookie("cart", cart)
        return response

    return redirect("/")


def harvest_detail(request, harvest_id):
    return render(request, "index/harvest_detail.html")


def blue_lobster(request):
    return render(request, "index/blue_lobster.html")
