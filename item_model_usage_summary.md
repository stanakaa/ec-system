# ItemFormを使わずにItemモデルを使う書き方まとめ

商品データをMySQLに直接INSERTして用意する場合、`ItemForm` は必須ではありません。

この場合、Django側では `Item` モデルを使って、データベースに入っている商品データを検索・表示・カート追加・購入処理で利用します。

---

## 1. 考え方

```text
Itemモデル
→ 必要。DBの商品テーブルとつながる。

ItemForm
→ 商品登録画面・商品修正画面を作らないなら不要。

Item.objects.all()
→ 商品一覧・検索結果で使う。

Item.objects.get(item_id=item_id)
→ 商品詳細・カート追加で使う。
```

つまり、商品をDBに直接入れるなら、商品登録画面と商品修正画面のための `ItemForm` は不要です。

ただし、商品検索・商品詳細・カート・購入では、`Item` モデル自体は必ず使います。

---

## 2. products/views.py の import

`ItemForm` や `UpdateItemForm` を使わない場合、import はこのようにします。

```python
from django.shortcuts import render, redirect
from django.views.generic import View

from .forms import SearchForm, PurchaseForm
from .models import Item, ShoppingCart, Purchase, PurchaseDetail
from accounts.models import User
```

以下のような import は不要です。

```python
from .forms import ItemForm, UpdateItemForm
```

---

## 3. 商品検索結果画面での Item の使い方

商品検索では、DBに入っている `Item` を取り出します。

```python
class ShowResult(View):
    def get(self, request, *args, **kwargs):
        form = SearchForm(request.GET)

        items = Item.objects.all()
        keyword = ""
        category_name = "すべて"

        if form.is_valid():
            category = form.cleaned_data["category"]
            keyword = form.cleaned_data["keyword"]

            category_dict = dict(form.fields["category"].choices)
            category_name = category_dict[category]

            if category != "all":
                items = items.filter(category__name=category_name)

            if keyword:
                items = items.filter(name__contains=keyword)

        context = {
            "items": items,
            "keyword": keyword,
            "category_name": category_name,
            "login_user_id": request.session.get("user_id"),
            "login_name": request.session.get("name"),
        }

        return render(request, "searchResult.html", context)
```

---

## 4. 商品詳細画面での Item の使い方

商品詳細では、URLで受け取った `item_id` を使って、DBから商品を1件取り出します。

```python
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
```

---

## 5. カート追加処理での Item の使い方

カートに入れる処理でも、URLで受け取った `item_id` を使ってDBから商品を取り出します。

```python
class AddCart(View):
    def post(self, request, item_id, *args, **kwargs):
        if "user_id" not in request.session:
            return redirect("login")

        user_id = request.session["user_id"]
        user = User.objects.get(user_id=user_id)

        item = Item.objects.get(item_id=item_id)

        amount = int(request.POST.get("amount"))

        cart_item = ShoppingCart.objects.filter(user=user, item=item).first()

        if cart_item:
            cart_item.amount += amount
            cart_item.save()
        else:
            cart_item = ShoppingCart()
            cart_item.user = user
            cart_item.item = item
            cart_item.amount = amount
            cart_item.save()

        return redirect("cart")
```

---

## 6. 管理者の商品一覧での Item の使い方

商品一覧を表示するだけなら、フォームは不要です。

```python
class AdminItemList(View):
    def get(self, request, *args, **kwargs):
        if "admin_id" not in request.session:
            return redirect("admin_login")

        items = Item.objects.all()

        context = {
            "items": items,
        }

        return render(request, "adminItemList.html", context)
```

---

## 7. ItemForm を削除してよい場合

次のように、商品データをMySQLに直接INSERTして用意する場合は、`ItemForm` を削除しても大丈夫です。

```sql
INSERT INTO shopping_category (category_id, name)
VALUES
(1, '帽子'),
(2, '鞄');

INSERT INTO shopping_item
(item_id, name, manufacturer, color, price, stock, recommended, category_id)
VALUES
(1, 'キャップ', 'NIKE', '黒', 3000, 10, 1, 1),
(2, 'トートバッグ', '無印良品', '白', 2500, 8, 0, 2);
```

ただし、テーブル名やカラム名は、自分の `models.py` の `db_table` やフィールド名に合わせてください。

---

## 8. ItemForm を残した方がよい場合

次の機能を使う場合は、`ItemForm` を残します。

```text
管理者の商品登録画面
管理者の商品修正画面
```

画面から商品情報を入力してDBに保存するなら、フォームが必要です。

逆に、商品データを最初からMySQLで直接入れるだけなら、フォームは不要です。

---

## 9. まとめ

```text
商品データをDBに直接INSERTする
→ ItemFormは不要

商品検索・商品詳細・カート・購入で商品情報を使う
→ Itemモデルは必要

管理者画面から商品登録・商品修正をしたい
→ ItemForm / UpdateItemForm が必要
```
