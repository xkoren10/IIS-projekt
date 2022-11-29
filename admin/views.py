from django.shortcuts import render, redirect
from index.views import LoginForm
import index.db_logic as db
from . import admin_db_logic as admin_db


def admin_logged_in(request):
    try:
        return request.COOKIES["admin"]
    except KeyError:
        return False


def admin_index(request):
    admin = admin_logged_in(request)
    if admin:
        return render(request, "admin/admin_index.html", {"admin": admin})

    return redirect("/admin/login")


def admin_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            admin = db.password_check(form.cleaned_data["username"], form.cleaned_data["password"])
            response = redirect("/admin/")
            response.set_cookie("admin", admin)
            return response
        else:
            error_msg = "Nesprávna kombinácia administátorského mena a hesla"
            return render(request, "admin/admin_login.html", {"form": form, "error": error_msg})
    else:
        form = LoginForm()

    response = render(request, "admin/admin_login.html", {"form": form})
    response.delete_cookie("admin")
    return response


def admin_users_view(request):
    admin = admin_logged_in(request)
    if admin:
        if request.method == "POST":
            operation = request.POST.keys()
            if "delete" in operation:
                db.user_delete(request.POST["user_id"])
            elif "make_mod" in operation:
                admin_db.toggle_mod(request.POST["user_id"])
            elif "unmake_mod" in operation:
                admin_db.toggle_mod(request.POST["user_id"], False)
        users = admin_db.get_all_users()
        return render(request, "admin/admin_users_view.html", {"users": users, "admin": admin})

    return redirect("/admin/login")


def admin_crops_view(request):
    admin = admin_logged_in(request)
    if admin:
        if request.method == "POST":
            operation = request.POST.keys()
            if "delete" in operation:
                db.crop_delete(request.POST["crop_id"])
        crops = admin_db.get_all_crops()
        return render(request, "admin/admin_crops_view.html", {"crops": crops, "admin": admin})

    return redirect("/admin/login")


def admin_orders_view(request):
    admin = admin_logged_in(request)
    if admin:
        orders = admin_db.get_all_orders()
        return render(request, "admin/admin_orders_view.html", {"orders": orders, "admin": admin})

    return redirect("/admin/login")


def admin_harvests_view(request):
    admin = admin_logged_in(request)
    if admin:
        if request.method == "POST":
            operation = request.POST.keys()
            if "delete" in operation:
                db.harvest_delete(request.POST["harvest_id"])
        harvests = db.harvest_get_all()
        return render(request, "admin/admin_harvests_view.html", {"harvests": harvests, "admin": admin})

    return redirect("/admin/login")


def admin_categories_view(request):
    admin = admin_logged_in(request)
    if admin:
        if request.method == "POST":
            operation = request.POST.keys()
            if "delete" in operation:
                db.category_delete(request.POST["user_id"])
            elif "approve" in operation:
                db.category_approve(request.POST["cat_id"])
            elif "disallow" in operation:
                db.category_approve(request.POST["cat_id"], False)
        categories = db.get_all_categories()
        return render(request, "admin/admin_categories_view.html", {"categories": categories, "admin": admin})

    return redirect("/admin/login")


def admin_reviews_view(request):
    admin = admin_logged_in(request)
    if admin:
        if request.method == "POST":
            operation = request.POST.keys()
            if "delete" in operation:
                db.review_delete(request.POST["review_id"])
        reviews = admin_db.get_all_reviews()
        return render(request, "admin/admin_reviews_view.html", {"reviews": reviews, "admin": admin})

    return redirect("/admin/login")


def admin_admins_view(request):
    admin = admin_logged_in(request)
    if admin:
        if request.method == "POST":
            form = LoginForm(request.POST)
            if form.is_valid():
                user = admin_db.admin_create(form.cleaned_data["username"], form.cleaned_data["password"])
                # set session and go back to index page
                if not user:
                    error_msg = "Uživateľ už existuje."
                    return render(request, "admin/admin_admins_view.html", {"form": form, "error": error_msg})

                return redirect("/admin/")
        else:
            form = LoginForm()
        return render(request, "admin/admin_admins_view.html", {"form": form})

    return redirect("/admin/login")
