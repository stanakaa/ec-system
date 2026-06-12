from django import forms


class SearchForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    category = forms.ChoiceField(
        label="カテゴリ",
        choices=(
            ("all", "すべて"),
            ("hat", "帽子"),
            ("bag", "鞄"),
        ),
        required=True,
        widget=forms.Select(attrs={"class": "form-control"})
    )

    keyword = forms.CharField(
        label="キーワード",
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
