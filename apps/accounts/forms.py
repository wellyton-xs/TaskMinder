from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from .models import UserProfile


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        exclude = ('user', 'profession', 'address')

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        # Form control section
        for field in self.fields.values():
            field.widget.attrs.pop('autofocus', None)
            field.widget.attrs['class'] = 'form-control'

        self.fields['photo'].widget.attrs['class'] = 'form-control-file'

        self.fields['cell_phone'].widget.attrs['class'] = 'form-control phone'

        # Placeholder field
        self.fields['first_name'].widget.attrs['placeholder'] = 'Primeiro nome'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Último nome'
        self.fields['username'].widget.attrs['placeholder'] = 'Nome de Usuário'
        self.fields['email'].widget.attrs['placeholder'] = 'Endereço de email'
        self.fields['password'].widget.attrs['placeholder'] = 'Senha'
        self.fields['password_confirmation'].widget.attrs['placeholder'] = 'Confirme sua Senha'
        self.fields['cell_phone'].widget.attrs['placeholder'] = '(DDD)99999-9999'


class UserPasswordChange(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(UserPasswordChange, self).__init__(*args, **kwargs)

        for field in self.fields.values():
            field.required = True
            field.widget.attrs['class'] = 'form-control'

        self.fields['old_password'].widget.attrs['label'] = 'Senha atual'
        self.fields['new_password1'].widget.attrs['label'] = 'Nova senha'
        self.fields['new_password2'].widget.attrs['label'] = 'Confirme sua nova senha'

        self.fields['old_password'].widget.attrs['placeholder'] = 'Confirme sua senha atual'
        self.fields['new_password1'].widget.attrs['placeholder'] = 'Sua nova senha'
        self.fields['new_password2'].widget.attrs['placeholder'] = 'Confirme sua nova senha'


class ChangeProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'cell_phone', 'photo',)

    def __init__(self, *args, **kwargs):
        super(ChangeProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        self.fields['photo'].widget.attrs['class'] = 'form-control-file'
        self.fields['cell_phone'].widget.attrs['class'] = 'form-control phone'

        self.fields['first_name'].widget.attrs['placeholder'] = 'Primeiro nome'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Último nome'
        self.fields['cell_phone'].widget.attrs['placeholder'] = '(DDD)99999-9999'


class MorefeInfoUserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profession', 'address')

    def __init__(self, *args, **kwargs):
        super(MorefeInfoUserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            field.required = False

        self.fields['profession'].widget.attrs['placeholder'] = 'Full Stack Developer'
        self.fields['address'].widget.attrs['placeholder'] = 'Manaíra, João Pessoa, PB'
