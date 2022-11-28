from unittest import TestCase

from utils.pagination import make_pagination_range


class PaginationTest(TestCase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

    def test_first_range_is_static_if_current_page_is_less_than_middle_page(
        self
    ):
        # Current page 1 midle_page 2
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )
        self.assertEqual([2, 3, 4, 5], pagination['pagination'])

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=6,
        )
        self.assertEqual([5, 6, 7, 8], pagination['pagination'])

    def test_middle_ranges_are_correct(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=6,
            current_page=10,
        )
        self.assertEqual([8, 9, 10, 11, 12, 13], pagination['pagination'])

    def test_final_range_is_the_last_page(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19,
        )
        self.assertEqual([17, 18, 19, 20], pagination['pagination'])

        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=6,
            current_page=20,
        )
        self.assertEqual([15, 16, 17, 18, 19, 20], pagination['pagination'])

    def test_pagination_ignore_negative_page_values(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=-4,
            current_page=-2,
        )
        self.assertEqual([1, 2, 3, 4], pagination['pagination'])

    def test_if_page_range_is_invalid_returns_raise_exeption(self):
        with self.assertRaises(Exception):
            make_pagination_range(
                page_range=list(range(-1, -21)),
                qty_pages=4,
                current_page=19,
            )

    def test_if_current_page_is_greater_then_last_page_returns_raise(self):
        with self.assertRaises(Exception):
            make_pagination_range(
                page_range=list(range(1, 21)),
                qty_pages=4,
                current_page=21,
            )

    def test_check_if_the_pagination_returns_is_a_valid_return(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 15)),
            qty_pages=6,
            current_page=5
        )
        self.assertEqual([3, 4, 5, 6, 7, 8], pagination['pagination'])
        self.assertEqual(3, pagination['start_range'])
        self.assertEqual(8, pagination['stop_range'])
        self.assertEqual(3, pagination['middle_range'])
        self.assertEqual(5, pagination['current_page'])
        self.assertEqual(6, pagination['qty_pages'])
        self.assertEqual(list(range(1, 15)), pagination['page_range'])
        self.assertEqual(len(list(range(1, 15))), pagination['total_pages'])
