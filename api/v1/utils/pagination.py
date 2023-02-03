from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class StandardResultsSetPagination(PageNumberPagination):
    """ Custom pagination set """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

    def get_paginated_response(self, data):
        number_of_pages = int(self.page.paginator.count / self.page_size)
        if (self.page.paginator.count % self.page_size) != 0:
            number_of_pages += 1
        return Response({
    
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'number_of_pages': number_of_pages,
            'current_page': int(self.request.GET.get('page')) if self.request.GET.get('page') else 1,
            'count': self.page.paginator.count,
            'results': data
        })
