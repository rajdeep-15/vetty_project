''' Views of the application are here'''

from rest_framework.permissions import IsAuthenticated
from django.core.cache import cache
from django.conf import settings
from rest_framework import status
from rest_framework.response import Response
from crypto.paginator import CustomPagination
from crypto.viewset import CustomListAPIView

# Create your views here.




class CoinListView(CustomListAPIView):
    '''View for listing list for the coins'''

    permission_class = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self, request):
        '''Get call for the view'''
        try:
            page_size = request.GET.get('page_size',10)
            page_num = request.GET.get('page_number',1)

            cache_key = 'coins_list'
            coins_data = cache.get(cache_key)

            if coins_data is None:
                coins_data = self.get_data_from_gecko(endpoint = 'coins/list')
                cache.set(cache_key,coins_data,timeout=300)

            if coins_data:
                paginator = self.pagination_class()
                paginator.page_size = int(page_size)
                paginator.page_number = int(page_num)
                page = paginator.paginate_queryset(coins_data,request)
                return paginator.get_paginated_response(page)
            return Response({'error' : "Could not fetch any data from the provider."})

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )



class CoinCategoryView(CustomListAPIView):
    ''' Class for the listing the categories of coins'''
    permisssion_class = [IsAuthenticated]
    pagination_class = CustomPagination
    def get(self, request):
        '''get call for the view'''
        try:
            page_size = request.GET.get('page_size',10)
            page_num = request.GET.get('page_number',1)
            cache_key = 'coin_category'

            category_data = cache.get(cache_key)

            if category_data is None:
                category_data = self.get_data_from_gecko(endpoint='coins/categories/list')
                cache.set(cache_key,category_data,timeout=300)
            if category_data:
                paginator = self.pagination_class()
                paginator.page_size = int(page_size)
                paginator.page_number = int(page_num)
                page = paginator.paginate_queryset(category_data,request)
                return paginator.get_paginated_response(page)
            return Response({'error':"Could not fetch any data from the provider."})

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class CoinDataView(CustomListAPIView):
    '''Class for view of market data of coins'''
    permission_class = [IsAuthenticated]
    def get(self,request):
        '''Get call for the view'''
        ids = request.GET.get('ids')
        category = request.GET.get('category')
        per_page = request.GET.get('per_page',10)
        page = request.GET.get('page',1)
        params = {
            'vs_currency':'cad',
            'per_page': per_page,
            'page': page,
        }

        if ids:
            params['ids'] = ids
        if category:
            params["category"] = category

        data = self.get_data_from_gecko(endpoint='coins/markets',params=params)

        if data:
            return Response(data)
        return Response({'error':"Could not fetch any data from the provider."})
