from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    """Extended user profile with additional information"""
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, null=True, max_length=500)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True)
    interests = models.CharField(max_length=500, blank=True, help_text="Comma-separated interests")
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username}'s Profile"


class LoveNote(models.Model):
    """Love notes or messages between users"""
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('opened', 'Opened'),
        ('liked', 'Liked'),
    ]
    
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notes')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_notes')
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField(max_length=2000)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_anonymous = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(blank=True, null=True)
    opened_at = models.DateTimeField(blank=True, null=True)
    emoji_reaction = models.CharField(max_length=10, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        unique_together = []
    
    def __str__(self):
        return f"Note from {self.sender.username} to {self.recipient.username}"


class Connection(models.Model):
    """Connect with other users (relationships/friendships)"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('blocked', 'Blocked'),
    ]
    
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connections_initiated')
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='connections_received')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('user1', 'user2')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user1.username} <> {self.user2.username} ({self.status})"


class Favorite(models.Model):
    """Save favorite notes or profiles"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    note = models.ForeignKey(LoveNote, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'note')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} favorited a note"
