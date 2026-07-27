from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from authentication.models import UserRole, Admin
from garages.models import Garage
from .models import Verification

@login_required
def toggle_verification(request, garage_id):
    if request.user.role != UserRole.ADMIN and not request.user.is_staff:
        return redirect('home')

    garage = get_object_or_404(Garage, id=garage_id)
    admin_profile, _ = Admin.objects.get_or_create(uid=request.user.uid or 'admin', defaults={'display_name': request.user.display_name})
    
    verification, created = Verification.objects.get_or_create(
        garage=garage,
        defaults={'verified': True, 'admin': admin_profile}
    )
    if not created:
        verification.verified = not verification.verified
        verification.admin = admin_profile
        verification.save()

    return redirect('admin_dashboard')
