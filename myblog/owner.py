from django.views.generic import ListView,CreateView,DetailView,DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

class OwnerListView(ListView):
    """
    Sub-class the ListView to pass the request to the form.
    """

class OwnerDetailView(DetailView):
    """
    Sub-class the ListView to pass the request to the form.
    """

class OwnerCreateView(LoginRequiredMixin,CreateView):

    def form_valid(self,form):
        object=form.save(commit=False)
        object.owner=self.request.user
        object.save()
        return super(OwnerCreateView, self).form_valid(form)

class OwnerDeleteView(LoginRequiredMixin,DeleteView):
    def get_queryset(self):
        qs=super(OwnerDeleteView, self).get_queryset()
        return qs.filter(owner=self.request.user)