from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class APIPagination(PageNumberPagination):
    """Page-based pagination returning {data, meta} per the API contract.

    Query params: page (default 1), perPage (default 10, max 50).
    Response:
      { "data": [...], "meta": { "page", "perPage", "total", "totalPages" } }
    """

    page_size = 10
    page_size_query_param = 'perPage'
    max_page_size = 50
    page_query_param = 'page'

    def get_paginated_response(self, data):
        return Response(
            OrderedDict([
                ('data', data),
                (
                    'meta',
                    OrderedDict([
                        ('page', self.page.number),
                        ('perPage', self.get_page_size(self.request)),
                        ('total', self.page.paginator.count),
                        ('totalPages', self.page.paginator.num_pages),
                    ]),
                ),
            ])
        )