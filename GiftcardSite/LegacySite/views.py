import json
from django.shortcuts import render, redirect
from django.http import HttpResponse
from LegacySite.models import User, Product, Card
from . import extras
from django.views.decorators.csrf import csrf_protect as csrf_protect
from django.contrib.auth import login, authenticate, logout
from django.core.exceptions import ObjectDoesNotExist

SALT_LEN = 16

# Create your views here.
# Landing page. Nav bar, most recently bought cards, etc.
def index(request): 
    context= {'user': request.user}
    return render(request, "index.html", context)

# Register for the service.
def register_view(request):
    if request.method == 'GET':
        return render(request, "register.html", {'method':'GET'})
    else:
        context = {'method':'POST'}
        uname = request.POST.get('uname', None)
        pword = request.POST.get('pword', None)
        pword2 = request.POST.get('pword2', None)
        assert (None not in [uname, pword, pword2])
        if pword != pword2:
            context["success"] = False
            return render(request, "register.html", context)
        salt = extras.generate_salt(SALT_LEN)
        hashed_pword = extras.hash_pword(salt, pword)
        hashed_pword = salt.decode('utf-8') + '$' + hashed_pword
        u = User(username=uname, password=hashed_pword)
        u.save()
        return redirect("index.html")
        

# Log into the service.
def login_view(request):
    if request.method == "GET":
        return render(request, "login.html", {'method':'GET', 'failed':False})
    else:
        context = {'method':'POST'}
        uname = request.POST.get('uname', None)
        pword = request.POST.get('pword', None)
        assert (None not in [uname, pword])
        user = authenticate(username=uname, password=pword)
        if user is not None:
            context['failed'] = False
            login(request, user)
            print("Logged in user")
        else:
            context['failed'] = True
            return render(request, "login.html", context)
        return redirect("index.html")

