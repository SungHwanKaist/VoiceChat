from django import forms
from django.contrib.auth.models import User
from chat.models import Room


class ChatForm(forms.ModelForm):
	class Meta:
		model = Room
		fields = ('contact','chatname')

