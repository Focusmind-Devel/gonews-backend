from rest_framework import generics,filters, response, views
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from .serializers import *
from .models import Note
from instascrape import Profile 
import math

# Create your views here.
class MenuList(generics.ListAPIView):
    #queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    def get_queryset(self,target):
        return Categories.objects.filter(visible=True).filter(target = target).filter(note__isnull = False).distinct().order_by('order')

    def list(self, request):
        main = self.get_queryset('M')
        second = self.get_queryset('S')
        mSerialize = CategorySerializer(main, many=True)
        sSerialize = CategorySerializer(second, many=True)
        return response.Response({
            'main':mSerialize.data,
            'second':sSerialize.data
        })

class HomeConfig(generics.ListAPIView):
    serializer_class = NoteSerializer
    top_notes = None
    def get_queryset(self,category=False,last=False,main=False):
        if(category):
            tops = Note.objects.filter(category=category).filter(top=True).order_by('-category_order')[:3]
            if(len(tops)<=0):
                tops = Note.objects.filter(category=category).order_by('-publish_at')[:3]
            return tops 
        if(last):
            return Note.objects.filter(last_notes=True).order_by('-top_order')[:6]
        if(main):
            main_note = Note.objects.filter(main_note=True)
            try:
                return main_note[0]
            except:
                return Note.objects.order_by('-publish_at')[0]

    

    def list(self,request):
        self.top_notes = Note.objects.filter(top=True).order_by('category__order','category', '-category_order')
        main = self.get_queryset(main=True)
        serialize_main = self.serializer_class(main).data
        lasts = self.get_queryset(last=True)
        serialize_lasts = self.serializer_class(lasts, many=True).data

        return response.Response({
            'main':serialize_main,
            'latests':serialize_lasts,
            'categories':self.serializer_class(self.top_notes,many=True).data
        })


class NoteList(generics.ListAPIView):
    queryset = Note.objects.all().order_by('-publish_at')
    serializer_class = NoteSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter]
    filterset_fields  = ['category__slug']
    search_fields = ['title','tags__name']

class NoteRetrieve(generics.RetrieveAPIView):
    lookup_field = 'slug'
    queryset = Note.objects.all()
    serializer_class = NoteDetailSerializer

class BannerRetrieveByCategory(generics.RetrieveAPIView):
    lookup_field = 'category__slug'
    queryset = Banners.objects.filter(visible=True)
    serializer_class = BannerSerializer

    def get_object(self):
        
        #return self.queryset.get(self.kwargs[self.lookup_field])
        try:
            obj = self.queryset.get(category__slug = self.kwargs[self.lookup_field])
        except:
            obj = Banners()
        
        return obj

class BannerRetrieveNotes(views.APIView):

    def get(self,request, format=None):
        obj = get_object_or_404(Banners.objects.filter(visible=True),category__isnull=True)
        serialize = BannerSerializer(obj)
        return response.Response(serialize.data)


class InstagramRetrieveData(views.APIView):

    def get(self,request, format=None):
        def parse_post(post):
            post.scrape(headers=headers)
            parse_post = post.to_dict()
            caption = parse_post['accessibility_caption'].split("text that says") if parse_post['accessibility_caption'] else ''
            datos = {
                'id': parse_post['id'],
                'display_url' : parse_post['display_url'],
                'accessibility_caption' : caption[1].strip('\' ') if len(caption) > 1 else "",
                'full_name' : parse_post['full_name'],
                'url_link': 'https://www.instagram.com/p/'+parse_post['shortcode']
            }
            return datos

        # PASTE YOUR SESSIONID HERE
        SESSIONID = '42842070132%3AaiqQ6TN9gl0uIp%3A2'

        headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.74 Safari/537.36 Edg/79.0.309.43",
        "cookie":f'sessionid={SESSIONID};'}

        profile = Profile('gonews_ok')
        profile.scrape(headers=headers)
        scraped_data = profile.to_dict()
        scraped_data['list_posts'] = list(map(parse_post,profile.get_recent_posts(3)))
        return response.Response(scraped_data)
   