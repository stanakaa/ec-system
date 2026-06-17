from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Admin
from products.models import Category, Item, ShoppingCart, Purchase as PurchaseModel, PurchaseDetail
from .forms import LoginForm, ItemRegisterForm, ItemUpdateForm, AdminPurchaseHistorySearchForm


class adminLogin(View):
    def get(self, request, *args, **kwargs):
        form = LoginForm()

        context = {
            "form": form,
        }
        return render(request, "adminLogin.html", context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "adminLogin.html", context)

        admin_id = form.cleaned_data["admin_id"]
        password = form.cleaned_data["password"]

        admin = Admin.objects.filter(admin_id=admin_id, password=password).first()

        if admin is None:
            context = {
                "form": form,
                "error": "管理者ID、またはパスワードが間違っています。",
            }
            return render(request, "adminLogin.html", context)

        request.session["admin_id"] = admin.admin_id

        return redirect("admin_main")


class adminMain(View):
    def get(self, request, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("admin_login")

        context = {
            "admin_id": request.session["admin_id"],
        }
        return render(request, "adminMain.html", context)
    

class adminLogout(View):
    def get(self, request, *args, **kwargs):
        if "admin_id" in request.session:
            del request.session["admin_id"]

        return redirect("admin_login")


class ItemList(View):
    def get(self, request, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("admin_login")

        keyword = request.GET.get("keyword", "")
        category_id = request.GET.get("category_id", "all")

        items = Item.objects.all()

        if keyword != "":
            items = items.filter(name__contains=keyword)

        if category_id != "all":
            items = items.filter(category_id=category_id)

        items = items.order_by("item_id")
        categories = Category.objects.all().order_by("category_id")

        context = {
            "items": items,
            "categories": categories,
            "keyword": keyword,
            "selected_category_id": category_id,
        }
        return render(request, "adminItemList.html", context)


class ItemRegister(View):
    def get(self, request, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("admin_login")

        form = ItemRegisterForm()

        context = {
            "form": form,
        }
        return render(request, "adminItemRegister.html", context)

    def post(self, request, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("admin_login")

        form = ItemRegisterForm(request.POST)

        if not form.is_valid():
            context = {
                "form": form,
            }
            return render(request, "adminItemRegister.html", context)

        item_id = form.cleaned_data["item_id"]
        name = form.cleaned_data["name"]
        category = form.cleaned_data["category"]
        manufacturer = form.cleaned_data["manufacturer"]
        color = form.cleaned_data["color"]
        price = form.cleaned_data["price"]
        stock = form.cleaned_data["stock"]
        recommended = form.cleaned_data["recommended"]

        if Item.objects.filter(item_id=item_id).exists():
            context = {
                "form": form,
                "error": "この商品IDはすでに使われています。",
            }
            return render(request, "adminItemRegister.html", context)

        item = Item(
            item_id=item_id,
            name=name,
            category=category,
            manufacturer=manufacturer,
            color=color,
            price=price,
            stock=stock,
            recommended=recommended
        )

        item.save()

        return redirect("item_list")


class ItemUpdate(View):
    # UserUpdateを使いまわせそう
    def get(self, request, item_id, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("admin_login")

        item = Item.objects.filter(item_id=item_id).first()

        if item is None:
            return redirect("item_list")

        form = ItemUpdateForm(initial={
            "item_id": item.item_id,
            "name": item.name,
            "category": item.category,
            "manufacturer": item.manufacturer,
            "color": item.color,
            "price": item.price,
            "stock": item.stock,
            "recommended": item.recommended,
        })

        context = {
            "form": form,
            "item": item,
        }
        return render(request, "adminItemUpdate.html", context)

    def post(self, request, item_id, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("admin_login")

        old_item = Item.objects.filter(item_id=item_id).first()

        if old_item is None:
            return redirect("item_list")

        form = ItemUpdateForm(request.POST)

        if not form.is_valid():
            context = {
                "form": form,
                "item": old_item,
            }

            return render(request, "adminItemUpdate.html", context)

        new_item_id = form.cleaned_data["item_id"]

        # 商品IDに変更があったとき
        if new_item_id != old_item.item_id:
            if Item.objects.filter(item_id=new_item_id).exists():
                context = {
                    "form": form,
                    "item": old_item,
                    "error": "この商品IDはすでに使われています。",
                }
                return render(request, "adminItemUpdate.html", context)

            new_item = Item(
                item_id=new_item_id,
                name=form.cleaned_data["name"],
                category=form.cleaned_data["category"],
                manufacturer=form.cleaned_data["manufacturer"],
                color=form.cleaned_data["color"],
                price=form.cleaned_data["price"],
                stock=form.cleaned_data["stock"],
                recommended=form.cleaned_data["recommended"],
            )

            new_item.save()

            # データベースのレコードをアップデート
            ShoppingCart.objects.filter(item=old_item).update(item=new_item)
            PurchaseModel.objects.filter(item=old_item).update(item=new_item)

            old_item.delete()
        
        # 商品IDに変更がなければそのままのものを使う
        else:
            old_item.name = form.cleaned_data["name"]
            old_item.category = form.cleaned_data["category"]
            old_item.manufacturer = form.cleaned_data["manufacturer"]
            old_item.color = form.cleaned_data["color"]
            old_item.price = form.cleaned_data["price"]
            old_item.stock = form.cleaned_data["stock"]
            old_item.recommended = form.cleaned_data["recommended"]

            old_item.save()

        return redirect("item_list")


class ItemDelete(View):
    def get(self, request, item_id, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("admin_login")

        item = Item.objects.filter(item_id=item_id).first()

        if item is None:
            return redirect("item_list")

        context = {
            "item": item,
        }

        return render(request, "adminItemDelete.html", context)

    def post(self, request, item_id, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("admin_login")

        item = Item.objects.filter(item_id=item_id).first()

        if item is None:
            return redirect("item_list")

        # 購入履歴が存在する商品は削除できないようにしておく（いらんかも）
        # if PurchaseModel.objects.filter(item=item).exists():
        #     context = {
        #         "item": item,
        #         "error": "この商品は購入履歴に存在するため、削除できません。",
        #     }

        #     return render(request, "adminItemDelete.html", context)

        ShoppingCart.objects.filter(item=item).delete()
        item.delete()

        return redirect("item_list")
    


class AdminPurchaseHistory(View):
    def get(self, request, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("admin_login")

        form = AdminPurchaseHistorySearchForm(request.GET)

        purchases = PurchaseModel.objects.all().order_by("-booked_date")

        if form.is_valid():
            purchase_id = form.cleaned_data["purchase_id"]
            user_id = form.cleaned_data["user_id"]
            item_name = form.cleaned_data["item_name"]
            cancel = form.cleaned_data["cancel"]

            if purchase_id is not None:
                purchases = purchases.filter(purchase_id=purchase_id)

            if user_id != "":
                purchases = purchases.filter(user__user_id__contains=user_id)

            if item_name != "":
                purchase_ids = PurchaseDetail.objects.filter(
                    item__name__contains=item_name
                ).values_list("purchase_id", flat=True)

                purchases = purchases.filter(purchase_id__in=purchase_ids)

            if cancel == "not_cancel":
                purchases = purchases.filter(cancel=False)

            if cancel == "cancel":
                purchases = purchases.filter(cancel=True)

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
            "form": form,
            "purchase_history_list": purchase_history_list,
        }

        return render(request, "adminPurchaseHistory.html", context)


class PurchaseCancel(View):
    def get(self, request, purchase_id, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("admin_login")

        purchase = PurchaseModel.objects.filter(purchase_id=purchase_id).first()

        if purchase is None:
            return redirect("admin_purchase_history")

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

        context = {
            "purchase": purchase,
            "detail_list": detail_list,
            "total_price_all": total_price_all,
        }

        return render(request, "adminPurchaseCancel.html", context)

    def post(self, request, purchase_id, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("admin_login")

        purchase = PurchaseModel.objects.filter(purchase_id=purchase_id).first()

        if purchase is None:
            return redirect("admin_purchase_history")

        if purchase.cancel:
            context = {
                "purchase": purchase,
                "error": "この注文はすでにキャンセル済みです。",
            }

            return render(request, "adminPurchaseCancel.html", context)

        purchase_details = PurchaseDetail.objects.filter(purchase=purchase)

        for detail in purchase_details:
            item = detail.item
            item.stock = item.stock + detail.amount
            item.save()

        purchase.cancel = True
        purchase.save()

        return redirect("admin_purchase_history")