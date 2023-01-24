from django.shortcuts import render


def page_not_found_view(request, exception):
    return render(request, 'errors/404.html', status=404)

# def my_custom_error_view(request, exception):
    # return render(request, 'errors/500.html', status=500)

def permission_denied_view(request, exception):
    return render(request, 'errors/403.html', status=403)
