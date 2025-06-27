from django.shortcuts import render, get_object_or_404
from .models import Opportunity, Tag
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .models import Opportunity, Tag
from .forms import OpportunityForm, TagForm
from django.contrib.auth.decorators import login_required

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
    return render(request, 'participation/opportunity_detail.html', {
        'opportunity': opportunity,
    })

@login_required
def create_opportunity(request):
    if request.method == "POST":
        form = OpportunityForm(request.POST)
        if form.is_valid():
            opportunity = form.save()
            return redirect('opportunity_detail', pk=opportunity.pk)
    else:
        form = OpportunityForm()

    return render(request, 'participation/create_opportunity.html', {'form': form})

@login_required
def opportunity_edit(request, pk):
    opportunity = get_object_or_404(Opportunity, pk=pk)
    if request.method == "POST":
        form = OpportunityForm(request.POST, instance=opportunity)
        if form.is_valid():
            form.save()
            return redirect('opportunity_detail', pk=opportunity.pk)
    else:
        form = OpportunityForm(instance=opportunity)
    return render(request, 'participation/opportunity_form.html', {'form': form, 'edit': True})

@login_required
def opportunity_delete(request, pk):

    opportunity = get_object_or_404(Opportunity, pk=pk)
    if request.method == "POST":
        print("Post")
        opportunity.delete()
        return redirect('opportunity_list')
    return render(request, 'participation/opportunity_confirm_delete.html', {'opportunity': opportunity})

@login_required
def create_tag(request):
    tags = Tag.objects.all()
    if request.method == "POST":

        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()
            return redirect('participation/opportunity_list.html')
    else:
        form = TagForm()

    return render(request, 'participation/create_tag.html', {
        'form': form,
        'tags': tags,
        }
    )