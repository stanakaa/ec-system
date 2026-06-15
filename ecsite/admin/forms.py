from django import forms


class LoginForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    admin_id = forms.CharField(
        label="管理者ID",
        max_length=128,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    password = forms.CharField(
        label="パスワード",
        max_length=256,
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )