from ..constants.constant import SORT_TYPE


def get_filter_params_query(data):
    page = int(data["page"]) if data.get("page") else 1
    page_size = int(data["page_size"]) if data.get("page_size") else 10
    keyword = data["keyword"] if data.get("keyword") else ""
    search_by = data["search_by"] if data.get("search_by") else ""
    sort_by = data["sort_by"] if data.get("sort_by") else ""
    sort_type = data["sort_type"] if data.get("sort_type") else SORT_TYPE.ASC

    return {
        "page": page,
        "page_size": page_size,
        "keyword": keyword,
        "search_by": search_by,
        "sort_by": sort_by,
        "sort_type": sort_type,
        **data,
    }
