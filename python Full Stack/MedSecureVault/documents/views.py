from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, Http404
from django.db.models import Q
from django.core.paginator import Paginator
from .models import Document
from .forms import DocumentUploadForm, DocumentSearchForm
from accounts.decorators import patient_required, approved_user_required
import os
import logging

logger = logging.getLogger(__name__)

@approved_user_required
def dashboard_view(request):
    try:
        # Redirect based on user role
        if hasattr(request.user, 'role'):
            if request.user.role == 'doctor':
                return redirect('accounts:doctor_dashboard')
            elif request.user.role == 'admin':
                return redirect('accounts:admin_dashboard')
            else:
                return redirect('accounts:patient_dashboard')
        else:
            return redirect('accounts:patient_dashboard')
    except Exception as e:
        logger.error(f"Error in dashboard_view: {e}")
        messages.error(request, 'Error loading dashboard. Please try again.')
        return redirect('accounts:login')

@patient_required
def upload_document_view(request):
    try:
        if request.method == 'POST':
            form = DocumentUploadForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    document = form.save(commit=False)
                    document.user = request.user
                    document.save()
                    messages.success(request, 'Document uploaded successfully!')
                    return redirect('documents:list')
                except Exception as e:
                    logger.error(f"Error saving document: {e}")
                    messages.error(request, 'Error uploading document. Please try again.')
            else:
                # Form validation errors will be displayed in template
                pass
        else:
            form = DocumentUploadForm()
    except Exception as e:
        logger.error(f"Error in upload_document_view: {e}")
        form = DocumentUploadForm()
        messages.error(request, 'Error loading upload form. Please try again.')
    
    return render(request, 'documents/upload.html', {'form': form})

@patient_required
def document_list_view(request):
    try:
        documents = Document.objects.filter(user=request.user)
        search_form = DocumentSearchForm(request.GET)
        
        if search_form.is_valid():
            search_query = search_form.cleaned_data.get('search')
            doc_type = search_form.cleaned_data.get('doc_type')
            date_from = search_form.cleaned_data.get('date_from')
            date_to = search_form.cleaned_data.get('date_to')
            
            if search_query:
                documents = documents.filter(
                    Q(title__icontains=search_query) |
                    Q(tags__icontains=search_query) |
                    Q(description__icontains=search_query)
                )
            
            if doc_type:
                documents = documents.filter(doc_type=doc_type)
            
            if date_from:
                documents = documents.filter(uploaded_at__date__gte=date_from)
            
            if date_to:
                documents = documents.filter(uploaded_at__date__lte=date_to)
        
        paginator = Paginator(documents, 12)  # Show 12 documents per page
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context = {
            'documents': page_obj,
            'search_form': search_form,
            'page_obj': page_obj,
        }
        return render(request, 'documents/list.html', context)
    except Exception as e:
        logger.error(f"Error in document_list_view: {e}")
        messages.error(request, 'Error loading documents. Please try again.')
        return redirect('accounts:patient_dashboard')

@approved_user_required
def document_detail_view(request, pk):
    try:
        # Patients can only see their own documents
        # Doctors and admins can see any document (for patient care)
        if hasattr(request.user, 'role') and request.user.role == 'patient':
            document = get_object_or_404(Document, pk=pk, user=request.user)
        else:  # doctor or admin
            document = get_object_or_404(Document, pk=pk)
        
        return render(request, 'documents/detail.html', {'document': document})
    except Http404:
        messages.error(request, 'Document not found.')
        if hasattr(request.user, 'role') and request.user.role == 'patient':
            return redirect('documents:list')
        else:
            return redirect('accounts:doctor_dashboard')
    except Exception as e:
        logger.error(f"Error in document_detail_view: {e}")
        messages.error(request, 'Error loading document. Please try again.')
        if hasattr(request.user, 'role') and request.user.role == 'patient':
            return redirect('documents:list')
        else:
            return redirect('accounts:doctor_dashboard')

@approved_user_required
def document_download_view(request, pk):
    try:
        # Patients can only download their own documents
        # Doctors and admins can download any document (for patient care)
        if hasattr(request.user, 'role') and request.user.role == 'patient':
            document = get_object_or_404(Document, pk=pk, user=request.user)
        else:  # doctor or admin
            document = get_object_or_404(Document, pk=pk)
        
        if document.file and os.path.exists(document.file.path):
            try:
                with open(document.file.path, 'rb') as fh:
                    response = HttpResponse(fh.read(), content_type="application/octet-stream")
                    response['Content-Disposition'] = f'attachment; filename="{os.path.basename(document.file.name)}"'
                    return response
            except Exception as e:
                logger.error(f"Error reading file: {e}")
                messages.error(request, 'Error downloading file. The file may be corrupted.')
                raise Http404("File cannot be read")
        else:
            messages.error(request, 'File not found on server.')
            raise Http404("File not found")
    except Http404:
        if hasattr(request.user, 'role') and request.user.role == 'patient':
            return redirect('documents:list')
        else:
            return redirect('accounts:doctor_dashboard')
    except Exception as e:
        logger.error(f"Error in document_download_view: {e}")
        messages.error(request, 'Error downloading document. Please try again.')
        if hasattr(request.user, 'role') and request.user.role == 'patient':
            return redirect('documents:list')
        else:
            return redirect('accounts:doctor_dashboard')

@patient_required
def document_delete_view(request, pk):
    try:
        document = get_object_or_404(Document, pk=pk, user=request.user)
        
        if request.method == 'POST':
            try:
                # Try to delete the file from filesystem, but continue even if file is missing
                if document.file:
                    try:
                        if os.path.isfile(document.file.path):
                            os.remove(document.file.path)
                    except (OSError, ValueError, AttributeError):
                        # File doesn't exist, path is invalid, or file field is None
                        # Log the issue but continue with database deletion
                        logger.warning(f"Could not delete file for document {document.id}")
                
                # Always delete the database record
                document_title = document.title
                document.delete()
                messages.success(request, f'Document "{document_title}" deleted successfully!')
                return redirect('documents:list')
            except Exception as e:
                logger.error(f"Error deleting document: {e}")
                messages.error(request, 'Error deleting document. Please try again.')
                return redirect('documents:detail', pk=pk)
        
        return render(request, 'documents/delete_confirm.html', {'document': document})
    except Http404:
        messages.error(request, 'Document not found.')
        return redirect('documents:list')
    except Exception as e:
        logger.error(f"Error in document_delete_view: {e}")
        messages.error(request, 'Error accessing document. Please try again.')
        return redirect('documents:list')