from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count, Prefetch
from django.http import Http404, JsonResponse
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import CustomUserCreationForm, CustomAuthenticationForm, MessageForm, DoctorReplyForm
from .models import CustomUser, Message
from .decorators import doctor_required, patient_required, approved_user_required
from documents.models import Document
import logging

logger = logging.getLogger(__name__)

def register_view(request):
    try:
        if request.method == 'POST':
            form = CustomUserCreationForm(request.POST)
            if form.is_valid():
                try:
                    user = form.save()
                    email = form.cleaned_data.get('email')
                    role = form.cleaned_data.get('role')
                    
                    if role == 'doctor':
                        messages.info(request, f'Doctor account created for {email}! Your account is pending approval.')
                    else:
                        messages.success(request, f'Account created for {email}!')
                    
                    return redirect('accounts:login')
                except Exception as e:
                    logger.error(f"Error creating user: {e}")
                    messages.error(request, 'An error occurred while creating your account. Please try again.')
        else:
            form = CustomUserCreationForm()
    except Exception as e:
        logger.error(f"Error in register_view: {e}")
        form = CustomUserCreationForm()
        messages.error(request, 'An unexpected error occurred. Please try again.')
    
    return render(request, 'accounts/register.html', {'form': form})

ADMIN_CODE = '987654321@1'

def login_view(request):
    try:
        # If user is already authenticated, redirect to appropriate dashboard
        if request.user.is_authenticated:
            return _redirect_authenticated_user(request.user)
        
        if request.method == 'POST':
            global ADMIN_CODE
            admin_code = request.POST.get('admin_code', '').strip()
            email = request.POST.get('username', '').strip()
            password = request.POST.get('password', '').strip()
            new_admin_code = request.POST.get('new_admin_code', '').strip()

            # Change admin code from admin dashboard
            if new_admin_code and request.user.is_authenticated and getattr(request.user, 'role', None) == 'admin':
                ADMIN_CODE = new_admin_code
                messages.success(request, f'Admin code updated to: {ADMIN_CODE}')
                return redirect('accounts:admin_dashboard')

            # Admin login with only admin code
            if admin_code == ADMIN_CODE and not email and not password:
                try:
                    admin_user, created = CustomUser.objects.get_or_create(
                        email='admin@medsecurevault.com',
                        defaults={
                            'first_name': 'System',
                            'last_name': 'Administrator',
                            'role': 'admin',
                            'is_staff': True,
                            'is_superuser': True,
                            'is_approved_doctor': True,
                        }
                    )
                    if not admin_user.is_staff or not admin_user.is_superuser:
                        admin_user.role = 'admin'
                        admin_user.is_staff = True
                        admin_user.is_superuser = True
                        admin_user.is_approved_doctor = True
                        admin_user.save()
                    
                    admin_user.set_password('admin_secure_password')
                    admin_user.save()
                    login(request, admin_user)
                    messages.success(request, 'Welcome, Administrator!')
                    return redirect('accounts:admin_dashboard')
                except Exception as e:
                    logger.error(f"Error creating admin user: {e}")
                    messages.error(request, 'Error accessing admin account. Please try again.')
            
            # Regular login
            elif email and password:
                try:
                    user = authenticate(username=email, password=password)
                    if user is not None:
                        login(request, user)
                        
                        # Smart redirect after login
                        return _redirect_authenticated_user(user)
                    else:
                        messages.error(request, 'Invalid email or password.')
                except Exception as e:
                    logger.error(f"Error during authentication: {e}")
                    messages.error(request, 'An error occurred during login. Please try again.')
            elif admin_code and not email and not password:
                messages.error(request, 'Invalid admin code.')
            else:
                messages.error(request, 'Please enter your credentials.')
        
        form = CustomAuthenticationForm()
    except Exception as e:
        logger.error(f"Error in login_view: {e}")
        form = CustomAuthenticationForm()
        messages.error(request, 'An unexpected error occurred. Please try again.')
    
    return render(request, 'accounts/login.html', {'form': form})

def _redirect_authenticated_user(user):
    """Helper function to redirect authenticated users to appropriate dashboard"""
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
        else:  # patient
            return redirect('accounts:patient_dashboard')
    except Exception as e:
        logger.error(f"Error in _redirect_authenticated_user: {e}")
        return redirect('accounts:patient_dashboard')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html', {'user': request.user})

