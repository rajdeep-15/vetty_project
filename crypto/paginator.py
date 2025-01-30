from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response 

class CustomPagination(PageNumberPagination):
    page_size = 10  # Default items per page
    page_size_query_param = 'per_page'  # Allow dynamic page sizes
    max_page_size = 100
    page_number = 1

    def get_page_number(self,request,view=None):
        page_number = request.query_params.get('page_number', 1)
        
        if page_number is not None:
            try:
                page_number = int(page_number)
                if page_number < 1:
                    raise ValidationError("Page number must be greater than or equal to 1.")
                return page_number
            except ValueError:
                raise ValidationError("Invalid page number. It must be an integer.")

        return None
    
    # def paginate_queryset(self, queryset, request, view=None):
        
    #     return super().paginate_queryset(queryset, request, view)

    def get_paginated_response(self, data):
        """
        Return a paginated response with a custom structure.
        """
        return Response({
            'results': data,
            'count': len(data),  # You may want to send total count here if needed
            'page_number': self.page_number,
            'page_size': self.page_size
        })
