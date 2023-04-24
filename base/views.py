from django.shortcuts import render , redirect
from base.models import Task

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView ,FormView

from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



#Custom login page view

class CustomLoginView(LoginView):
    fields='__all__'
    template_name = "login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')





class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request , user)
        return super(RegisterPage,self).form_valid(form)

    def get(self , *args , **kuargs):
        if self.request.user.is_authenticated:
            return redirect ('tasks')
        return super(RegisterPage , self).get(*args , **kuargs)





class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name='tasks'
    
    template_name = "task_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user = self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        
        search_input= self.request.GET.get('search-area') or ''
        
        if search_input:
            context['tasks'] = context ['tasks'].filter(title__icontains = search_input) #title__icontains or title__startswith
            
        context['search-input'] = search_input
        
        return context




class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name='task'

    template_name = "task_detail.html"




class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title' , 'description' , 'complete']
    success_url = reverse_lazy('tasks')

    template_name = "task_form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate , self).form_valid(form)




class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title' , 'description' , 'complete']
    success_url = reverse_lazy('tasks')

    template_name = "task_form.html"




class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    fields ='__all__'
    context_object_name='task'
    success_url = reverse_lazy('tasks')

    template_name = "task_confirm_delete.html"
