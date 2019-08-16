from django import template
from django.utils.http import urlencode

from utils.utils import get_attribute_from_context

register = template.Library()

@register.inclusion_tag('../templates/utils/paged_nav.html', takes_context=True)
def paging_navigation(context, page, params, *args, **kwargs):
    max_page_btn = 10
    if 'max_page_btn' in kwargs:
        max_page_btn = kwargs['max_page_btn']
    if 'show_page_info' in kwargs:
        show_page_info = True
    else:
        show_page_info = False
    if not page:
        return {}
    rng = page.paginator.page_range

    if type(page.paginator.page_range) == int:
        new_range = range(page.paginator.page_range)
    else:
        if rng.stop > max_page_btn:
            step = int(rng.stop // max_page_btn)+1
            new_range = range(rng.start, rng.stop, step)
        else:
            new_range = rng
    return {
        'page': page,
        'param': params,
        'max_page_btn': max_page_btn,
        'page_range': new_range,
        'show_page_info': show_page_info
    }



@register.simple_tag
def url_replace(request, field, value):
    d = request.GET.copy()
    d[field] = value
    return urlencode(d)


@register.simple_tag
def url_delete(request, field):
    d = request.GET.copy()
    del d[field]
    return urlencode(d)


@register.simple_tag(takes_context=True)
def param_replace(context, param, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.

    It also removes any empty parameters to keep things neat,
    so you can remove a parm by setting it to ``""``.

    For example, if you're on the page ``/things/?with_frosting=true&page=5``,
    then

    <a href="/things/?{% param_replace page=3 %}">Page 3</a>

    would expand to

    <a href="/things/?with_frosting=true&page=3">Page 3</a>

    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    #print(context)
    # if context:
    #     if hasattr(context, 'request') and hasattr(context.request, 'GET'):
    #         d = {k: v for k, v in context.request.GET.items()}
    #     elif 'request' in context and context['request'].GET:
    #         d = context['request'].GET.copy()
    #     else:
    #         d = {}
    # else:
    #     d = {}

    d = get_attribute_from_context(context, 'request.GET')

    element_per_page = get_attribute_from_context(context, 'request.POST.per_page')

    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]

    if type(param) == dict:
        for pk, pv in param.items():
            d[pk] = pv

    if element_per_page:
        d['per_page']=element_per_page

    url = urlencode(d)
    return url