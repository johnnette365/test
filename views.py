from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.timezone import now
from Megazine.models import Magazine, Comment, Subscriber
from Megazine.forms import CommentForm, SubscriptionForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages


# Create your views here.



def home(request):
    return render(request, "home.html")


# def article_detail(request, slug):
#     article = get_object_or_404(Article, slug=slug, is_published=True)

#     if request.method == "POST" and request.user.is_authenticated:
#         comment_content = request.POST.get("comment")
#         if comment_content:
#             Comment.objects.create(
#                 article=article,
#                 user=request.user,
#                 content=comment_content,
#                 created_at=now(),
#             )
#         return redirect("article_detail", slug=article.slug)

#     return render(request, "article.html", {"article": article})





# List all published magazines
def magazine_list(request):
    magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')
    return render(request, 'magazine_list.html', {'magazines': magazines})


# def magazine_detail(request, slug):
#     magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
#     latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]  # Get latest 5 magazines
#     comments = magazine.comments.all()

#     if request.method == "POST":
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             comment = comment_form.save(commit=False)
#             comment.magazine = magazine
#             comment.user = request.user  # Ensure user is logged in
#             comment.created_at = timezone.now()
#             comment.save()
#             return redirect('magazine_detail', slug=magazine.slug)  # Redirect to prevent form resubmission
#     else:
#         comment_form = CommentForm()

#     return render(request, 'magazine.html', {
#         'magazine': magazine,
#         'latest_magazines': latest_magazines,
#         'comments': comments,
#         'comment_form': comment_form
#     })







def magazine_detail(request, slug):
    magazine = get_object_or_404(Magazine, slug=slug, is_published=True)
    latest_magazines = Magazine.objects.filter(is_published=True).order_by('-published_at')[:5]
    comments = magazine.comments.all()

    comment_form = CommentForm()
    subscription_form = SubscriptionForm()

    if request.method == "POST":
        if 'comment_submit' in request.POST:  # Handling Comment Form
            comment_form = CommentForm(request.POST)
            
            if comment_form.is_valid():
                if request.user.is_authenticated:
                    comment = comment_form.save(commit=False)
                    comment.magazine = magazine
                    comment.user = request.user
                    comment.created_at = timezone.now()
                    comment.save()
                    
                    messages.success(request, "Your comment was posted successfully!")
                    return redirect('magazine_detail', slug=magazine.slug)
                else:
                    messages.error(request, "You must be logged in to comment!")
                    return redirect('login')

        elif 'subscribe_submit' in request.POST:  # Handling Subscription Form
            subscription_form = SubscriptionForm(request.POST)

            if subscription_form.is_valid():
                email = subscription_form.cleaned_data['email']
                
                # Check if email is already subscribed
                if not Subscriber.objects.filter(email=email).exists():
                    subscriber = subscription_form.save(commit=False)
                    subscriber.subscribed_at = timezone.now()
                    subscriber.save()
                    
                    messages.success(request, "You have successfully subscribed!")
                else:
                    messages.warning(request, "You are already subscribed!")

                return redirect('magazine_detail', slug=magazine.slug)

    return render(request, 'magazine.html', {
        'magazine': magazine,
        'latest_magazines': latest_magazines,
        'comments': comments,
        'comment_form': comment_form,
        'subscription_form': subscription_form
    })