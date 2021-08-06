from rest_framework import serializers
from .models import *

class NoteSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(source='colaborator')
    category = serializers.StringRelatedField()
    category_slug = serializers.SlugRelatedField(source='category',read_only=True,slug_field='slug')
    thumbnail = serializers.ImageField(source='thumb_image')
    headerImage = serializers.ImageField(source='header_image')
    publisedAt = serializers.DateTimeField(source='publish_at', format='%d/%m/%Y %I:%M %p')
    content = serializers.CharField(source = 'resume')
    tags = serializers.StringRelatedField(many=True)
    
    class Meta:
        model = Note
        fields = ('id','category_slug','slug','title','content','publisedAt','headerImage','thumbnail','author','category','tags', 'category_order','top_order')

class NoteDetailSerializer(NoteSerializer):
    
    related_notes = NoteSerializer(many=True, read_only=True)
    class Meta:
        model = Note
        fields = ('id','slug','title','content','publisedAt','thumbnail','headerImage','author','category','body','tags','body','show_signed','enable_comments','related_notes')

class CategorySerializer(serializers.ModelSerializer):
    destacada  = NoteSerializer(read_only=True, source="top_note")
    class Meta:
        model = Categories
        fields = ('name','slug','destacada')

class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banners
        fields = ('id','popup_image','popup_link','leaderboard_image','leaderboard_link','skyscraper_image','skyscraper_link','footbuttom_image','footbuttom_link','prefooter_image','prefooter_link')