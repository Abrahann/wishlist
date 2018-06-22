from django.shortcuts import render, redirect
from .models import User, Item, Wish
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
    wishes = Wish.objects.all().filter(user_id = request.session["id"])
    allWishes = Wish.objects.all().exclude(user_id = request.session["id"])
    context = {"wishes": wishes, "allWishes": allWishes}
    return render(request, "dashboard.html", context)

def create(request):
    if "id" not in request.session:
        return redirect("/")
    return render(request, "create.html")

def additem(request):
    if request.method != "POST":
        return redirect("/dashboard")
    item = request.POST["item"]
    if len(item) < 4:
        messages.add_message(request, messages.ERROR, "Item must contain at least four characters.")
        return redirect("/create")
        checkItem = Item.objects.filter(item__icontains = request.POST["item"]) 
        newItem = Item.objects.create(item = request.POST["item"], user_id = User.objects.get(id = request.session["id"])) 
        Wish.objects.create(item_id = newItem, user_id = User.objects.get(id = request.session["id"])) 
        return redirect("/dashboard")
    if Wish.objects.filter(item_id = checkItem, user_id = request.session["id"]): 
        messages.add_message(request, messages.ERROR, "Item already on your wish list.")
        return redirect("/create")
    Wish.objects.create(item_id = checkItem[0], user_id = User.objects.get(id = request.session["id"])) 
    return redirect("/dashboard")

def wishes(request, id):
    if "id" not in request.session:
        return redirect("/")
    context = {"wishes": Wish.objects.all().filter(item_id = id)}
    return render(request, "wishes.html", context)

def logout(request):
    if "id" not in request.session:
        return redirect("/")
    del request.session["id"]
    del request.session["first_name"]
    return redirect("/")

def removeitem(request, id):
    if "id" not in request.session:
        return redirect("/") 
    Wish.objects.filter(user_id = request.session["id"], item_id = id).delete() 
    return redirect("/dashboard")

def deleteitem(request, id):
    if "id" not in request.session or not Item.objects.filter(id = id) or Item.objects.filter(id = id)[0].user_id.id != request.session["id"]: 
        return redirect("/")
    Item.objects.filter(id = id).delete() 
    return redirect("/dashboard")

def addfromanother(request, id):
    if "id" not in request.session or not Item.objects.filter(id = id):
        return redirect("/")
    item = Item.objects.filter(id = id)[0] 
    if Wish.objects.filter(item_id = id, user_id = request.session["id"]): 
        messages.add_message(request, messages.ERROR, "Item already on your wish list.")
    else:
        Wish.objects.create(item_id = item, user_id = User.objects.get(id = request.session["id"])) 
    return redirect("/dashboard")