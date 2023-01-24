from dishes.models import Cuisine
from general.models import Badge, Days, RecentLocation, RecentSearches
from rest_framework import serializers
from shops.models import ShopType

class BadgeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Badge
        fields = ['id','title','icon']
        
        
class DaysSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Days
        fields = ['id','day']
        
        
class ShopTypeSerializer(serializers.ModelSerializer):
    filter_type = serializers.SerializerMethodField()
    
    class Meta:
        model = ShopType
        fields = ['id','name',"icon","filter_type"]
        
    def get_filter_type(self,instance):
        return "shop_filter"
        

class CuisineSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Cuisine
        fields = ('id','name')
        

class ReSearchSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RecentSearches
        fields = ['id','keys']
        

class ReLocationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RecentLocation
        fields = ['id','short_name','latitude','longitude']