from django import forms
from ebook.models import EbookPost


class CreateEbookPostForm(forms.ModelForm):
    class Meta:
        model = EbookPost
        fields = ['title', 'description', 'image', 'pdf', 'author']


class UpdateEbookPostForm(forms.ModelForm):
    class Meta:
        model = EbookPost
        fields = ['title', 'description', 'image', 'pdf', 'author']

    def save(self, commit=True):
        ebook_post = self.instance
        ebook_post.title = self.cleaned_data['title']
        ebook_post.description = self.cleaned_data['description']
        ebook_post.author = self.cleaned_data['author']

        if self.cleaned_data['image']:
            ebook_post.image = self.cleaned_data['image']
        if self.cleaned_data['pdf']:
            ebook_post.pdf = self.cleaned_data['pdf']
        if commit:
            ebook_post.save()
        return ebook_post
