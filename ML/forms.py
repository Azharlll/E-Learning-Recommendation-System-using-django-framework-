from django import forms
from .models import Users,Notes

class UsersForm(forms.ModelForm):
    email = forms.EmailField(label="Email")

    class Meta:
        model = Users
        fields = ['name','surname','gender','age','standard','school_name','pincode']


class NotesForm(forms.ModelForm):

    class Meta:
        model = Notes
        fields = ['notes']
