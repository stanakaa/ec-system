from django.db import models
from django.core.validators import MinValueValidator


class Category(models.Model):

    class Meta:
        db_table = "shopping_category"
    
    category_id = models.IntegerField(verbose_name="カテゴリID", primary_key=True, db_index=True)
    name = models.CharField(verbose_name="カテゴリ名", max_length=256)

    def __str__(self):
        return self.name
    

class Item(models.Model):

    class Meta:
        db_table = "shopping_item"

    item_id = models.IntegerField(verbose_name="商品ID", primary_key=True, db_index=True)
    name = models.CharField(verbose_name="商品名", max_length=128)
    manufacturer = models.CharField(verbose_name="メーカー名", max_length=32)
    color = models.CharField(verbose_name="商品の色", max_length=16)
    price = models.IntegerField(verbose_name="価格")
    stock = models.IntegerField(verbose_name="在庫数")
    recommended = models.BooleanField(verbose_name="オススメ", max_length=1, default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):

    class Meta:
        db_table = "shopping_itemsincart"

    # id = models.IntegerField(verbose_name="ID", primary_key=True, autoincrement=True, db_index=True)
    amount = models.IntegerField(verbose_name="数量")
    booked_date = models.DateTimeField(verbose_name="登録日", auto_now_add=True)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.user


class Purchase(models.Model):

    class Meta:
        db_table = "shopping_purchase"

    purchase_id = models.IntegerField(verbose_name="注文ID", primary_key=True, db_index=True)
    destination = models.CharField(verbose_name="配送先", max_length=256)
    booked_date = models.DateTimeField(verbose_name="注文日", auto_now_add=True)
    cancel = models.BooleanField(verbose_name="キャンセル", max_length=1, default=False)
    user = models.ForeignKey("accounts.User", on_delete=models.CASCADE)

    def __str__(self):
        return self.purchase_id
    
class PurchaseDetail(models.Model):

    class Meta:
        db_table = "shopping_purchasedetail"

    purchase_detail_id = models.IntegerField(verbose_name="注文詳細ID", primary_key=True, db_index=True)
    amount = models.IntegerField(verbose_name="注文数", validators=[MinValueValidator(1)])
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)

    def __str__(self):
        return self.purchase_detail_id






