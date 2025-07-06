from django.shortcuts import render, get_object_or_404, redirect
from .models import Opportunity, Tag
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .models import Opportunity, Tag, TagSubscription
from .forms import OpportunityForm, TagForm, TagSubscriptionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.shortcuts import render
from .models import Opportunity, Tag

def opportunity_list(request):
    selected_tag_names = request.GET.getlist('tag')  # This allows multiple ?tag=foo&tag=bar
    opportunities = Opportunity.objects.all()

    if selected_tag_names:
        for tag_name in selected_tag_names:
            opportunities = opportunities.filter(tags__name=tag_name)

    tags = Tag.objects.all()
    selected_tags = Tag.objects.filter(name__in=selected_tag_names)

    # Organize tags by category
    project_tags = tags.filter(category='Project')
    skill_tags = tags.filter(category='Skill')
    interest_tags = tags.filter(category='Interest')

    tag_groups = [
        {'name': 'Project', 'tags': project_tags},
        {'name': 'Skill', 'tags': skill_tags},
        {'name': 'Interest', 'tags': interest_tags},
    ]

    return render(request, 'participation/opportunity_list.html', {
        'opportunities': opportunities.distinct(),
        'tags': tags,
        'selected_tags': selected_tag_names,
        'tag_groups': tag_groups,
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

def subscribe(request):
    if request.method == 'POST':
        form = TagSubscriptionForm(request.POST)
        if form.is_valid():
            subscription = TagSubscription.objects.create(email=form.cleaned_data['email'])
            subscription.tags.set(form.cleaned_data['tags'])  # assign ManyToMany tags
            subscription.save()
            messages.success(request, "You've been subscribed!")
            return redirect('subscribe')
    else:
        form = TagSubscriptionForm()
    return render(request, 'participation/subscribe.html', {'form': form})

@login_required
def subscription_list(request):
    subscribers = TagSubscription.objects.all()
    return render(request, 'participation/subscription_list.html', {
        'subscribers': subscribers
    })