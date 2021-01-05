from django.shortcuts import render

def media_view(request):
    return render(request, 'index.html', context={})
