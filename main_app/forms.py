from django import forms
from main_app.models import Video


class CommentForm(forms.ModelForm):
    class Meta():
        model = Video
        fields = ("description", "display_name", "category", "favorite")

        widgets = {
            'description': forms.Textarea(
                attrs={'class': 'form-control', 'id': 't-area', 'rows': '2', 'placeholder': 'Enter ideas here!'}),
            'display_name': forms.Textarea(
                attrs={'class': 'form-control', 'id': 't-area', 'rows': '1', 'placeholder': 'Give it a name'}),
            'favorite': forms.CheckboxInput(attrs={'class': 'checkbox-round'})
        }
