from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    if "id" in request.session:
        return redirect("/dashboard")
    return render(request, "index.html")

def validate(request):
    if request.method != "POST":
        return redirect("/")
    if request.POST["action"] == "login":
        result = User.objects.login(request.POST["email"], request.POST["password"])
        if not result[0]:
            messages.add_message(request, messages.ERROR, result[1]) 
            return redirect("/")
        request.session["id"] = result[1].id
        request.session["first_name"] = result[1].first_name
        return redirect("/dashboard")
    if request.POST["action"] == "register":
        kwargs = {"first_name": request.POST["first_name"], "last_name": request.POST["last_name"], "email": request.POST["email"], "password": request.POST["password"], "vpassword": request.POST["vpassword"]}
        result = User.objects.register(**kwargs)
        if not result[0]:
            errors = result[1]
            for error in errors:
                messages.add_message(request, messages.ERROR, error) 
            return redirect("/")
        request.session["id"] = result[1].id
        request.session["first_name"] = result[1].first_name
        return redirect("/dashboard")

def dashboard(request):
    if "id" not in request.session:
        return redirect("/")
    user = User.objects.get(id = request.session["id"])
    otherWishes = Wish.objects.exclude(users_wishes = user).exclude(created = user )
    createdwishes = Wish.objects.filter(created = user)
    likewishes = Wish.objects.filter(users_wishes = user)
    context = {"otherWishes": otherWishes,"createdwishes":createdwishes,"likewishes" : likewishes }
    return render(request, "dashboard.html", context)

def create(request):
    if "id" not in request.session:
        return redirect("/")
    return render(request, "create.html")

def additem(request):
    if request.method != "POST":
        return redirect("/dashboard")
    wish = request.POST["wish"]
    checkWish = request.POST["wish"]
    if len(wish) < 4:
        messages.add_message(request, messages.ERROR, "Item must contain at least four characters.")
        return redirect("/create")
        newWish = Wish.objects.create(wish = request.POST["wish"], created = User.objects.get(id = request.session["id"])) 
        Wish.objects.create(name = newWish, created = User.objects.get(id = request.session["id"])) 
        return redirect("/dashboard")
    if Wish.objects.filter(name = checkWish, created = request.session["id"]): 
        messages.add_message(request, messages.ERROR, "Item already on your wish list.")
        return redirect("/create")
    Wish.objects.create(name = checkWish, created = User.objects.get(id = request.session["id"])) 
    return redirect("/dashboard")

def wishes(request, id):
    if "id" not in request.session:
        return redirect("/")
    thiswish = Wish.objects.get(id = id)
    context = {"wishes": Wish.objects.all().filter(id = id),'thiswish': thiswish }
    return render(request, "wishes.html", context)

def logout(request):
    if "id" not in request.session:
        return redirect("/")
    del request.session["id"]
    del request.session["first_name"]
    return redirect("/")

def removeitem(request, id):
    # if "id" not in request.session:
    user = User.objects.get(id = request.session["id"])
    wish = Wish.objects.get(id = id )
    wish.users_wishes.remove(user)
    return redirect("/dashboard")

def deleteitem(request, id):
    if "id" not in request.session or not Wish.objects.filter(id = id) or Wish.objects.filter(id = id)[0].created.id != request.session["id"]: 
        return redirect("/")
    Wish.objects.filter(id = id).delete() 
    return redirect("/dashboard")

def addfromanother(request, id):
    if "id" not in request.session or not Wish.objects.filter(id = id):
        return redirect("/")
    wish = Wish.objects.filter(id = id)[0] 
    if Wish.objects.filter(name = id, created = request.session["id"]): 
        messages.add_message(request, messages.ERROR, "Item already on your wish list.")
    else:
        user = User.objects.get(id = request.session["id"])
        wish.users_wishes.add(user)

    return redirect("/dashboard")