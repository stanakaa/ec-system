from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Item, ShoppingCart, Purchase as PurchaseModel, PurchaseDetail
from accounts.models import User
from .forms import SearchForm, PurchaseForm

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

        # すでに同じ商品がカートに入っているかどうかの確認
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

        cart_item = ShoppingCart.objects.filter(id=cart_id, user=user).first()

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
    

class Purchase(View):
    def get(self, request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")
        
        user_id = request.session["user_id"]
        user = User.objects.get(user_id=user_id)

        cart_items = ShoppingCart.objects.filter(user=user)

        # エラー渡してもいいかも？
        if not cart_items.exists():
            return redirect("cart")
        
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

        form = PurchaseForm(initial={
            "destination": user.address,
            "payment_mothod": "代引き"
        })

        context = {
            "form": form,
            "cart_list": cart_list,
            "total_price_all": total_price_all,
            "login_user_id": request.session.get("user_id"),
            "login_name": request.session.get("name"),
        }
        return render(request, "purchase.html", context)
    
    def post(self, request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")
        
        user_id = request.session["user_id"]
        user = User.objects.get(user_id=user_id)

        cart_items = ShoppingCart.objects.filter(user=user)

        if not cart_items.exists():
            return redirect("cart")

        form = PurchaseForm(request.POST)

        cart_list = []
        total_price_all = 0

        for cart_item in cart_items:
            total_price = cart_item.item.price * cart_item.amount
            total_price_all += total_price

            cart_list.append({
                "cart_item": cart_item,
                "item": cart_item.item,
                "amount": cart_item.amount,
                "total_price": total_price,
            })

        if not form.is_valid():
            context = {
                "form": form,
                "cart_list": cart_list,
                "total_price_all": total_price_all,
                "login_user_id": request.session.get("user_id"),
                "login_name": request.session.get("name"),
            }

            return render(request, "purchase.html", context)

        for cart_item in cart_items:
            if cart_item.amount > cart_item.item.stock:
                context = {
                    "form": form,
                    "cart_list": cart_list,
                    "total_price_all": total_price_all,
                    "error": cart_item.item.name + "の在庫が不足しています。",
                    "login_user_id": request.session.get("user_id"),
                    "login_name": request.session.get("name"),
                }

                return render(request, "purchase.html", context)

        last_purchase = PurchaseModel.objects.order_by("-purchase_id").first()

        if last_purchase is None:
            purchase_id = 1
        else:
            purchase_id = last_purchase.purchase_id + 1

        purchase = PurchaseModel(
            purchase_id=purchase_id,
            destination=form.cleaned_data["destination"],
            user=user,
        )

        purchase.save()

        # 一番最近の注文IDをとってくる
        last_purchase_detail = PurchaseDetail.objects.order_by("-purchase_detail_id").first()

        if last_purchase_detail is None:
            purchase_detail_id = 1
        else:
            purchase_detail_id = last_purchase_detail.purchase_detail_id + 1

        for cart_item in cart_items:
            purchase_detail = PurchaseDetail(
                purchase_detail_id=purchase_detail_id,
                purchase=purchase,
                item=cart_item.item,
                amount=cart_item.amount,
            )

            purchase_detail.save()

            item = cart_item.item
            item.stock = item.stock - cart_item.amount
            item.save()

            purchase_detail_id += 1

        cart_items.delete()

        context = {
            "purchase": purchase,
            "login_user_id": request.session.get("user_id"),
            "login_name": request.session.get("name"),
        }
        return render(request, "purchaseCommit.html", context)


class PurchaseHistory(View):
    def get(self, request, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")

        user_id = request.session["user_id"]
        user = User.objects.get(user_id=user_id)

        purchases = PurchaseModel.objects.filter(user=user).order_by("-booked_date")

        purchase_history_list = []

        for purchase in purchases:
            purchase_details = PurchaseDetail.objects.filter(purchase=purchase)

            detail_list = []
            total_price_all = 0

            for detail in purchase_details:
                total_price = detail.item.price * detail.amount
                total_price_all += total_price

                detail_list.append({
                    "detail": detail,
                    "item": detail.item,
                    "amount": detail.amount,
                    "total_price": total_price,
                })

            purchase_history_list.append({
                "purchase": purchase,
                "detail_list": detail_list,
                "total_price_all": total_price_all,
            })

        context = {
            "purchase_history_list": purchase_history_list,
            "login_user_id": request.session.get("user_id"),
            "login_name": request.session.get("name"),
        }
        return render(request, "purchaseHistory.html", context)