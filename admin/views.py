from django.shortcuts import render, redirect
from index.views import LoginForm
import index.db_logic as db


def index(request):
    try:
        request.session["admin"]
    except KeyError:
        form = LoginForm()
        return render(request, "admin/admin_login.html", {"form": form})
    render(request, "admin/index.html")


def admin_login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            admin = db.password_check(form.cleaned_data["username"], form.cleaned_data["password"])
            request.session["admin"] = True
            return redirect("/")
        else:
            error_msg = "Nesprávna kombinácia uživateľského mena a hesla"
            return render(request, "admin/admin_login.html", {"form": form, "error": error_msg})
    else:
        request.session.clear()
        form = LoginForm()

    return render(request, "admin/admin_login.html", {"form": form})

