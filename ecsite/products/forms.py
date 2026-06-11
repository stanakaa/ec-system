from django import forms



class ChoiceForm(forms.Form):
    choice = forms.MultipleChoiceField(
        choices = (
            ('all', 'すべて'),
            ('hat', '帽子'),
            ('bag', '鞄'),
        ),
        required=True,
        widget=forms.SelectMultiple
    )


class KeywordForm(forms.Form):
    # 初期化処理でデフォルトでラベルに付与される「：」を削除
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    keywords = forms.CharField(label="キーワード", max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))