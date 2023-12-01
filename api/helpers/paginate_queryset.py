from django.core import paginator


class Paginator(paginator.Paginator):
    def __init__(self, queryset, params):
        super().__init__(queryset, per_page=params.get('items_per_page'))
        self.page_number = params.get('page')

    def paginate_queryset(self):
        return self.get_page(self.page_number)

    def get_paginated_response(self, data):
        res = {
            'page_index': self.page_number,
            'page_size': self.per_page,
            'total_pages': self.num_pages,
            'total_items': self.count,
            'items': data
        }
        return res
