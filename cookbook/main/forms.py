from django import forms

from cookbook.common.helpers import AddBootstrapFormCLassMixin

from cookbook.main.models import Recipe, Comment, Reply


class CreateRecipeForm(AddBootstrapFormCLassMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'description', 'category', 'image', ]


class EditRecipeForm(AddBootstrapFormCLassMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._init_bootstrap_form_controls()

    class Meta:
        model = Recipe
        fields = ['title', 'ingredients', 'description', 'category', 'image', ]


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Add comment here...',
                                          'class': 'form-control ml-1 shadow-none textarea',
                                          'style': 'height: 60px;',
                                          }),

        }


class CreateCommentReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['text']

        widgets = {
            'text': forms.Textarea(attrs={'placeholder': 'Add reply here...',
                                          'class': 'form-control ml-1 shadow-none textarea',
                                          'style': 'height: 60px;'
                                          }),
        }
