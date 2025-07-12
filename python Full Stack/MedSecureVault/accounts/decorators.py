from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def role_required(allowed_roles):
    """
    Decorator to restrict access based on user roles.
    Usage: @role_required(['doctor']) or @role_required(['patient', 'doctor'])
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            try:
                if not request.user.is_authenticated:
                    messages.info(request, "Please log in to access this page.")
                    return redirect('accounts:login')
                
                if not hasattr(request.user, 'role') or request.user.role not in allowed_roles:
                    messages.error(request, "You don't have permission to access this page.")
                    # Redirect based on user role
                    if hasattr(request.user, 'role'):
                        if request.user.role == 'doctor':
                            return redirect('accounts:doctor_dashboard')
                        elif request.user.role == 'admin':
                            return redirect('accounts:admin_dashboard')
                        else:
                            return redirect('accounts:patient_dashboard')
                    return redirect('accounts:login')
                
                # Check if doctor is approved
                if (hasattr(request.user, 'role') and 
                    request.user.role == 'doctor' and 
                    hasattr(request.user, 'is_approved_doctor') and 
                    not request.user.is_approved_doctor):
                    messages.warning(request, "Your doctor account is pending approval.")
                    return redirect('accounts:pending_approval')
                
                return view_func(request, *args, **kwargs)
            except Exception as e:
                logger.error(f"Error in role_required decorator: {e}")
                messages.error(request, "An error occurred. Please try again.")
                return redirect('accounts:login')
        return _wrapped_view
    return decorator

def doctor_required(view_func):
    """
    Decorator to restrict access to approved doctors only.
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        try:
            logger.info(f"doctor_required: user={request.user.email}, role={getattr(request.user, 'role', None)}, is_approved_doctor={getattr(request.user, 'is_approved_doctor', None)}")
            if not request.user.is_authenticated:
                return redirect('accounts:login')
            # Check if user is a doctor
            if not hasattr(request.user, 'role') or request.user.role != 'doctor':
                messages.error(request, "Access denied. Doctor privileges required.")
                return _redirect_by_role(request.user)
            # Check if doctor is approved
            if not getattr(request.user, 'is_approved_doctor', False):
                logger.info(f"doctor_required: redirecting to pending_approval for user={request.user.email}")
                if request.resolver_match and request.resolver_match.url_name == 'pending_approval':
                    return view_func(request, *args, **kwargs)
                messages.warning(request, "Your doctor account is pending approval.")
                return redirect('accounts:pending_approval')
            logger.info(f"doctor_required: access granted to doctor_dashboard for user={request.user.email}")
            return view_func(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in doctor_required decorator: {e}")
            return _redirect_by_role(request.user) if request.user.is_authenticated else redirect('accounts:login')
    return _wrapped_view

def _redirect_by_role(user):
    """Helper function to redirect users based on their role"""
    try:
        if not hasattr(user, 'role'):
            return redirect('accounts:patient_dashboard')
        
        if user.role == 'admin':
            return redirect('accounts:admin_dashboard')
        elif user.role == 'doctor':
            if getattr(user, 'is_approved_doctor', False):
                return redirect('accounts:doctor_dashboard')
            else:
                return redirect('accounts:pending_approval')
        else:
            return redirect('accounts:patient_dashboard')
    except:
        return redirect('accounts:login')
def patient_required(view_func):
    """
    Decorator to restrict access to patients only.
    """
    return role_required(['patient'])(view_func)

def admin_required(view_func):
    """
    Decorator to restrict access to administrators only.
    """
    return role_required(['admin'])(view_func)

def approved_user_required(view_func):
    """
    Decorator to ensure user is approved (for doctors) or is patient/admin
    """
    @wraps(view_func)
    @login_required
    def _wrapped_view(request, *args, **kwargs):
        try:
            if not request.user.is_authenticated:
                messages.info(request, "Please log in to access this page.")
                return redirect('accounts:login')
            
            # Check if user has is_approved property/method
            is_approved = False
            try:
                if hasattr(request.user, 'is_approved'):
                    is_approved = request.user.is_approved
                elif hasattr(request.user, 'role'):
                    if request.user.role == 'patient':
                        is_approved = True
                    elif request.user.role == 'doctor':
                        is_approved = getattr(request.user, 'is_approved_doctor', False)
                    elif request.user.role == 'admin':
                        is_approved = True
            except Exception as e:
                logger.error(f"Error checking user approval status: {e}")
                is_approved = False
            
            if not is_approved:
                if hasattr(request.user, 'role') and request.user.role == 'doctor':
                    messages.warning(request, "Your doctor account is pending approval.")
                    return redirect('accounts:pending_approval')
                else:
                    messages.error(request, "Your account is not approved.")
                    return redirect('accounts:login')
            
            return view_func(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Error in approved_user_required decorator: {e}")
            messages.error(request, "An error occurred. Please try again.")
            return redirect('accounts:login')
    return _wrapped_view