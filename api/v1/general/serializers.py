from general.models import Spotlight
from rest_framework import serializers



class SpotlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Spotlight
        fields = ['image']