@login_required
def pending_approval_view(request):
    """Show pending approval page only for unapproved doctors"""
    try:
        # Only unapproved doctors should see this page
        if not hasattr(request.user, 'role') or request.user.role != 'doctor':
            return _redirect_authenticated_user(request.user)
        
        if getattr(request.user, 'is_approved_doctor', False):
            # Doctor is approved, redirect to dashboard
            messages.success(request, f'Welcome back, Dr. {request.user.get_full_name()}!')
            return redirect('accounts:doctor_dashboard')
        
        # Show pending approval page
        return render(request, 'accounts/pending_approval.html')
    except Exception as e:
        logger.error(f"Error in pending_approval_view: {e}")
        return redirect('accounts:login')

@login_required
def check_approval_status(request):
    """AJAX endpoint to check doctor approval status"""
    try:
        if request.user.role == 'doctor' and getattr(request.user, 'is_approved_doctor', False):
            return JsonResponse({'approved': True, 'redirect_url': '/accounts/doctor-dashboard/'})
        return JsonResponse({'approved': False})
    except Exception as e:
        logger.error(f"Error checking approval status: {e}")
        return JsonResponse({'approved': False, 'error': True})
    return render(request, 'accounts/pending_approval.html')

@patient_required
def patient_dashboard(request):
    try:
        # Get patient's documents
        documents = Document.objects.filter(user=request.user).order_by('-uploaded_at')[:5]
        total_documents = Document.objects.filter(user=request.user).count()
        
        # Get assigned doctor
        assigned_doctor = getattr(request.user, 'assigned_doctor', None)
        
        # Handle message sending
        message_form = None
        messages_sent = []
        
        if assigned_doctor:
            if request.method == 'POST' and 'send_message' in request.POST:
                message_form = MessageForm(request.POST)
                if message_form.is_valid():
                    msg = message_form.save(commit=False)
                msg.sender = request.user
                msg.receiver = assigned_doctor
                msg.save()
                messages.success(request, 'Message sent to your doctor!')
                return redirect('accounts:patient_dashboard')
            else:
                message_form = MessageForm()
            
            # Get recent messages sent to doctor
            messages_sent = Message.objects.filter(
                sender=request.user, 
                receiver=assigned_doctor
            ).order_by('-timestamp')[:5]
        
        context = {
            'documents': documents,
            'total_documents': total_documents,
            'assigned_doctor': assigned_doctor,
            'message_form': message_form,
            'messages_sent': messages_sent,
        }
        return render(request, 'accounts/patient_dashboard.html', context)
    except Exception as e:
        logger.error(f"Error in patient_dashboard: {e}")
        messages.error(request, 'Error loading dashboard.')
        return redirect('accounts:login')

@doctor_required
def doctor_dashboard(request):
    try:
        logger.info(f"doctor_dashboard: user={request.user.email}, role={getattr(request.user, 'role', None)}, is_approved_doctor={getattr(request.user, 'is_approved_doctor', None)}")
        # Get assigned patients with document count (optimized query)
        assigned_patients = CustomUser.objects.filter(
            role='patient', 
            assigned_doctor=request.user
        ).annotate(document_count=Count('documents')).order_by('-date_joined')[:6]
        
        # Get statistics
        assigned_patients_count = CustomUser.objects.filter(
            role='patient', 
            assigned_doctor=request.user
        ).count()
        
        total_patients = CustomUser.objects.filter(role='patient').count()
        
        # Get documents from assigned patients
        assigned_patient_ids = list(assigned_patients.values_list('id', flat=True))
        total_documents = Document.objects.filter(user__in=assigned_patient_ids).count() if assigned_patient_ids else 0
        
        # Get recent documents from assigned patients
        recent_documents = Document.objects.filter(
            user__in=assigned_patient_ids
        ).select_related('user').order_by('-uploaded_at')[:8] if assigned_patient_ids else []
        
        # Get latest messages from patients
        latest_messages = Message.objects.filter(
            receiver=request.user
        ).select_related('sender').order_by('-timestamp')[:10]
        
        # Count unread messages
        unread_messages_count = Message.objects.filter(
            receiver=request.user,
            is_read=False
        ).count()
        
        # Get recent patient registrations
        recent_patients = CustomUser.objects.filter(
            role='patient'
        ).order_by('-date_joined')[:5]
        
        # Handle message replies
        reply_forms = {}
        if request.method == 'POST' and request.POST.get('reply_to_message_id'):
            try:
                msg_id = request.POST.get('reply_to_message_id')
                original_msg = get_object_or_404(Message, id=msg_id, receiver=request.user)
                reply_form = DoctorReplyForm(request.POST)
                if reply_form.is_valid():
                    reply = reply_form.save(commit=False)
                    reply.sender = request.user
                    reply.receiver = original_msg.sender
                    reply.save()
                    # Mark original message as read
                    original_msg.is_read = True
                    original_msg.save()
                    messages.success(request, f'Reply sent to {original_msg.sender.get_full_name()}!')
                    return redirect('accounts:doctor_dashboard')
            except Exception as e:
                logger.error(f"Error sending reply: {e}")
                messages.error(request, 'Error sending reply.')
        
        # Create reply forms for all messages
        for msg in latest_messages:
            reply_forms[msg.id] = DoctorReplyForm()
        
        context = {
            'assigned_patients': assigned_patients,
            'total_patients': total_patients,
            'assigned_patients_count': assigned_patients_count,
            'total_documents': total_documents,
            'recent_documents': recent_documents,
            'recent_patients': recent_patients,
            'latest_messages': latest_messages,
            'unread_messages_count': unread_messages_count,
            'reply_forms': reply_forms,
        }
        return render(request, 'accounts/doctor_dashboard.html', context)
    except Exception as e:
        logger.error(f"Error in doctor_dashboard: {e}")
        error_message = f"Error loading dashboard: {e}"
        # Try to show partial dashboard if possible
        try:
            context['error_message'] = error_message
        except:
            context = {'error_message': error_message}
        return render(request, 'accounts/doctor_dashboard.html', context)

