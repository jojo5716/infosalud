'''from django.shortcuts import render_to_response
from infosalud.models import Entry

def search(request):
    query = request.GET.get('q', '')
    if query:
        entry_query = get_query(query, ['title', 'post',])
        entries_list = Entry.objects.filter(entry_query).order_by('-pub_date')
    else:
        entries_list = []
    return render_response(request, 'blog/list.html', {'entries': entries_list})# Create your views here.'''
def search(request):
	pass