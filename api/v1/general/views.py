import datetime
from datetime import datetime

from rest_framework import status
from rest_framework.decorators import (api_view, permission_classes, renderer_classes)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from shops.models import ShopType
from general.models import Spotlight
from api.v1.filter.serializers import ShopTypeSerializer
from api.v1.general.serializers import SpotlightSerializer


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def spotlight(request):
    """
    spotlights
    :param request:
    :return:
    """
    response_data = {}
    
    if Spotlight.objects.filter(is_deleted=False).exists():
        instances = Spotlight.objects.filter(is_deleted=False)
        serialized = SpotlightSerializer(instances, many=True, context={"request": request})
        
        response_data = {
            "StatusCode": 6000,
            "data": serialized.data,
        }
    
    else:
        response_data = {
            "StatusCode": 6001,
            "message": "no data",
        }

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def shop_type(request):
    """
    shop type
    :param request:
    :return:
    """
    response_data = {}
    
    if ShopType.objects.filter(is_deleted=False).exists():
        instances = ShopType.objects.filter(is_deleted=False)
        serialized = ShopTypeSerializer(instances, many=True, context={"request": request})
        
        response_data = {
            "StatusCode": 6000,
            "data": serialized.data,
        }
    
    else:
        response_data = {
            "StatusCode": 6001,
            "message": "no data",
        }

    return Response(response_data, status=status.HTTP_200_OK)