from rest_framework.generics import ListAPIView
from django.conf import settings
import requests
from rest_framework import status




class CustomListAPIView(ListAPIView):
    def get_data_from_gecko(self,endpoint,params={}):
        headers = {
                    "accept": "application/json",
                    "x-cg-demo-api-key": settings.COINGECKO_API_KEY
                }
        url = f"{settings.COINGECKO_API_URL}{endpoint}"
        response = requests.get(url,params = params,headers=headers)

        # breakpoint()
        if response.status_code == status.HTTP_200_OK:    
            return response.json()

        return None
