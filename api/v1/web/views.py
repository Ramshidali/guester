from api.v1.filter.serializers import ShopTypeSerializer
from api.v1.users import serializers
from dishes.models import DISH_TIMING
from rest_framework import status
from rest_framework.decorators import (api_view, permission_classes, renderer_classes)
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from shops.models import ShopType


@api_view(['GET'])
@permission_classes((AllowAny,))
@renderer_classes((JSONRenderer,))
def categories_view(request):
    """
    for categories
    :param request:
    :return:
    """
    response_data = {}
        
    shop_types = ShopType.objects.filter(is_deleted=False)
    serialized = ShopTypeSerializer(shop_types, many=True, context={"request": request})
    
    response_data = {
        "StatusCode": 6000,
        "data" : {
            "shop_type" : serialized.data,
        }
    }
    return Response(response_data, status=status.HTTP_200_OK)