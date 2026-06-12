from django.shortcuts import render, redirect
from django.views.generic import View
from .models import Item
from .forms import SearchForm

# Create your views here.

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

# class ShowResult(View):
#     def get(self, request, *args, **kwargs):
#         form = SearchForm(request.GET)

#         items = Item.objects.all()

#         if form.is_valid():
#             category = form.cleaned_data["category"]
#             keyword = form.cleaned_data["keyword"]

#             category_dict = dict(form.fields["category"].choices)
#             category_name = category_dict[category]

#             if category != "all":
#                 items = items.filter(category=category)

#             if keyword:
#                 items = items.filter(name__contains=keyword)

#         context = {
#             "items": items,
#             "keyword": keyword,
#             "category_name": category_name,
#             "login_user_id": request.session.get("user_id"),
#             "login_name": request.session.get("name"),
#         }
#         return render(request, "searchResult.html", context)
    

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
    
