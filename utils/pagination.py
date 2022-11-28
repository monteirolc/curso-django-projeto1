from math import ceil


def make_pagination_range(
    page_range: list,
    qty_pages: int,
    current_page: int
):
    if len(page_range) > 0:
        current_page = abs(current_page)
        qty_pages = abs(qty_pages)
        middle_range = ceil(qty_pages / 2)
        last_page = len(page_range)
        if not current_page > last_page:
            if current_page < (last_page - middle_range):
                if current_page <= 1:
                    start_range = 0
                    stop_range = qty_pages
                else:
                    start_range = current_page - middle_range
                    stop_range = current_page + middle_range
            else:
                start_range = last_page - qty_pages
                stop_range = last_page
            pagination = page_range[start_range:stop_range]
            return {
                'pagination': pagination,
                'start_range': start_range + 1,
                'stop_range': stop_range,
                'middle_range': middle_range,
                'qty_pages': qty_pages,
                'current_page': current_page,
                'page_range': page_range,
                'total_pages': len(page_range),
            }
        else:
            raise Exception('Last page is a impossible page')
    else:
        raise Exception("Page range can't be null")
