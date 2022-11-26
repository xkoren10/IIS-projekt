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
    email = forms.CharField(label="Email", max_length=100, initial='', required=False)
    password = forms.CharField(label="Password", max_length=100, initial='', widget=forms.PasswordInput)


class CropForm(forms.Form):
    """
    Crop form used in new_crop view
    """
    crop_name = forms.CharField(label="Názov", max_length=80, initial='')
    description = forms.CharField(label="Popis", max_length=100, initial='', required=False)
    price = forms.FloatField(label="Cena")
    amount = forms.IntegerField(label="Počet")
    origin = forms.CharField(label="Pôvod", max_length=80, initial='', required=False)
    crop_year = forms.IntegerField(label="Rok", required=False)
    price_type = forms.CharField(label="Typ predaju", max_length=80, initial='')
                                 # widget=forms.Select(choices=db.get_crop_price_types())) not bueno
    category_id = forms.IntegerField(label="Kategória", widget=forms.Select(choices=db.get_list_of_categories()))


class HarvestForm(forms.Form):
    """
    Harvest form used in new_harvest view
    """
    date = forms.DateField(label="Dátum", initial=datetime.date.today())
    place = forms.CharField(label="Miesto", max_length=80, initial='')
    description = forms.CharField(label="Popis", max_length=80, initial='', required=False)
    max_occupancy = forms.IntegerField(label="Kapacita", initial=0)
    current_occupation = forms.IntegerField(label="Obsadenosť", initial=0, required=False)
    crop_id = forms.IntegerField(label="Plodina", widget=forms.Select())    # db.get_list_of_farmer_crops(famer id)


class NewCategoryForm(forms.Form):
    cat_name = forms.CharField(label="Názov kategórie")
    cat_of = forms.IntegerField(label="Je podkategóriou", widget=forms.Select(choices=db.get_list_of_categories()))


class NewReview(forms.Form):
    title = forms.CharField(label="Titulok", max_length=80, initial='')
    description = forms.CharField(label="Popis", max_length=200, initial='', required=False)
    stars = forms.IntegerField(label="Počet hviezdičiek (1-5)", max_value=5)


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

    request.session.clear()
    form = LoginForm()
    response = render(request, "index/login.html", {"form": form})
    response.delete_cookie("cart")
    return response


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
    # access restricted
    if not user_logged_in(request):
        form = LoginForm()
        return render(request, "index/login.html", {"form": form})

    all_crops = db.get_all_crops()
    user = user_logged_in(request)
    all_categories = db.category_get_all_approved()

    filters = dict(request.GET)

    if 'filter' in filters:
        if filters['filter'] != 1:
            all_crops.clear()

            for category in filters['filter']:
                filtered_crops = db.crop_get_by_category(int(category))
                all_crops.extend(filtered_crops)

    if 'sort' in filters:
        if filters['sort'] == 'descend':
            all_crops = sorted(all_crops, key=lambda d: d['price'], reverse=True)
        elif filters['sort'] == 'ascend':
            all_crops = sorted(all_crops, key=lambda d: d['price'])

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
    # access restricted
    if not user_logged_in(request):
        form = LoginForm()
        return render(request, "index/login.html", {"form": form})

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
    # access restricted
    if not user_logged_in(request):
        form = LoginForm()
        return render(request, "index/login.html", {"form": form})


    user_profile = db.user_get_by_id(request.session['user'])   # ziskame usera so session
    farmer_crops = db.get_crops_from_farmer(request.session['user'])
    orders = db.get_order_by_person_id(request.session['user'])
    reviews = db.get_user_reviews(request.session['user'])
    for review in reviews:
        review['crop'] = db.crop_get_by_id(review['crop'])['crop_name']

    # bruh, index out of range moment
    if len(orders) > 0:
        if user_profile['id'] == orders[0]['farmer']:   # ak sa zhoduje prvá, zhodujú sa všetky
            farmer = True
        else:
            farmer = False
    else:
        farmer = False

    if not user_profile:
        return False

    if request.method == "POST":                        # zmena
        operation = request.POST.keys()
        if 'save' in operation:         # zmena udajov
            form = ProfileForm(request.POST)
            if form.is_valid():
                user = db.user_update(request.session['user'], form.cleaned_data["username"], form.cleaned_data["email"], form.cleaned_data["password"], user_profile['mod'])
                if user:
                    error_msg = " Údaje úspešne zmenené"
                    return render(request, "index/profile.html", {"user": user_profile, "form": form,
                                                                  "error": error_msg, "crops": farmer_crops,
                                                                  "orders": orders, "farmer": farmer,
                                                                  "reviews": reviews})
                else:
                    return False
            else:
                return False
        elif 'delete' in operation:                                          # mazanie profilu
            delete = db.user_delete(request.session['user'])
            if delete:
                request.session.clear()
                form = LoginForm()
                error_msg = "Váš účet bol úspešne odstránený."
                return render(request, "index/sign_up.html", {"form": form, "error": error_msg, "crops": farmer_crops,
                                                              "orders": orders, "farmer": farmer, "reviews": reviews})
            else:
                return False

        elif 'confirm' in operation:
            res = db.change_order_state('confirmed', int(request.POST["order_id"]))
            if res == "amount":
                err = "Nemožno predať viac tejto plodiny než je zadaného množstva"
            orders = db.get_order_by_person_id(request.session['user'])
        elif 'refuse' in operation:
            db.change_order_state('rejected', request.POST["order_id"])
            orders = db.get_order_by_person_id(request.session['user'])

        elif 'del_review' in operation:
            deletion = db.review_delete(request.POST["review_id"])
            if deletion:
                err = "Hodnotenie bolo odstránené."
                reviews.clear()
                reviews = db.get_user_reviews(request.session['user'])
                for review in reviews:
                    review['crop'] = db.crop_get_by_id(review['crop'])['crop_name']
            else:
                err = "Hodnotenie nebolo odstránené."


    # prístup z indexu alebo cez redirect + zmena stavu
    form = ProfileForm()
    form.fields['email'].initial = user_profile['email']
    form.fields['username'].initial = user_profile['user_name']
    form.fields['password'].initial = user_profile['password']

    return render(request, "index/profile.html", {"user": user_profile, "form": form, "crops": farmer_crops,
                                                  "orders": orders, "error": err, "farmer": farmer, "reviews": reviews})


