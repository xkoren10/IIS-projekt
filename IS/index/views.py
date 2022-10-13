from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    # plus context = dict with data supposed
    return render(request, "index/index.html")


def login(request):
    return render(request, "index/login.html")


def sign_up(request):
    return render(request, "index/sign_up.html")


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

