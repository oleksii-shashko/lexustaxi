from django import forms
from .models import Client


class RegForm(forms.ModelForm):
    phone_number = forms.CharField(label='Введите нормер телефона',
                                   widget=forms.TextInput(
                                       attrs={"class": "form-control phone"}
                                   ))
    login = forms.CharField(label='Введите логин',
                            widget=forms.TextInput(
                                attrs={"class": "form-control"}
                            ))
    password = forms.CharField(label='Введите пароль',
                               widget=forms.PasswordInput(
                                   attrs={"class": "form-control"}
                               ))
    password_confirm = forms.CharField(label="Введите пароль повторно",
                                       widget=forms.PasswordInput(
                                           attrs={"class": "form-control"}
                                       ))
    name = forms.CharField(label="Введите имя",
                           required=False,
                           widget=forms.TextInput(
                               attrs={"class": "form-control"}
                           ))

    class Meta:
        model = Client
        fields = ['phone_number', 'login', 'name', 'password']

    def clean(self, *args, **kwargs):
        login = self.cleaned_data.get("login")
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")

        obj = Client.objects.filter(login=login)

        if obj:
            raise forms.ValidationError('Уже есть пользователь с таким логином!')
        if not password == password_confirm:
            raise forms.ValidationError('Пароли не сходятся!')


class AuthForm(forms.Form):
    login = forms.CharField(label='Логин',
                            widget=forms.TextInput(
                                attrs={"class": "form-control"}
                            ))
    password = forms.CharField(label='Пароль',
                               widget=forms.PasswordInput(
                                   attrs={
                                       "class": "form-control",
                                       "id": "inputPassword"
                                   }
                               ))

    def clean(self, *args, **kwargs):
        login = self.cleaned_data.get("login")
        password = self.cleaned_data.get("password")

        obj = Client.objects.filter(login=login)

        if not obj or not obj.values('password')[0]['password'] == password:
            raise forms.ValidationError('Invalid login/password')

        return login
