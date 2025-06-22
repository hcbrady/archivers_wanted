from django.shortcuts import render, get_object_or_404
from .models import Opportunity, Tag
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .models import Opportunity
from .forms import OpportunityForm

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

def create_opportunity(request):
    key = request.GET.get('key')
    if key != settings.ADMIN_ACCESS_KEY:
        return HttpResponseForbidden("You don't have permission to view this page.")

    if request.method == "POST":
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save()
            return redirect('opportunity_detail', pk=opportunity.pk)
    else:
        form = OpportunityForm()

    return render(request, 'participation/create_opportunity.html', {'form': form})