@user_passes_test(lambda u: u.is_authenticated and getattr(u, 'role', None) == 'admin')
def admin_dashboard(request):
    try:
        # Handle doctor approval
        if request.method == 'POST' and 'approve_doctor_id' in request.POST:
            try:
                doctor_id = request.POST.get('approve_doctor_id')
                doctor = get_object_or_404(
                    CustomUser, 
                    id=doctor_id, 
                    role='doctor', 
                    is_approved_doctor=False
                )
                doctor.is_approved_doctor = True
                doctor.save()
                messages.success(request, f"Dr. {doctor.get_full_name()} has been approved!")
                return redirect('accounts:admin_dashboard')
            except Exception as e:
                logger.error(f"Error approving doctor: {e}")
                messages.error(request, 'Error approving doctor.')

        # Get statistics
        pending_doctors = CustomUser.objects.filter(
            role='doctor', 
            is_approved_doctor=False
        ).order_by('-date_joined')
        
        total_users = CustomUser.objects.count()
        total_doctors = CustomUser.objects.filter(role='doctor').count()
        approved_doctors = CustomUser.objects.filter(role='doctor', is_approved_doctor=True).count()
        total_patients = CustomUser.objects.filter(role='patient').count()
        total_documents = Document.objects.count()

        # Patient search and pagination
        search_query = request.GET.get('search', '')
        patients = CustomUser.objects.filter(role='patient').select_related('assigned_doctor').order_by('-date_joined')
        
        if search_query:
            patients = patients.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        
        paginator = Paginator(patients, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        # Patient document view
        patient_detail = None
        patient_documents = None
        if request.GET.get('view_patient_id'):
            try:
                patient_detail = get_object_or_404(
                    CustomUser, 
                    id=request.GET['view_patient_id'], 
                    role='patient'
                )
                patient_documents = Document.objects.filter(
                    user=patient_detail
                ).order_by('-uploaded_at')
            except Exception as e:
                logger.error(f"Error fetching patient details: {e}")
                messages.error(request, 'Error loading patient details.')

        context = {
            'pending_doctors': pending_doctors,
            'total_users': total_users,
            'total_doctors': total_doctors,
            'approved_doctors': approved_doctors,
            'total_patients': total_patients,
            'total_documents': total_documents,
            'patients': page_obj,
            'search_query': search_query,
            'patient_detail': patient_detail,
            'patient_documents': patient_documents,
        }
        return render(request, 'accounts/admin_dashboard.html', context)
    except Exception as e:
        logger.error(f"Error in admin_dashboard: {e}")
        messages.error(request, 'Error loading admin dashboard.')
        return redirect('accounts:login')

@doctor_required
def patient_list_view(request):
    try:
        search_query = request.GET.get('search', '')
        filter_type = request.GET.get('filter', 'all')
        
        # Optimized query with select_related
        patients = CustomUser.objects.filter(role='patient').select_related('assigned_doctor').annotate(
            document_count=Count('documents')
        ).order_by('-date_joined')
        
        # Apply filters
        if search_query:
            patients = patients.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        
        if filter_type == 'assigned':
            patients = patients.filter(assigned_doctor=request.user)
        elif filter_type == 'unassigned':
            patients = patients.filter(assigned_doctor__isnull=True)
        
        # Pagination
        paginator = Paginator(patients, 12)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        # Statistics
        total_patients = CustomUser.objects.filter(role='patient').count()
        assigned_to_me = CustomUser.objects.filter(role='patient', assigned_doctor=request.user).count()
        unassigned_patients = CustomUser.objects.filter(role='patient', assigned_doctor__isnull=True).count()
        
        context = {
            'patients': page_obj,
            'search_query': search_query,
            'filter_type': filter_type,
            'total_patients': total_patients,
            'assigned_to_me': assigned_to_me,
            'unassigned_patients': unassigned_patients,
            'page_obj': page_obj,
        }
        return render(request, 'accounts/patient_list.html', context)
    except Exception as e:
        logger.error(f"Error in patient_list_view: {e}")
        messages.error(request, 'Error loading patient list.')
        return redirect('accounts:doctor_dashboard')

@doctor_required
def patient_detail_view(request, patient_id):
    try:
        patient = get_object_or_404(CustomUser, id=patient_id, role='patient')
        
        # Handle patient assignment
        if request.method == 'POST' and 'assign_patient' in request.POST:
            try:
                patient.assigned_doctor = request.user
                patient.save()
                messages.success(request, f'{patient.get_full_name()} has been assigned to you!')
                return redirect('accounts:patient_detail', patient_id=patient_id)
            except Exception as e:
                logger.error(f"Error assigning patient: {e}")
                messages.error(request, 'Error assigning patient.')
        
        # Handle patient unassignment
        if request.method == 'POST' and 'unassign_patient' in request.POST:
            try:
                patient.assigned_doctor = None
                patient.save()
                messages.success(request, f'{patient.get_full_name()} has been unassigned!')
                return redirect('accounts:patient_detail', patient_id=patient_id)
            except Exception as e:
                logger.error(f"Error unassigning patient: {e}")
                messages.error(request, 'Error unassigning patient.')
        
        # Get documents with filtering
        documents = Document.objects.filter(user=patient).order_by('-uploaded_at')
        doc_type = request.GET.get('doc_type')
        if doc_type:
            documents = documents.filter(doc_type=doc_type)
        
        context = {
            'patient': patient,
            'documents': documents,
            'total_documents': documents.count(),
            'doc_type_filter': doc_type,
            'document_types': Document.DOCUMENT_TYPES,
        }
        return render(request, 'accounts/patient_detail.html', context)
    except Exception as e:
        logger.error(f"Error in patient_detail_view: {e}")
        messages.error(request, 'Error loading patient details.')
        return redirect('accounts:patient_list')

@doctor_required
def patient_document_view(request, patient_id, document_id):
    try:
        patient = get_object_or_404(CustomUser, id=patient_id, role='patient')
        document = get_object_or_404(Document, id=document_id, user=patient)
        
        context = {
            'patient': patient,
            'document': document,
        }
        return render(request, 'accounts/patient_document.html', context)
    except Exception as e:
        logger.error(f"Error in patient_document_view: {e}")
        messages.error(request, 'Error loading document.')
        return redirect('accounts:patient_detail', patient_id=patient_id)

@require_POST
@doctor_required
def assign_patient_ajax(request, patient_id):
    """AJAX endpoint for patient assignment"""
    try:
        patient = get_object_or_404(CustomUser, id=patient_id, role='patient')
        action = request.POST.get('action')
        
        if action == 'assign':
            patient.assigned_doctor = request.user
            patient.save()
            return JsonResponse({
                'success': True, 
                'message': f'{patient.get_full_name()} assigned to you!',
                'assigned': True
            })
        elif action == 'unassign':
            patient.assigned_doctor = None
            patient.save()
            return JsonResponse({
                'success': True, 
                'message': f'{patient.get_full_name()} unassigned!',
                'assigned': False
            })
        else:
            return JsonResponse({'success': False, 'message': 'Invalid action'})
    except Exception as e:
        logger.error(f"Error in assign_patient_ajax: {e}")
        return JsonResponse({'success': False, 'message': 'Error processing request'})