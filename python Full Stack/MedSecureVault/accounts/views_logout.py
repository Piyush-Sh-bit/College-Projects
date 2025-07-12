from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)

class CustomLogoutView(View):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        try:
            if request.user.is_authenticated:
                user_name = request.user.get_full_name() or request.user.email
                logout(request)
                messages.success(request, f'You have been successfully logged out. Goodbye, {user_name}!')
            else:
                logout(request)  # Ensure session is cleared even if user not authenticated
        except Exception as e:
            logger.error(f"Error during logout (GET): {e}")
            # Still try to logout and redirect even if there's an error
            try:
                logout(request)
            except:
                pass
            messages.info(request, 'You have been logged out.')
        
        return redirect('accounts:login')

    def post(self, request):
        try:
            if request.user.is_authenticated:
                user_name = request.user.get_full_name() or request.user.email
                logout(request)
                messages.success(request, f'You have been successfully logged out. Goodbye, {user_name}!')
            else:
                logout(request)  # Ensure session is cleared even if user not authenticated
        except Exception as e:
            logger.error(f"Error during logout (POST): {e}")
            # Still try to logout and redirect even if there's an error
            try:
                logout(request)
            except:
                pass
            messages.info(request, 'You have been logged out.')
        
        return redirect('accounts:login')