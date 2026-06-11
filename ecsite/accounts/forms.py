from django import forms


class RegisterForm(forms.Form):
    # 初期化処理でデフォルトでラベルに付与される「：」を削除
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""

    
    user_id = forms.CharField(label="会員ID", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="パスワード", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="パスワード(確認)", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    name = forms.CharField(label="お名前", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    address = forms.CharField(label="ご住所", max_length=256, widget=forms.TextInput(attrs={'class': 'form-control'}))

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            raise forms.ValidationError("パスワードと確認用パスワードが一致しません")


class LoginForm(forms.Form):
    user_id = forms.CharField(label="会員ID", max_length=128, widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label="パスワード", max_length=256, widget=forms.PasswordInput(attrs={'class': 'form-control'}))