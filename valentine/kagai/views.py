from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.http import JsonResponse

from .models import UserProfile, LoveNote, Connection, Favorite


# ==================== Authentication Views ====================

def home(request):
    """Homepage view"""
    if request.user.is_authenticated:
        return redirect('kagai:dashboard')
    
    context = {
        'total_notes': LoveNote.objects.filter(status='sent').count(),
        'total_users': User.objects.count(),
    }
    return render(request, 'home.html', context)


def register(request):
    """User registration view"""
    if request.user.is_authenticated:
        return redirect('kagai:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password_confirm = request.POST.get('password_confirm', '')
        accept_terms = request.POST.get('accept_terms')
        
        errors = {}
        
        # Validation
        if not username or len(username) < 3:
            errors['username'] = 'Username must be at least 3 characters'
        if User.objects.filter(username=username).exists():
            errors['username'] = 'Username already taken'
        if not email or '@' not in email:
            errors['email'] = 'Enter a valid email'
        if User.objects.filter(email=email).exists():
            errors['email'] = 'Email already registered'
        if password != password_confirm:
            errors['password'] = 'Passwords do not match'
        if len(password) < 6:
            errors['password'] = 'Password must be at least 6 characters'
        if not accept_terms:
            errors['terms'] = 'You must accept the terms and conditions'
        
        if errors:
            return render(request, 'register.html', {'errors': errors})
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=username
        )
        
        # Create user profile
        UserProfile.objects.create(user=user)
        
        messages.success(request, 'Account created successfully! Please login.')
        return redirect('kagai:login')
    
    return render(request, 'register.html')


