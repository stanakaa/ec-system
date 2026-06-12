# ec-system

insert into shopping_item()

insert into shopping_category(category_id, name) values (1, '帽子'), (2, '鞄'); 

INSERT INTO shopping_item (item_id, name, manufacturer, color, price, stock, recommended, category_id) VALUES

(101, '麦わら帽子', '日本帽子製造', '黄色', 4980, 12, TRUE, 1),
(102, '子ども用麦わら帽子', '東京帽子店', '赤色', 2980, 50, FALSE, 1),
(103, 'キャップ', '大阪アパレル', '黒色', 3500, 30, TRUE, 1),
(104, 'ニット帽', '北海道ニット', '白色', 2800, 20, FALSE, 1),
(105, 'サンバイザー', 'スポーツギア社', '青色', 2200, 15, TRUE, 1),

(201, 'トートバッグ', '京都バッグ工房', 'ベージュ', 4500, 25, TRUE, 2),
(202, 'リュックサック', 'アウトドアジャパン', '緑色', 7800, 18, TRUE, 2),
(203, 'ショルダーバッグ', '東京レザー', '茶色', 6200, 10, FALSE, 2),
(204, 'ビジネスバッグ', '日本ビジネス用品', '黒色', 12000, 8, TRUE, 2);


    item_id = models.IntegerField(verbose_name="商品ID", primary_key=True, db_index=True)
    name = models.CharField(verbose_name="商品名", max_length=128)
    manufacturer = models.CharField(verbose_name="メーカー名", max_length=32)
    color = models.CharField(verbose_name="商品の色", max_length=16)
    price = models.IntegerField(verbose_name="価格")
    stock = models.IntegerField(verbose_name="在庫数")
    recommended = models.BooleanField(verbose_name="オススメ", max_length=1, default=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    