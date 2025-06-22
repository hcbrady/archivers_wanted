from django.shortcuts import render, get_object_or_404
from .models import Opportunity, Tag

def opportunity_list(request):
    tag_name = request.GET.get('tag')
    if tag_name:
        opportunities = Opportunity.objects.filter(tags__name=tag_name)
    else:
        opportunities = Opportunity.objects.all()
    
    tags = Tag.objects.all()
    return render(request, 'participation/opportunity_list.html', {
        'opportunities': opportunities,
        'tags': tags,
        'selected_tag': tag_name,
    })

def opportunity_detail(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    return render(request, 'participation/opportunity_detail.html', {'opportunity': opportunity})