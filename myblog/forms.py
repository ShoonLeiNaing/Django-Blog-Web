from django import forms
from .models import Post,Comment
from .humanize import naturalsize
from django.core.files.uploadedfile import InMemoryUploadedFile

class PostCreateForm(forms.ModelForm):
    max_upload_limit=2*1024*1024
    max_upload_limit_text=naturalsize(max_upload_limit)
    picture=forms.FileField(required=False,label="File must be <= "+max_upload_limit_text)
    upload_file_name='picture'
    class Meta:
        model=Post
        fields=['title','context','picture']

    def clean(self):
        clean_data=super().clean()
        pic=clean_data.get('picture')
        if pic is None:
            return
        if len(pic)>self.max_upload_limit:
            self.add_error('picture',"File must be less than "+self.max_upload_limit_text+" bytes")

    def save(self, commit=True):
        instance = super(PostCreateForm, self).save(commit=False)
        f = instance.picture
        if isinstance(f, InMemoryUploadedFile):
            bytearr = f.read()
            instance.content_type = f.content_type
            instance.picture = bytearr

        if commit:
            instance.save()

        return instance

class CommentForm(forms.Form):
    text=forms.CharField(max_length=512,required=True,min_length=2,strip=True)