from rest_framework import serializers
from ebook.models import EbookPost

class EbookPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = EbookPost
        fields = ['title', 'description', 'image', 'pdf', 'date_published', 'date_updated', 'author']