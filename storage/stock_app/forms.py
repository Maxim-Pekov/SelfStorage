from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from stock_app.models import CustomUser
from django.contrib.auth import get_user_model, password_validation
from django.core.exceptions import ValidationError
from django import forms


class CreateUserForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs["class"] = "form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey"
        self.fields["email"].widget.attrs["class"] = "form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey"
        self.fields["password1"].widget.attrs["class"] = "form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey"
        self.fields["password2"].widget.attrs["class"] = "form-control border-8 mb-4 py-3 px-5 border-0 fs_24 SelfStorage__bg_lightgrey"
        self.fields["username"].widget.attrs["placeholder"] = "Ваше имя"
        self.fields["email"].widget.attrs["placeholder"] = "E-mail"
        self.fields["password1"].widget.attrs["placeholder"] = "Пароль"
        self.fields["password2"].widget.attrs["placeholder"] = "Повторите пароль"

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']


class ChangeUserForm(UserChangeForm):
    email = forms.CharField(required=True)
    phone = forms.EmailField(required=False)
    password = forms.CharField(required=True)

    # def clean(self):
    #     super().clean()
    #     password1 = self.cleaned_data['password1']
    #     password2 = self.cleaned_data['password2']
    #     if password1 and password2:
    #         if password1 != password2:
    #             errors = {
    #                 'password2': ValidationError('The two password fields did not match.',
    #                                              code='password_mismatch')
    #             }
    #             raise ValidationError(errors)
    #         password_validation.validate_password(password1, self.instance)

    class Meta:
        model = get_user_model()
        fields = ['email', 'phone', 'password']


class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'phone', 'password')
        labels = {
            'EMAIL': '',
            'PHONE': '',
            'PASSWORD': '',
        }
        widgets = {
            'customer': forms.TextInput(attrs={'class': 'consultation__form_input',
                                               'placeholder': "Введите Имя"}),
            'phone': forms.TextInput(attrs={'class': 'consultation__form_input',
                                            'placeholder': "+ 7 (999) 000 00 00"}),
        }