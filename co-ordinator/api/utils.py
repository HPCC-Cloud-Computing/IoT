from . import serializers
from rest_framework.response import Response
from collections import OrderedDict
from django.utils.translation import ugettext as _

OK = {
    "code": "OK",
    "message": _("Success")
}

class EsPaging:
    pass


def es_paging(es_query, request, page=None, item_per_page=None):
    if not page:
        page = int(request.GET.get("page", "1"))
    if not item_per_page:
        item_per_page = int(request.GET.get("perPage", 10))
    start = (page - 1) * item_per_page
    end = start + item_per_page
    paginator = EsPaging()
    data = es_query[start:end].execute().hits
    paginator.data = data.hits
    paginator.num_pages = data.total
    paginator.current_page = page
    return paginator

def ok(data=None, paginator=None):
    msg = OrderedDict()
    msg['meta'] = OrderedDict()
    msg['meta']["code"] = OK["code"]
    msg['meta']["message"] = OK["message"]
    if data:
        msg['data'] = data
    if paginator:
        msg['pagination'] = {
            "num_pages": paginator.num_pages,
            "current_page": paginator.current_page,
        }
    return Response(msg)

def restrict_search(request, key, es_query):
    paginator = es_paging(es_query, request)
    serialization = serializers.es_serialize(paginator.data)
    return ok({key: serialization}, paginator)
