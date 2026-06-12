from django import forms
from .models import Category



class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    category = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by("category_id"),
        label="カテゴリ",
        required=False,
        empty_label="すべて"
    )

    keyword = forms.CharField(label="キーワード", required=False, max_length=100)


# class SearchForm(forms.Form):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.label_suffix = ""

#     category = forms.ChoiceField(
#         label="カテゴリ",
#         choices=(
#             ("all", "すべて"),
#             ("hat", "帽子"),
#             ("bag", "鞄"),
#         ),
#         required=True,
#         widget=forms.Select(attrs={"class": "form-control"})
#     )

#     keyword = forms.CharField(
#         label="キーワード",
#         max_length=255,
#         required=False,
#         widget=forms.TextInput(attrs={"class": "form-control"})
#     )
