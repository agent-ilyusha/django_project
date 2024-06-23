from django.forms import Form, CharField, DecimalField, ChoiceField
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

choices = (
    ('first', 'first'),
    ('second', 'second'),
)


class TestForm(Form):
    choice = ChoiceField(label='choice', choices=choices)
    number = DecimalField(label='number')
    text = CharField(label='text')


class RegistrationForm(UserCreationForm):
    first_name = CharField(max_length=100, required=True)
    last_name = CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class AddFundsForm(Form):
    money = DecimalField(label='money', decimal_places=2, max_digits=11)
