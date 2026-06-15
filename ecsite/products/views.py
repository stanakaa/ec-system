from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Item, ShoppingCart
from accounts.models import User
from .forms import SearchForm

# http://127.0.0.1:8000/ にアクセスしたときにトップページへのリンクを表示
class Index(View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html")


class Top(View):
    def get(self, request, *args, **kwargs):
        form = SearchForm()

        context = {
            "form": form,
            "login_user_id": request.session.get("user_id"),
            "login_name": request.session.get("name"),
        }
        return render(request, "main.html", context)


class ShowResult(View):
    def get(self, request, *args, **kwargs):
        form = SearchForm(request.GET or None)
        items = Item.objects.select_related("category").all()

        keyword = ""
        category_name = "すべて"

        if form.is_valid():
            category = form.cleaned_data["category"]
            keyword = form.cleaned_data["keyword"] or ""

            if category:
                items = items.filter(category=category)
                category_name = category.name

            if keyword:
                items = items.filter(name__icontains=keyword)

        context = {
            "form": form,
            "items": items,
            "keyword": keyword,
            "category_name": category_name,
            "login_user_id": request.session.get("user_id"),
            "login_name": request.session.get("name"),
        }
        return render(request, "searchResult.html", context)
    

class ItemDetail(View):
    def get(self, request, item_id, *args, **kwargs):
        item = Item.objects.get(item_id=item_id)

        amount_list = range(1, item.stock + 1)

        context = {
            "item": item,
            "amount_list": amount_list,
            "login_user_id": request.session.get("user_id"),
            "login_name": request.session.get("name"),
        }
        return render(request, "itemDetail.html", context)
    

class AddCart(View):
    def post(self, request, item_id, *args, **kwargs):
        # ログインしていない場合はログイン画面へ
        if "user_id" not in request.session:
            return redirect("/accounts/login/?next=/products/itemDetail/" + str(item_id))

        user_id = request.session["user_id"]
        user = User.objects.get(user_id=user_id)

        item = Item.objects.get(item_id=item_id)

        amount = int(request.POST.get("amount"))

        # すでに同じ商品がカートに入っているかの確認
        cart_item = ShoppingCart.objects.filter(user=user,item=item).first()

        # カートに入れる数量が在庫数を超えないようにしてる
        if cart_item:
            cart_item.amount += amount

            if cart_item.amount > item.stock:
                cart_item.amount = item.stock

            cart_item.save()

        else:
            cart_item = ShoppingCart()
            cart_item.user = user
            cart_item.item = item

            if amount > item.stock:
                cart_item.amount = item.stock
            else:
                cart_item.amount = amount

            cart_item.save()
        return redirect("cart")
    

class ShowCart(View):
    def get(self, request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("/accounts/login/?next=/products/cart/")

        user_id = request.session["user_id"]
        user = User.objects.get(user_id=user_id)

        cart_items = ShoppingCart.objects.filter(user=user)

        cart_list = []
        total_price_all = 0

        for cart_item in cart_items:
            total_price = cart_item.item.price * cart_item.amount
            total_price_all += total_price

            cart_list.append({
                "cart_item": cart_item,
                "item": cart_item.item,
                "amount": cart_item.amount,
                "amount_list": range(1, cart_item.item.stock + 1),
                "total_price": total_price,
            })

        context = {
            "cart_list": cart_list,
            "total_price_all": total_price_all,
            "login_user_id": request.session.get("user_id"),
            "login_name": request.session.get("name"),
        }
        return render(request, "cart.html", context)


class DeleteCart(View):
    def post(self, request, cart_id, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")

        user_id = request.session["user_id"]
        user = User.objects.get(user_id=user_id)

        cart_item = ShoppingCart.objects.filter(
            id=cart_id,
            user=user,
        ).first()

        if cart_item is not None:
            cart_item.delete()

        return redirect("cart")
    

class UpdateCart(View):
    def post(self, request, cart_id, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")
        
        user_id = request.session["user_id"]
        user = User.objects.get(user_id=user_id)

        cart_item = ShoppingCart.objects.filter(id=cart_id, user=user).first()

        if cart_item is None:
            return redirect("cart")
        
        amount = int(request.POST.get("amount"))

        if amount > cart_item.item.stock:
            context = {
                "error": "数量が在庫数を超えています。",
            }
            return render(request, "cart", context)
        
        cart_item.amount = amount
        cart_item.save()

        return redirect("cart")