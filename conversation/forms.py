from django import forms

from .models import ConversationMessage


class ConversationMessageForm(forms.ModelForm):
    class Meta:
        model = ConversationMessage
        fields = ("content",)
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "block w-full md:w-1/2 mx-auto py-4 px-6 rounded-xl border dark:bg-zinc-500"
                }
            )
        }