def login_view(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('kagai:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        remember = request.POST.get('remember')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if not remember:
                request.session.set_expiry(0)
            messages.success(request, f'Welcome back, {user.username}!')
            return redirect('kagai:dashboard')
        else:
            messages.error(request, 'Invalid username or password')
    
    return render(request, 'login.html')


def logout_view(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('kagai:home')


# ==================== Dashboard & Main Views ====================

@login_required(login_url='kagai:login')
def dashboard(request):
    """Main dashboard view"""
    user = request.user
    profile = user.profile
    
    # Get statistics
    sent_notes = LoveNote.objects.filter(sender=user, status='sent').count()
    received_notes = LoveNote.objects.filter(recipient=user, status='sent').count()
    connections = Connection.objects.filter(
        Q(user1=user, status='accepted') | Q(user2=user, status='accepted')
    ).count()
    pending_requests = Connection.objects.filter(user2=user, status='pending').count()
    
    # Recent notes
    recent_received = LoveNote.objects.filter(
        recipient=user, status='sent'
    ).order_by('-created_at')[:5]
    
    context = {
        'profile': profile,
        'sent_notes': sent_notes,
        'received_notes': received_notes,
        'connections': connections,
        'pending_requests': pending_requests,
        'recent_received': recent_received,
    }
    return render(request, 'dashboard.html', context)


# ==================== Profile Views ====================

@login_required(login_url='kagai:login')
def profile(request, username):
    """View user profile"""
    user_obj = get_object_or_404(User, username=username)
    profile = user_obj.profile
    
    # Get connection status if viewing other's profile
    connection = None
    is_friend = False
    is_pending = False
    
    if request.user != user_obj:
        connection = Connection.objects.filter(
            Q(user1=request.user, user2=user_obj) | Q(user1=user_obj, user2=request.user)
        ).first()
        
        if connection:
            is_friend = connection.status == 'accepted'
            is_pending = connection.status == 'pending'
    
    context = {
        'profile_user': user_obj,
        'profile': profile,
        'connection': connection,
        'is_friend': is_friend,
        'is_pending': is_pending,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='kagai:login')
def edit_profile(request):
    """Edit user profile"""
    profile = request.user.profile
    
    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')
        profile.location = request.POST.get('location', '')
        profile.interests = request.POST.get('interests', '')
        profile.website = request.POST.get('website', '')
        profile.phone = request.POST.get('phone', '')
        profile.gender = request.POST.get('gender', '')
        
        # Handle avatar upload
        if 'avatar' in request.FILES:
            profile.avatar = request.FILES['avatar']
        
        profile.save()
        
        # Update user info
        request.user.first_name = request.POST.get('first_name', '')
        request.user.last_name = request.POST.get('last_name', '')
        request.user.email = request.POST.get('email', '')
        request.user.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('kagai:profile', username=request.user.username)
    
    context = {
        'profile': profile,
    }
    return render(request, 'edit_profile.html', context)


# ==================== Love Notes Views ====================

@login_required(login_url='kagai:login')
def send_note(request, recipient_username):
    """Send a love note to a user"""
    recipient = get_object_or_404(User, username=recipient_username)
    
    if request.user == recipient:
        messages.error(request, 'You cannot send a note to yourself')
        return redirect('kagai:profile', username=recipient_username)
    
    if request.method == 'POST':
        title = request.POST.get('title', '')
        content = request.POST.get('content', '')
        is_anonymous = request.POST.get('is_anonymous') == 'on'
        
        if not content.strip():
            messages.error(request, 'Note content cannot be empty')
            return redirect('kagai:send_note', recipient_username=recipient_username)
        
        note = LoveNote.objects.create(
            sender=request.user,
            recipient=recipient,
            title=title,
            content=content,
            is_anonymous=is_anonymous,
            status='sent',
            sent_at=timezone.now()
        )
        
        messages.success(request, 'Love note sent successfully! 💌')
        return redirect('kagai:dashboard')
    
    context = {
        'recipient': recipient,
    }
    return render(request, 'send_note.html', context)


@login_required(login_url='kagai:login')
def view_note(request, note_id):
    """View a specific love note"""
    note = get_object_or_404(LoveNote, id=note_id)
    
    # Check if user has permission to view
    if request.user != note.recipient and request.user != note.sender:
        messages.error(request, 'You do not have permission to view this note')
        return redirect('kagai:dashboard')
    
    # Mark as opened if recipient is viewing
    if request.user == note.recipient and note.status == 'sent':
        note.status = 'opened'
        note.opened_at = timezone.now()
        note.save()
    
    sender_profile = note.sender.profile if not note.is_anonymous else None
    is_favorite = Favorite.objects.filter(user=request.user, note=note).exists()
    
    context = {
        'note': note,
        'sender_profile': sender_profile,
        'is_favorite': is_favorite,
    }
    return render(request, 'view_note.html', context)


@login_required(login_url='kagai:login')
def my_notes(request):
    """View all user's notes"""
    sent_notes = LoveNote.objects.filter(sender=request.user).order_by('-created_at')
    received_notes = LoveNote.objects.filter(recipient=request.user).order_by('-created_at')
    
    context = {
        'sent_notes': sent_notes,
        'received_notes': received_notes,
    }
    return render(request, 'my_notes.html', context)


@login_required(login_url='kagai:login')
@require_POST
def toggle_favorite(request, note_id):
    """Toggle favorite status of a note"""
    note = get_object_or_404(LoveNote, id=note_id)
    
    if request.user != note.recipient and request.user != note.sender:
        return JsonResponse({'error': 'Permission denied'}, status=403)
    
    favorite, created = Favorite.objects.get_or_create(user=request.user, note=note)
    
    if not created:
        favorite.delete()
        return JsonResponse({'favorited': False})
    
    return JsonResponse({'favorited': True})


# ==================== Connection Views ====================

@login_required(login_url='kagai:login')
def send_connection_request(request, recipient_username):
    """Send a connection request"""
    recipient = get_object_or_404(User, username=recipient_username)
    
    if request.user == recipient:
        messages.error(request, 'You cannot connect with yourself')
        return redirect('kagai:profile', username=recipient_username)
    
    # Check if connection already exists
    existing = Connection.objects.filter(
        Q(user1=request.user, user2=recipient) | Q(user1=recipient, user2=request.user)
    ).first()
    
    if existing:
        if existing.status == 'blocked':
            messages.error(request, 'You blocked this user or they blocked you')
        else:
            messages.info(request, 'Connection already requested')
        return redirect('kagai:profile', username=recipient_username)
    
    Connection.objects.create(user1=request.user, user2=recipient)
    messages.success(request, 'Connection request sent!')
    return redirect('kagai:profile', username=recipient_username)


@login_required(login_url='kagai:login')
def accept_connection(request, connection_id):
    """Accept a connection request"""
    connection = get_object_or_404(Connection, id=connection_id)
    
    if request.user != connection.user2:
        messages.error(request, 'You do not have permission')
        return redirect('dashboard')
    
    connection.status = 'accepted'
    connection.save()
    messages.success(request, f'You are now connected with {connection.user1.username}! 💕')
    return redirect('dashboard')


@login_required(login_url='kagai:login')
def reject_connection(request, connection_id):
    """Reject a connection request"""
    connection = get_object_or_404(Connection, id=connection_id)
    
    if request.user != connection.user2:
        messages.error(request, 'You do not have permission')
        return redirect('dashboard')
    
    connection.delete()
    messages.success(request, 'Connection request rejected')
    return redirect('kagai:dashboard')


@login_required(login_url='kagai:login')
def remove_connection(request, connection_id):
    """Remove a connection"""
    connection = get_object_or_404(Connection, id=connection_id)
    
    if request.user not in [connection.user1, connection.user2]:
        messages.error(request, 'You do not have permission')
        return redirect('kagai:dashboard')
    
    connection.delete()
    messages.success(request, 'Connection removed')
    return redirect('kagai:dashboard')


# ==================== Browse & Discover ====================

@login_required(login_url='kagai:login')
def browse_users(request):
    """Browse other users"""
    query = request.GET.get('q', '')
    gender = request.GET.get('gender', '')
    sort = request.GET.get('sort', '-created_at')
    
    users = User.objects.exclude(id=request.user.id).prefetch_related('profile')
    
    if query:
        users = users.filter(
            Q(username__icontains=query) | Q(first_name__icontains=query)
        )
    
    if gender and gender != 'all':
        users = users.filter(profile__gender=gender)
    
    users = users.order_by(sort)[:50]
    
    context = {
        'users': users,
        'query': query,
        'gender': gender,
        'sort': sort,
    }
    return render(request, 'browse_users.html', context)


def valentine_proposal(request):
    """Special Valentine's proposal page for Lucy"""
    context = {
        'lucy_image': True,
    }
    return render(request, 'valentine_proposal.html', context)
