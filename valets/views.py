from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from authentication.models import UserRole
from valet_assignments.models import ValetAssignment

@login_required
def valet_dashboard(request):
    if request.user.role != UserRole.VALET and not request.user.is_staff:
        return redirect('home')

    assignments = ValetAssignment.objects.all().select_related('booking', 'pickup_valet', 'return_valet')
    return render(request, 'valet_dashboard.html', {'assignments': assignments})
