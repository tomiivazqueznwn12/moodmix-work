from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class UserLoginForm(AuthenticationForm):
    username = forms.CharField(max_length=100, widget=forms.widgets.TextInput(attrs={'placeholder': ' Nombre de usuario'}))
    password = forms.CharField(widget=forms.widgets.PasswordInput(attrs={'placeholder': 'Contraseña'}))

    class Meta:
        model = AuthenticationForm
        AuthenticationFormFields = ('username', 'password')
        exclude = []


class SignUpForm(UserCreationForm):
    username = forms.CharField(label="",max_length=100,required=True, widget=forms.TextInput(
        attrs={
            'placeholder':'Nombre de usuario',
            'class' : 'field'
        }
    )
)
    
    first_name = forms.CharField(label="",max_length=100,required=True,widget= forms.TextInput(
        attrs={
            'placeholder':'Nombre',
            'class' : 'field'
        }
    )
)
    
    last_name = forms.CharField(label="",max_length=100, required=False,widget= forms.TextInput(
        attrs={
            'placeholder':'Apellido',
            'class' : 'field'
        }
    )
)
    email = forms.EmailField(label="",required=True,widget= forms.TextInput(
        attrs={
            'placeholder':'Correo electronico',
            'class' : 'field'
            }
    )
)
    

    class Meta:
        model = User
        help_texts = {
            'username': None,
        }
        
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        )

        widgets = {
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password from numbers and letters of the Latin alphabet'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password confirmation'})
            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña nueva','class' : 'field'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Repite tu contraseña','class' : 'field'})