# Log out of the service.
def logout_view(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect("index.html")

def buy_card_view(request, prod_num=0):
    if request.method == 'GET':
        context = {"prod_num" : prod_num}
        director = request.GET.get('director', None)
        if director is not None:
            # KG: Wait, what is this used for? Need to check the template.
            context['director'] = director
        if prod_num != 0:
            try:
                prod = Product.objects.get(product_id=prod_num) 
            except:
                return HttpResponse("ERROR: 404 Not Found.")
        else:
            try:
                prod = Product.objects.get(product_id=1) 
            except:
                return HttpResponse("ERROR: 404 Not Found.")
        context['prod_name'] = prod.product_name
        context['prod_path'] = prod.product_image_path
        context['price'] = prod.recommended_price
        context['description'] = prod.description
        return render(request, "item-single.html", context)
    elif request.method == 'POST':
        if prod_num == 0:
            prod_num = 1
        num_cards = len(Card.objects.filter(user=request.user))
        # Generate a card here, based on amount sent. Need binary for this.
        card_file_path = f"/tmp/addedcard_{request.user.id}_{num_cards + 1}.gftcrd'"
        card_file_name = "newcard.gftcrd"
        # Use binary to write card here.
        # Create card record with data.
        # For now, until we get binary, write random data.
        prod = Product.objects.get(product_id=prod_num)
        amount = request.POST.get('amount', None)
        if amount is None or amount == '':
            amount = prod.recommended_price
        extras.write_card_data(card_file_path, prod, amount, request.user)
        card_file = open(card_file_path, 'rb')
        card = Card(data=card_file.read(), product=prod, amount=amount, fp=card_file_path, user=request.user)
        card.save()
        card_file.seek(0)
        response = HttpResponse(card_file, content_type="application/octet-stream")
        response['Content-Disposition'] = f"attachment; filename={card_file_name}"
        return response
        #return render(request, "item-single.html", {})
    else:
        return redirect("/buy/1")

# KG: What stops an attacker from making me buy a card for him?
def gift_card_view(request, prod_num=0):
    context = {"prod_num" : prod_num}
    if request.method == "GET":
        context['user'] = None
        director = request.GET.get('director', None)
        if director is not None:
            context['director'] = director
        if prod_num != 0:
            try:
                prod = Product.objects.get(product_id=prod_num) 
            except:
                return HttpResponse("ERROR: 404 Not Found.")
        else:
            try:
                prod = Product.objects.get(product_id=1) 
            except:
                return HttpResponse("ERROR: 404 Not Found.")
        context['prod_name'] = prod.product_name
        context['prod_path'] = prod.product_image_path
        context['price'] = prod.recommended_price
        context['description'] = prod.description
        return render(request, "gift.html", context)
    elif request.method == "POST":
        if prod_num == 0:
            prod_num = 1
        user = request.POST.get('username', None)
        if user is None:
            return HttpResponse("ERROR 404")
        try:
            user_account = User.objects.get(username=user)
        except:
            user_account = None
        if user_account is None:
            context['user'] = None
            return render(request, f"gift.html", context)
        context['user'] = user_account
        num_cards = len(Card.objects.filter(user=user_account))
        card_file_path = f"/tmp/addedcard_{user_account.id}_{num_cards + 1}.gftcrd'"
        extras.write_card_data(card_file_path)
        prod = Product.objects.get(product_id=prod_num)
        card_file = open(card_file_path, 'rb')
        card = Card(data=card_file.read(), product=prod, amount=request.POST.get('amount', prod.recommended_price), fp=card_file_path, user=user_account)
        card.save()
        card_file.close()
        return render(request, f"gift.html", context)

def use_card_view(request):
    context = {'card_found':None}
    if request.method == 'GET':
        if not request.user.is_authenticated:
            return redirect("login.html")
        try:
            user_cards = Card.objects.filter(user=request.user).filter(used=False)
        except ObjectDoesNotExist:
            user_cards = None
        context['card_list'] = user_cards
        context['card'] = None
        return render(request, 'use-card.html', context)
    elif request.method == "POST" and request.POST.get('card_supplied', False):
        # Post with specific card, use this card.
        context['card_list'] = None
        # Need to write this to parse card type.
        card_file_data = request.FILES['card_data']
        card_fname = request.POST.get('card_fname', None)
        if card_fname is None or card_fname == '':
            card_file_path = f'/tmp/newcard_{request.user.id}_parser.gftcrd'
        else:
            card_file_path = f'/tmp/{card_fname}_{request.user.id}_parser.gftcrd'
        card_data = extras.parse_card_data(card_file_data.read(), card_file_path)
        # check if we know about card.
        # KG: Where is this data coming from? RAW SQL usage with unkown
        # KG: data seems dangerous.
        print(card_data.strip())
        signature = json.loads(card_data)['records'][0]['signature']
        # signatures should be pretty unique, right?
        card_query = Card.objects.raw('select id from LegacySite_card where data = \'%s\'' % signature)
        user_cards = Card.objects.raw('select id, count(*) as count from LegacySite_card where LegacySite_card.user_id = %s' % str(request.user.id))
        card_query_string = ""
        for thing in card_query:
            # print cards as strings
            card_query_string += str(thing) + '\n'
        if len(card_query) is 0:
            # card not known, add it.
            if card_fname is not None:
                card_file_path = f'/tmp/{card_fname}_{request.user.id}_{user_cards[0].count + 1}.gftcrd'
            else:
                card_file_path = f'/tmp/newcard_{request.user.id}_{user_cards[0].count + 1}.gftcrd'
            fp = open(card_file_path, 'w')
            fp.write(card_data)
            fp.close()
            card = Card(data=card_data, fp=card_file_path, user=request.user, used=True)
        else:
            context['card_found'] = card_query_string
            try:
                card = Card.objects.get(data=card_data)
                card.used = True
            except ObjectDoesNotExist:
                card = None
        context['card'] = card
        return render(request, "use-card.html", context) 
    elif request.method == "POST":
        card = Card.objects.get(id=request.POST.get('card_id', None))
        card.used=True
        card.save()
        context['card'] = card
        try:
            user_cards = Card.objects.filter(user=request.user).filter(used=False)
        except ObjectDoesNotExist:
            user_cards = None
        context['card_list'] = user_cards
        return render(request, "use-card.html", context)
    return HttpResponse("Error 404: Internal Server Error")

