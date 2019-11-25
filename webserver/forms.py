from django import forms
from .models import Train

class TrainForm(forms.ModelForm):
    train_no = forms.CharField(max_length=10)
    slot_no = forms.CharField(max_length=10)
    seat_no = forms.CharField(max_length=10)

    class Meta:
        model = Train
        fields = ['train_no', 'slot_no', 'seat_no', ]