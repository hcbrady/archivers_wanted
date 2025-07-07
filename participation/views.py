from django.shortcuts import render, get_object_or_404, redirect
from .models import Opportunity, Tag, TagSubscription
from .forms import OpportunityForm, TagForm, TagSubscriptionForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

def opportunity_list(request):
    selected_tag_names = request.GET.getlist('tag')
    opportunities = Opportunity.objects.all()

    if selected_tag_names:
        for tag_name in selected_tag_names:
            opportunities = opportunities.filter(tags__name=tag_name)

    opportunities = opportunities.distinct()

    paginator = Paginator(opportunities, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    tags = Tag.objects.all()

    project_tags = tags.filter(category='project')
    skill_tags = tags.filter(category='skill')
    interest_tags = tags.filter(category='interest')

    tag_groups = [
        {'name': 'Project', 'tags': project_tags},
        {'name': 'Skill', 'tags': skill_tags},
        {'name': 'Interest', 'tags': interest_tags},
    ]

    return render(request, 'participation/opportunity_list.html', {
        'page_obj': page_obj,
        'opportunities': page_obj.object_list,
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

@login_required
def tag_edit(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == "POST":
        form = TagForm(request.POST, instance=tag)
        if form.is_valid():
            form.save()
            return redirect('create_tag')
    else:
        form = TagForm(instance=tag)
    return render(request, 'participation/tag_form.html', {'form': form, 'edit': True})


@login_required
def tag_delete(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.method == "POST":
        tag.delete()
        return redirect('create_tag')
    return render(request, 'participation/tag_confirm_delete.html', {'tag': tag})

def subscribe(request):
    if request.method == 'POST':
        form = TagSubscriptionForm(request.POST)
        if form.is_valid():
            subscription = TagSubscription.objects.create(email=form.cleaned_data['email'])
            subscription.tags.set(form.cleaned_data['tags'])
            subscription.save()
            messages.success(request, "You've been subscribed!")
            return redirect('subscribe')
    else:
        form = TagSubscriptionForm()
    return render(request, 'participation/subscribe.html', {'form': form})

def about(request):
    return render(request, 'participation/about.html')

@login_required
def subscription_list(request):
    subscribers = TagSubscription.objects.all()
    return render(request, 'participation/subscription_list.html', {
        'subscribers': subscribers
    })