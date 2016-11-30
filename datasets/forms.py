from django import forms

from datasets.models import Dataset


class DatasetForm(forms.ModelForm):
    """
    After a while I might try and move away from boostrap, but that may never
    happen. If I do move away from bootstrap then all of these widgets will
    be changed

    Until after the initial deployment i am removing "dataset_user" and
    "dataset_password"
    """
    class Meta:
        model = Dataset
        fields = ["title", "author", "url", "public_access", "description"]
        basic_input_class = {"class": "form-control"}
        widgets = {
            "title": forms.TextInput(attrs=basic_input_class),
            "author": forms.TextInput(attrs=basic_input_class),
            "url": forms.TextInput(attrs=basic_input_class),
            "description": forms.Textarea(attrs=basic_input_class)
        }
