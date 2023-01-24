import datetime
from django.db.models import Q
from django.core.management.base import BaseCommand, CommandError
from shops.models import ShopOffer, DishOffer, BrandOffer

class Command(BaseCommand):


    def handle(self, *args, **options):
        now = datetime.datetime.now()
        
        ShopOffer.objects.filter(start_date__lte = now, end_date__gte = now).exclude(is_deleted = True).update(is_active=True)
        ShopOffer.objects.filter(Q(start_date__gt = now)|Q(end_date__lt =now)).exclude(is_deleted = True).update(is_active=False)
        
        DishOffer.objects.filter(start_date__lte = now, end_date__gte = now).exclude(is_deleted = True).update(is_active=True)
        DishOffer.objects.filter(Q(start_date__gt = now)|Q(end_date__lt =now)).exclude(is_deleted = True).update(is_active=False)
        
        BrandOffer.objects.filter(start_date__lte = now, end_date__gte = now).exclude(is_deleted = True).update(is_active=True)
        BrandOffer.objects.filter(Q(start_date__gt = now)|Q(end_date__lt =now)).exclude(is_deleted = True).update(is_active=False)
