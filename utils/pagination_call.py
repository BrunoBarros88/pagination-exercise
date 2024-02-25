from pagination import make_pagination_range, make_pagination


# Call make_pagination_range
total_pages = 10
current_page = 4
boundaries = 2
around = 2

make_pagination_range(total_pages, current_page, boundaries, around)


# Create 100 dummy objects
class DummyObject:
    def __init__(self, name):
        self.name = name


dummy_objects = [DummyObject(f"Object {i+1}") for i in range(100)]


# Create dummy request
class DummyRequest:
    def __init__(self, page):
        self.GET = {'page': page}


dummy_request = DummyRequest(page=4)

# Call make_pagination using the dummy data
pagination_info = make_pagination(dummy_request,
                                  dummy_objects,
                                  per_page=10,
                                  boundaries=2,
                                  around=2)