def moderation(request):
    # access restricted
    user = user_logged_in(request)
    if user:
        categories = db.get_all_categories()
        return render(request, "index/category_moderation.html", {"user": user, "categories": categories})
    form = LoginForm()
    return render(request, "index/login.html", {"form": form})


def new_category(request):
    # access restricted
    user = user_logged_in(request)
    if user:
        if request.method == "POST":
            form = NewCategoryForm(request.POST)
            if form.is_valid():
                db.category_create_new(form.cleaned_data["cat_name"], form.cleaned_data["cat_of"])
                return profile(request, err="Kategória sa odoslala na schválenie")
        form = NewCategoryForm()
        return render(request, "index/new_category.html", {"user": user, "form": form})

    form = LoginForm()
    return render(request, "index/login.html", {"form": form})


def product_detail(request, product_id):
    user = user_logged_in(request)
    crop_to_show = db.crop_get_by_id(product_id)
    reviews = db.get_reviews_for_crop(product_id)
    reviewable = False  # lebo  referencia

    if user:
        orders = db.get_order_by_person_id(user)
        for order in orders:
            if order['crop'] == crop_to_show['crop_name'] and order['state'] != 'pending':
                reviewable = True
            else:
                reviewable = False

    if request.method == "POST":
        operation = request.POST.keys()
        if "delete" in operation:
            delete = db.crop_delete(product_id)
            if delete:
                err_msg = "Plodina zmazaná."
                request.method = "GET"
                return profile(request, err_msg)

        # add crop to cart cookie
        elif "add_to_cart" in operation:
            cart = cookie.add_to_cart(request, product_id, request.POST["amount"])
            response = render(request, "index/product_detail.html",
                              {"crop": crop_to_show, "reviews": reviews,
                               "user": request.session['user'], "farmer": False, "reviewable": reviewable})
            response.set_cookie("cart", cart)
            return response

    # else

    if user:
        if user == crop_to_show["farmer"]:
            return render(request, "index/product_detail.html",
                          {"crop": crop_to_show, "reviews": reviews,
                           "user": user, "farmer": True, "reviewable": reviewable})
        else:
            return render(request, "index/product_detail.html",
                          {"crop": crop_to_show, "reviews": reviews,
                           "user": user, "farmer": False, "reviewable": reviewable})

    # else
    return render(request, "index/product_detail.html",
                  {"crop": crop_to_show, "reviews": reviews,
                   "user": False, "farmer": False, "reviewable": reviewable})


def new_review(request, crop_id):
    # access restricted
    user = user_logged_in(request)
    if user:
        if request.method == "POST":
            form = NewReview(request.POST)
            if form.is_valid():
                db.review_create_new(user, crop_id, form.cleaned_data["title"], form.cleaned_data["description"], form.cleaned_data["stars"])
                return product_detail(request, product_id=crop_id)
        form = NewReview()
        return render(request, "index/new_review.html", {"user": user, "form": form})
    form = LoginForm()
    return render(request, "index/login.html", {"form": form})


def cart_detail(request):
    # access restricted
    total = 0
    user = user_logged_in(request)
    if user:
        orders = []
        cart = cookie.try_cookie(request, "cart")
        if cart != "":
            orders = cookie.get_cart(request, cart)

        if request.method == "POST":
            operation = request.POST.keys()
            if "delete_one" in operation:
                cart = cookie.delete_from_cart(request, request.POST["crop_id"])
            elif "delete_order" in operation:
                cart = ""
            elif "order" in operation:
                db.create_new_orders(user, orders)
                cart = ""

        orders = []
        if cart != "":
            orders = cookie.get_cart(request, cart)
            if orders:
                for order in orders:
                    total = total + order["price"]

        response = render(request, "index/cart_detail.html", {"user": user, "orders": orders, "total": total})
        if cart != "":
            response.set_cookie("cart", cart)
        else:
            response.delete_cookie("cart")
        return response

    form = LoginForm()
    return render(request, "index/login.html", {"form": form})


def harvest_detail(request, harvest_id):
    return render(request, "index/harvest_detail.html")


def blue_lobster(request):
    return render(request, "index/blue_lobster.html")
