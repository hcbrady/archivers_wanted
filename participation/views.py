from django.shortcuts import render, get_object_or_404
from .models import Opportunity

def opportunity_list(request):
    opportunities = Opportunity.objects.all()
    return render(request, 'participation/opportunity_list.html', {'opportunities': opportunities})

def opportunity_detail(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    return render(request, 'participation/opportunity_detail.html', {'opportunity': opportunity})