from django.core.mail import message, send_mail
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views import generic
from .models import Agent, Lead
from .forms import LeadForm, LeadModelForm


# CRUD+L - Create, Retrieve, Update and Delete + List view
# Start from 3:54:31

# -----landing page Class based view's-------
class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'

# ----Function based view's
# def landing_page(request):
#     return render(request, 'landing.html')


# -----Generic List View -------
class LeadListView(generic.ListView):
    template_name = "leads/lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"

# ----Function List View--------


def lead_list(request):
    leads = Lead.objects.all()
    context = {'leads': leads}
    return render(request, "leads/lead_list.html", context)

# ------ Generic Detail View--------


class LeadDetailView(generic.DetailView):
    template_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"

# ------Function Detail view--------


def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead,
    }
    return render(request, "leads/lead_detail.html", context)


# --------------------lead create with Model Form which reduce the amount of code------------------

# -------generic Create View-------
class LeadCreateView(generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

    def form_valid(self, form):
        # TODO send email
        send_mail(
            subject="A lead has been created",
            message="Go to the site to see the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)

# --------Function Lead Create view-------


def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()   # Model Form reduce the amount of code
            return redirect("/leads")
    context = {
        'form': form
    }
    return render(request, "leads/lead_create.html", context)


# -------------------------lead update with Model Form-----------------------------

# -------Generic Lead Update View------

class LeadUpdateView(generic.UpdateView):
    template_name = "leads/lead_update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

# ----Function Lead Update view--------


def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return("/leads")

    context = {
        'form': form,
        'lead': lead
    }
    return render(request, 'leads/lead_update.html', context)

# ------generic Class based Delete view-------


class LeadDeleteView(generic.DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")

# ------Function based Delete View-------


def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")

# ---------------------------lead update with Simple Form---------------------------

# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
    # form = LeadForm()
    # if request.method == 'POST':
    #     form = LeadForm(request.POST)
    #     if form.is_valid():
    #         first_name = form.cleaned_data['first_name']
    #         last_name = form.cleaned_data['last_name']
    #         age = form.cleaned_data['age']
    #         lead.first_name = first_name
    #         lead.last_name = last_name
    #         lead.age = age
    #         lead.save()
    #         return redirect('/leads')
    # context = {
    #     'form': form,
    #     'lead': lead
    # }
    # return render(request, 'leads/lead_update.html', context)


# -----------------------lead create with Simple Form-----------------------------

# def lead_create(request):
#     form = LeadForm()
#     if request.method == "POST":
#         print('Receiving a post request')
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             print("The form is valid")
#             print(form.cleaned_data)
#             first_name = form.cleaned_data['first_name']
#             last_name = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.first()
#             Lead.objects.create(
#                 first_name=first_name,
#                 last_name=last_name,
#                 age=age,
#                 agent=agent
#             )
#             print('Lead has been created')
#             return redirect("/leads")
#     context = {
#         'form': form
#     }
#     return render(request, "leads/lead_create.html", context)
