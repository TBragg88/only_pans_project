# recipes/notifications.py
import logging
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from .models import Recipe

logger = logging.getLogger(__name__)


def send_comment_notification(comment, recipe_owner):
    """Send email notification when someone comments on a recipe"""
    if not recipe_owner.email:
        return
        
    subject = f"New comment on your recipe: {comment.recipe.title}"
    
    context = {
        'recipe_owner': recipe_owner,
        'comment': comment,
        'recipe': comment.recipe,
        'commenter': comment.user,
    }
    
    # Render email content
    html_message = render_to_string(
        'emails/comment_notification.html', context
    )
    plain_message = render_to_string(
        'emails/comment_notification.txt', context
    )
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipe_owner.email],
            fail_silently=True,
        )
    except Exception as e:
        # Log error properly
        logger.error(f"Failed to send comment notification: {e}")


def send_rating_notification(rating, recipe_owner):
    """Send email notification when someone rates a recipe"""
    if not recipe_owner.email:
        return
        
    subject = (
        f"New {rating.rating}-star rating on your recipe: "
        f"{rating.recipe.title}"
    )
    
    context = {
        'recipe_owner': recipe_owner,
        'rating': rating,
        'recipe': rating.recipe,
        'rater': rating.user,
    }
    
    # Render email content
    html_message = render_to_string('emails/rating_notification.html', context)
    plain_message = render_to_string('emails/rating_notification.txt', context)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipe_owner.email],
            fail_silently=True,
        )
    except Exception as e:
        # Log error properly
        logger.error(f"Failed to send rating notification: {e}")


def send_weekly_recipe_digest(user):
    """Send weekly digest of new recipes from followed users"""
    if not user.email:
        return
    
    # Get recipes from last week from followed users
    from django.utils import timezone
    from datetime import timedelta
    
    one_week_ago = timezone.now() - timedelta(days=7)
    
    # Get users this user follows (we'll need to create a follow system)
    # For now, just get recent popular recipes
    recent_recipes = Recipe.objects.filter(
        created_at__gte=one_week_ago
    ).order_by('-average_rating', '-created_at')[:5]
    
    if not recent_recipes.exists():
        return
    
    subject = "OnlyPans: This week's delicious recipes!"
    
    context = {
        'user': user,
        'recipes': recent_recipes,
        'week_start': one_week_ago.date(),
        'week_end': timezone.now().date(),
    }
    
    # Render email content
    html_message = render_to_string('emails/weekly_digest.html', context)
    plain_message = render_to_string('emails/weekly_digest.txt', context)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=True,
        )
    except Exception as e:
        # Log error in production
        logger.error(f"Failed to send weekly digest: {e}")


def send_new_follower_notification(followed_user, follower):
    """Send notification when someone follows a user"""
    if not followed_user.email:
        return
        
    subject = f"{follower.username} started following you on OnlyPans!"
    
    context = {
        'followed_user': followed_user,
        'follower': follower,
    }
    
    # Render email content
    html_message = render_to_string('emails/new_follower.html', context)
    plain_message = render_to_string('emails/new_follower.txt', context)
    
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            html_message=html_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[followed_user.email],
            fail_silently=True,
        )
    except Exception as e:
        # Log error in production
        logger.error(f"Failed to send follower notification: {e}")
