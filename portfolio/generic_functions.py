from distutils.log import error
from django.shortcuts import render
from django.core.paginator import Paginator

def error_page(request, error_status, message):
    return render(
        request,
        "defaultError.html",{
            "error_status": error_status,
            "error_message": message
        }, 
        status=error_status
    )

def pagination_handling(item_files, item_per_page, request):
    paginator = Paginator(item_files, item_per_page)
    pages = range(1, paginator.num_pages+1)

    page_num = request.GET.get("page")
    item_page = paginator.get_page(page_num)
    item_page_list = item_page.object_list
    return item_page_list, pages