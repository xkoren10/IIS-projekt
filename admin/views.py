from django.shortcuts import render, redirect
from index.views import LoginForm
import index.db_logic as db
from . import admin_db_logic as admin_db


def admin_index(request):
    try:
        if request.session["admin"]:
            return render(request, "admin/admin_index.html", {"admin": True})
    except KeyError:
        pass

    return redirect("/admin/login")


def admin_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            admin = db.password_check(form.cleaned_data["username"], form.cleaned_data["password"])
            request.session["admin"] = True
            return redirect("/admin/")
        else:
            error_msg = "Nesprávna kombinácia administátorského mena a hesla"
            return render(request, "admin/admin_login.html", {"form": form, "error": error_msg})
    else:
        request.session["admin"] = False
        form = LoginForm()

    return render(request, "admin/admin_login.html", {"form": form})


def admin_users_view(request):
    try:
        if request.session["admin"]:
            if request.method == "POST":
                operation = request.POST.keys()
                if "delete" in operation:
                    db.user_delete(request.POST["user_id"])
                elif "make_mod" in operation:
                    admin_db.toggle_mod(request.POST["user_id"])
                elif "unmake_mod" in operation:
                    admin_db.toggle_mod(request.POST["user_id"], False)
            users = admin_db.get_all_users()
            return render(request, "admin/admin_users_view.html", {"users": users})
    except KeyError:
        pass

    return redirect("/admin/login")


def admin_crops_view(request):
    try:
        if request.session["admin"]:
            return render(request, "admin/admin_crops_view.html")
    except KeyError:
        pass

    return redirect("/admin/login")


def admin_harvests_view(request):
    try:
        if request.session["admin"]:
            return render(request, "admin/admin_harvests_view.html")
    except KeyError:
        pass

    return redirect("/admin/login")


def admin_categories_view(request):
    try:
        if request.session["admin"]:
            return render(request, "admin/admin_categories_view.html")
    except KeyError:
        pass

    return redirect("/admin/login")


def admin_reviews_view(request):
    try:
        if request.session["admin"]:
            return render(request, "admin/admin_reviews_view.html")
    except KeyError:
        pass

    return redirect("/admin/login")


def admin_orders_view(request):
    try:
        if request.session["admin"]:
            return render(request, "admin/admin_orders_view.html")
    except KeyError:
        pass

    return redirect("/admin/login")


def admin_admins_view(request):
    try:
        if request.session["admin"]:
            return render(request, "admin/admin_admins_view.html")
    except KeyError:
        pass

    return redirect("/admin/login")
