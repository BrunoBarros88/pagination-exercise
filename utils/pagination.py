from django.core.paginator import Paginator, EmptyPage


# Set pages to be displayed
def make_pagination_range(
    total_pages,
    current_page,
    boundaries=1,
    around=0,
):
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

    pagination_info = {
        "current_page": current_page,
        "total_pages": total_pages,
        "boundaries": boundaries,
        "around": around,
        "pagination": pagination,

    }
    print(pagination_info)

    return pagination


# Make pagination considering the pagination range, objects and request
def make_pagination(request, queryset, per_page, boundaries=1, around=0):
    paginator = Paginator(queryset, per_page)
    total_pages = paginator.num_pages

    try:
        current_page = int(request.GET.get('page', 1))
    except ValueError:
        current_page = 1

    try:
        paginated_queryset = paginator.page(current_page)
    except EmptyPage:
        paginated_queryset = paginator.page(1)

    pagination_range = make_pagination_range(total_pages,
                                             current_page,
                                             boundaries,
                                             around)

    pagination_info = {
        'current_page': current_page,
        'total_pages': total_pages,
        'per_page': per_page,
        'has_next': paginated_queryset.has_next(),
        'has_previous': paginated_queryset.has_previous(),
        'next_page_number': paginated_queryset.next_page_number() if paginated_queryset.has_next() else None,  # noqa: E501
        'previous_page_number': paginated_queryset.previous_page_number() if paginated_queryset.has_previous() else None,  # noqa: E501
        'pagination_range': pagination_range,
        'object_list': paginated_queryset.object_list,
    }

    return pagination_info
