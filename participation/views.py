from django.shortcuts import render, get_object_or_404, redirect
from .models import Opportunity, Tag
from django.conf import settings
from django.shortcuts import render, redirect
from django.http import HttpResponseForbidden
from .models import Opportunity, Tag, TagSubscription
from .forms import OpportunityForm, TagForm, TagSubscriptionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def opportunity_list(request):
    selected_tag = request.GET.get('tag')
    opportunities = Opportunity.objects.all()

    if selected_tag:
        opportunities = opportunities.filter(tags__name=selected_tag)

    tag_groups = [
        {"name": "Project", "tags": Tag.objects.filter(category="project")},
        {"name": "Skill", "tags": Tag.objects.filter(category="skill")},
        {"name": "Interest", "tags": Tag.objects.filter(category="interest")},
    ]

    context = {
        "opportunities": opportunities,
        "selected_tag": selected_tag,
        "tag_groups": tag_groups,
    }
    return render(request, "participation/opportunity_list.html", context)

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