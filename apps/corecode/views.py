from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import HttpResponseRedirect, redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, TemplateView, View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import (
    AcademicSessionForm,
    AcademicTermForm,
    CurrentSessionForm,
    SiteConfigForm,
    StudentClassForm,
    SubjectForm,
)
from .models import (
    AcademicSession,
    AcademicTerm,
    SiteConfig,
    StudentClass,
    Subject,
)


from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.students.models import Student
from apps.staffs.models import Staff
from apps.finance.models import Invoice

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_students'] = Student.objects.count()
        context['total_staff'] = Staff.objects.count()
        context['total_invoice'] = Invoice.objects.count()
        return context



# class IndexView(LoginRequiredMixin, TemplateView):
#     template_name = "index.html"

# from django.shortcuts import render
# from apps.students.models import Student
# from apps.staffs.models import Staff

# def total_count_view(request):
#     total_students = Student.objects.count()
#     total_staff = Staff.objects.count()
#     context = {
#         'total_students': total_students,
#         'total_staff': total_staff,
#     } 
#     return render(request, 'index.html', context)









from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from .forms import UserForm, ProfileForm


@login_required
def profile_view(request):
    return render(request, 'profile.html', {
        'user': request.user,
    })

@login_required
def edit_profile_view(request):
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    password_form = PasswordChangeForm(request.user)

    if request.method == 'POST':
        if 'old_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('edit_profile')
            else:
                messages.error(request, 'Please correct the error below / pls enter the stronge password.')
        else:
            user_form = UserForm(request.POST, instance=request.user)
            profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
            if user_form.is_valid() and profile_form.is_valid():
                user_form.save()
                profile_form.save()
                messages.success(request, 'Your profile was successfully updated!')
                return redirect('edit_profile')
            else:
                messages.error(request, 'Please correct the error below.')

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'password_form': password_form
    })




# #### new default profile picture added views.py functions:

# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import PasswordChangeForm
# from django.contrib.auth import update_session_auth_hash
# from django.shortcuts import render, redirect
# from django.templatetags.static import static
# from .forms import UserForm, ProfileForm

# @login_required
# def profile_view(request):
#     profile_picture_url = request.user.profile.profile_picture.url if request.user.profile.profile_picture else static('dist/img/avatar.png')
#     return render(request, 'profile.html', {
#         'user': request.user,
#         'profile_picture_url': profile_picture_url,
#     })

# @login_required
# def edit_profile_view(request):
#     if request.method == 'POST':
#         if 'old_password' in request.POST:
#             password_form = PasswordChangeForm(request.user, request.POST)
#             if password_form.is_valid():
#                 user = password_form.save()
#                 update_session_auth_hash(request, user)
#                 messages.success(request, 'Your password was successfully updated!')
#                 return redirect('edit_profile')
#             else:
#                 messages.error(request, 'Please correct the error below.')
#         else:
#             user_form = UserForm(request.POST, instance=request.user)
#             profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
#             if user_form.is_valid() and profile_form.is_valid():
#                 user_form.save()
#                 profile_form.save()
#                 messages.success(request, 'Your profile was successfully updated!')
#                 return redirect('edit_profile')
#             else:
#                 messages.error(request, 'Please correct the error below.')
#     else:
#         user_form = UserForm(instance=request.user)
#         profile_form = ProfileForm(instance=request.user.profile)
#         password_form = PasswordChangeForm(request.user)

#     profile_picture_url = request.user.profile.profile_picture.url if request.user.profile.profile_picture else static('dist/img/avatar.png')
    
#     return render(request, 'edit_profile.html', {
#         'user_form': user_form,
#         'profile_form': profile_form,
#         'password_form': password_form,
#         'profile_picture_url': profile_picture_url,
#     })
 




##### old sign-up view function:


from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
from .models import UserProfile
from django.contrib import messages

class SignupView(View):
    def get(self, request):
        return render(request, 'corecode/signup.html')
    

    def post(self, request):
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('signup')
        
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Create UserProfile instance and link to the User
        UserProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            email=email
            # Add other fields as needed
        )

        messages.success(request, 'Signup successful! Please login.')
        return redirect('login')



class SiteConfigView(LoginRequiredMixin, View):
    """Site Config View"""

    form_class = SiteConfigForm
    template_name = "corecode/siteconfig.html"

    def get(self, request, *args, **kwargs):
        formset = self.form_class(queryset=SiteConfig.objects.all())
        context = {"formset": formset}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        formset = self.form_class(request.POST)
        if formset.is_valid():
            formset.save()
            messages.success(request, "Configurations successfully updated")
        context = {"formset": formset, "title": "Configuration"}
        return render(request, self.template_name, context)


class SessionListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AcademicSession
    template_name = "corecode/session_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicSessionForm()
        return context


class SessionCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("sessions")
    success_message = "New session successfully added"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Add new session"
        return context


class SessionUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicSession
    form_class = AcademicSessionForm
    success_url = reverse_lazy("sessions")
    success_message = "Session successfully updated."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        obj = self.object
        if obj.current == False:
            terms = (
                AcademicSession.objects.filter(current=True)
                .exclude(name=obj.name)
                .exists()
            )
            if not terms:
                messages.warning(self.request, "You must set a session to current.")
                return redirect("session-list")
        return super().form_valid(form)


class SessionDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicSession
    success_url = reverse_lazy("sessions")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The session {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current == True:
            messages.warning(request, "Cannot delete session as it is set to current")
            return redirect("sessions")
        messages.success(self.request, self.success_message.format(obj.name))
        return super(SessionDeleteView, self).delete(request, *args, **kwargs)


class TermListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = AcademicTerm
    template_name = "corecode/term_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = AcademicTermForm()
        return context


class TermCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("terms")
    success_message = "New term successfully added"


class TermUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = AcademicTerm
    form_class = AcademicTermForm
    success_url = reverse_lazy("terms")
    success_message = "Term successfully updated."
    template_name = "corecode/mgt_form.html"

    def form_valid(self, form):
        obj = self.object
        if obj.current == False:
            terms = (
                AcademicTerm.objects.filter(current=True)
                .exclude(name=obj.name)
                .exists()
            )
            if not terms:
                messages.warning(self.request, "You must set a term to current.")
                return redirect("term")
        return super().form_valid(form)


class TermDeleteView(LoginRequiredMixin, DeleteView):
    model = AcademicTerm
    success_url = reverse_lazy("terms")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The term {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.current == True:
            messages.warning(request, "Cannot delete term as it is set to current")
            return redirect("terms")
        messages.success(self.request, self.success_message.format(obj.name))
        return super(TermDeleteView, self).delete(request, *args, **kwargs)


class ClassListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = StudentClass
    template_name = "corecode/class_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = StudentClassForm()
        return context


class ClassCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = StudentClass
    form_class = StudentClassForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("classes")
    success_message = "New class successfully added"


class ClassUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = StudentClass
    fields = ["name"]
    success_url = reverse_lazy("classes")
    success_message = "class successfully updated."
    template_name = "corecode/mgt_form.html"


class ClassDeleteView(LoginRequiredMixin, DeleteView):
    model = StudentClass
    success_url = reverse_lazy("classes")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The class {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        print(obj.name)
        messages.success(self.request, self.success_message.format(obj.name))
        return super(ClassDeleteView, self).delete(request, *args, **kwargs)


class SubjectListView(LoginRequiredMixin, SuccessMessageMixin, ListView):
    model = Subject
    template_name = "corecode/subject_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SubjectForm()
        return context


class SubjectCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Subject
    form_class = SubjectForm
    template_name = "corecode/mgt_form.html"
    success_url = reverse_lazy("subjects")
    success_message = "New subject successfully added"


class SubjectUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Subject
    fields = ["name"]
    success_url = reverse_lazy("subjects")
    success_message = "Subject successfully updated."
    template_name = "corecode/mgt_form.html"


class SubjectDeleteView(LoginRequiredMixin, DeleteView):
    model = Subject
    success_url = reverse_lazy("subjects")
    template_name = "corecode/core_confirm_delete.html"
    success_message = "The subject {} has been deleted with all its attached content"

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        messages.success(self.request, self.success_message.format(obj.name))
        return super(SubjectDeleteView, self).delete(request, *args, **kwargs)


class CurrentSessionAndTermView(LoginRequiredMixin, View):
    """Current SEssion and Term"""

    form_class = CurrentSessionForm
    template_name = "corecode/current_session.html"

    def get(self, request, *args, **kwargs):
        form = self.form_class(
            initial={
                "current_session": AcademicSession.objects.get(current=True),
                "current_term": AcademicTerm.objects.get(current=True),
            }
        )
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_Class(request.POST)
        if form.is_valid():
            session = form.cleaned_data["current_session"]
            term = form.cleaned_data["current_term"]
            AcademicSession.objects.filter(name=session).update(current=True)
            AcademicSession.objects.exclude(name=session).update(current=False)
            AcademicTerm.objects.filter(name=term).update(current=True)

        return render(request, self.template_name, {"form": form})

#################################### signup


# from django.shortcuts import render,HttpResponse,redirect
# from django.contrib.auth.models import User
# from django.contrib.auth import authenticate,login,logout
# from django.contrib.auth.decorators import login_required
# # Create your views here.
# @login_required(login_url='login')
# def HomePage(request):
#     # return render (request,'home.html')
#     return render (request,'index.html')

# def SignupPage(request):
#     if request.method=='POST':
#         uname=request.POST.get('username')
#         email=request.POST.get('email')
#         pass1=request.POST.get('password1')
#         pass2=request.POST.get('password2')

#         if pass1!=pass2:
#             return HttpResponse("Your password and confrom password are not Same!!")
#         else:

#             my_user=User.objects.create_user(uname,email,pass1)
#             my_user.save()
#             return redirect('login')
        



#     return render (request,'signup.html')

# def LoginPage(request):
#     if request.method=='POST':
#         username=request.POST.get('username')
#         pass1=request.POST.get('pass')
#         user=authenticate(request,username=username,password=pass1)
#         if user is not None:
#             login(request,user)
#             return redirect('home')
#         else:
#             return HttpResponse ("Username or Password is incorrect!!!")

#     return render (request,'login.html')

# def LogoutPage(request):
#     logout(request)
#     return redirect('login')