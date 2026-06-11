from django.db import models
from django.core.validators import MinValueValidator


class User(models.Model):

    class Meta:
        db_table = "account_user"

    user_id = models.CharField(verbose_name="会員ID", max_length=128, primary_key=True, db_index=True)
    password = models.CharField(verbose_name="パスワード", max_length=256)
    name = models.CharField(verbose_name="名前", max_length=128)
    address = models.CharField(verbose_name="住所", max_length=256)

    def __str__(self):
        return self.name
    

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
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    # article = models.ForeignKey(Article, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class ShoppingCart(models.Model):

    class Meta:
        db_table = "shopping_itemsincart"

    # id = models.IntegerField(verbose_name="ID", primary_key=True, autoincrement=True, db_index=True)
    amount = models.IntegerField(verbose_name="数量")
    booked_date = models.DateTimeField(verbose_name="登録日", auto_now_add=True)
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user_id


class Purchase(models.Model):

    class Meta:
        db_table = "shopping_purchase"

    purchase_id = models.IntegerField(verbose_name="注文ID", primary_key=True, db_index=True)
    destination = models.CharField(verbose_name="配送先", max_length=256)
    booked_date = models.DateTimeField(verbose_name="注文日", auto_now_add=True)
    cancel = models.BooleanField(verbose_name="キャンセル", max_length=1, default=False)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.purchase_id
    
class PurchaseDetail(models.Model):

    class Meta:
        db_table = "shopping_purchasedetail"

    purchase_detail_id = models.IntegerField(verbose_name="注文詳細ID", primary_key=True, db_index=True)
    amount = models.IntegerField(verbose_name="注文数", validators=[MinValueValidator(1)])
    item_id = models.ForeignKey(Item, on_delete=models.CASCADE)
    purchase_id = models.ForeignKey(Purchase, on_delete=models.CASCADE)

    def __str__(self):
        return self.purchase_detail_id
    

class Admin(models.Model):

    class Meta:
        db_table = "administrator_admin"

    admin_id = models.CharField(verbose_name="管理者ID", max_length=128, primary_key=True, db_index=True)
    password = models.CharField(verbose_name="パスワード", max_length=256)

    def __str__(self):
        return self.admin_id





