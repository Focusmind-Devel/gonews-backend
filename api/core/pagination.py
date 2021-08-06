from rest_framework import pagination, response

class CustomPaginate(pagination.PageNumberPagination):
    page_size = 6
    def get_paginated_response(self, data):
        return response.Response({
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'current': self.page.number,
            'count': self.page.paginator.count,
            'results': data
        })

         