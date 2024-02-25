from unittest import TestCase


class PaginationTest(TestCase):

    # Build Pagination
    def make_pagination_range(self,
                              total_pages,
                              current_page,
                              boundaries=1,
                              around=0, ):
        # Validate Values
        if not isinstance(total_pages, int) or total_pages <= 0:
            raise ValueError("total_pages must be a positive integer")
        if not isinstance(current_page, int):
            raise ValueError("current_page must be a integer and between 1 and total_pages")  # noqa: E501
        if not (1 <= current_page <= total_pages):
            raise ValueError("current_page must be between 1 and total_pages")
        if not isinstance(boundaries, int) or boundaries <= 0:
            raise ValueError("boundaries must be a positive integer")
        if not isinstance(around, int) or around < 0:
            raise ValueError("around must be a non-negative integer")

        pagination = []

        # Add beggining boundaries
        for n in range(1, boundaries + 1):
            if n <= total_pages:
                pagination.append(n)

        # Add around pages before current page
        if current_page not in pagination:
            for n in range(current_page - around, current_page):
                if n > 0 and n not in pagination:
                    if n - 1 != pagination[-1]:
                        pagination.append("...")
                    pagination.append(n)

        # Add current page
        if current_page not in pagination:
            if current_page - 1 != pagination[-1]:
                pagination.append("...")
            pagination.append(current_page)

        # Add around pages after current page
        if current_page < total_pages:
            for n in range(current_page + 1, current_page + around + 1):
                if n <= total_pages:
                    if n not in pagination:
                        if n - 1 != pagination[-1]:
                            pagination.append("...")
                        pagination.append(n)

        # Add end boundaries
        for n in range((total_pages + 1) - boundaries, total_pages + 1):
            if n <= total_pages:
                if n not in pagination:
                    if total_pages not in pagination:
                        if n - 1 != pagination[-1]:
                            pagination.append("...")
                        pagination.append(n)
        if total_pages not in pagination:
            pagination.append(total_pages)

        return pagination

    def test_if_start_page_is_1(self):
        pagination = self.make_pagination_range(total_pages=5,
                                                current_page=1,
                                                boundaries=2,
                                                around=1)
        self.assertEqual(1, pagination[0])

        pagination = self.make_pagination_range(total_pages=10,
                                                current_page=9,
                                                boundaries=1,
                                                around=0)
        self.assertEqual(1, pagination[0])

    def test_validation_cases(self):
        # total_pages = 0
        with self.assertRaises(ValueError):
            self.make_pagination_range(0, 1, 1, 1)
        # total_pages = negative
        with self.assertRaises(ValueError):
            self.make_pagination_range(-1, 1, 1, 1)
        # total_pages = non integer
        with self.assertRaises(ValueError):
            self.make_pagination_range("abc", 1, 1, 0)
        # current_page = 0
        with self.assertRaises(ValueError):
            self.make_pagination_range(5, 0, 1, 0)
        # current_page = non integer
        with self.assertRaises(ValueError):
            self.make_pagination_range(5, "abc", 1, 0)
        # current_page > total_pages
        with self.assertRaises(ValueError):
            self.make_pagination_range(5, 6, 1, 0)
        # boundaries = 0
        with self.assertRaises(ValueError):
            self.make_pagination_range(5, 1, 0, 1)
        # boundaries = negative
        with self.assertRaises(ValueError):
            self.make_pagination_range(5, 1, -1, 1)
        # boundaries = non integer
        with self.assertRaises(ValueError):
            self.make_pagination_range(5, 1, "abc", 0)
        # around = negative
        with self.assertRaises(ValueError):
            self.make_pagination_range(5, 1, 1, -1)
        # around = non integer
        with self.assertRaises(ValueError):
            self.make_pagination_range(5, 1, 1, "abc")

    def test_stop_page_is_equal_to_total_pages(self):
        pagination = self.make_pagination_range(total_pages=5,
                                                current_page=2,
                                                boundaries=1,
                                                around=0)
        self.assertEqual(5, pagination[-1])

    def test_no_direct_link_separated_by_dots(self):
        pagination = self.make_pagination_range(total_pages=5,
                                                current_page=2,
                                                boundaries=1,
                                                around=0)
        self.assertEqual([1, 2, '...', 5], pagination)

    def test_total_pages_is_1(self):
        pagination = self.make_pagination_range(total_pages=1,
                                                current_page=1,
                                                boundaries=1,
                                                around=0)
        self.assertEqual([1], pagination)

    def test_current_page_at_beginning(self):
        pagination = self.make_pagination_range(total_pages=5,
                                                current_page=1,
                                                boundaries=1,
                                                around=0)
        self.assertEqual([1, '...', 5], pagination)

    def test_current_page_at_end(self):
        pagination = self.make_pagination_range(total_pages=5,
                                                current_page=5,
                                                boundaries=1,
                                                around=0)
        self.assertEqual([1, '...', 5], pagination)

    def test_current_page_at_mid(self):
        pagination = self.make_pagination_range(total_pages=5,
                                                current_page=3,
                                                boundaries=1,
                                                around=0)
        self.assertEqual([1, '...', 3, '...', 5], pagination)

    def test_current_page_is_equal_to_total_pages(self):
        pagination = self.make_pagination_range(total_pages=5,
                                                current_page=5,
                                                boundaries=1,
                                                around=0)
        self.assertEqual([1, '...', 5], pagination)

    def test_boundaries_gt_total_pages(self):
        pagination = self.make_pagination_range(total_pages=10,
                                                current_page=4,
                                                boundaries=11,
                                                around=1)
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], pagination)

    def test_around_gt_total_pages(self):
        pagination = self.make_pagination_range(total_pages=10,
                                                current_page=4,
                                                boundaries=1,
                                                around=11)
        self.assertEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], pagination)

    def test_around_is_0(self):
        pagination = self.make_pagination_range(5, 4, 1, 0)
        self.assertEqual([1, '...', 4, 5], pagination)

    def test_pagination_example_1(self):
        pagination = self.make_pagination_range(5, 4, 1, 0)
        self.assertEqual([1, '...', 4, 5], pagination)

    def test_pagination_example_2(self):
        pagination = self.make_pagination_range(10, 4, 2, 2)
        self.assertEqual([1, 2, 3, 4, 5, 6, '...', 9, 10], pagination)
