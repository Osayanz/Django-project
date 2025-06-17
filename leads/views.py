from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from django.views import generic
from .models import Lead, Agent
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm

class SignUpView(generic.CreateView):
    template_name = "registration/signup.html"
    form_class = CustomUserCreationForm
    
    def get_success_url(self):
        return reverse("login")


# CRUD+L - Create, Retrieve, Update, and Delete + List

# Landing page view class
class LandingPageView(generic.TemplateView):
    template_name = 'landing.html'

# Landing page view function
def landing_page(request):
    return render(request, "landing.html")

# List view for leads using class-based view
class LeadListView(generic.ListView):
    trmplate_name = "leads/lead_list.html"
    queryset = Lead.objects.all()
    context_object_name = "leads"

# List view for leads using function-based view
def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads" : leads
    }
    return render(request, "leads/lead_list.html", context)

# Detail view for a single lead using class-based view
class LeadDetailView(generic.DetailView):
    trmplate_name = "leads/lead_detail.html"
    queryset = Lead.objects.all()
    context_object_name = "lead"

# Detail view for a single lead using function-based view
def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)

# Create view for a new lead using class-based view
class LeadCreateView(generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        # TODO send email
        send_mail(
            subject="A lead has been created",
            message="Go to the site to view the new lead",
            from_email="test@test.com",
            recipient_list=["test2@test.com"]
        )
        return super(LeadCreateView, self).form_valid(form)

# Create view for a new lead using function-based view
def lead_create(request):
    form = LeadModelForm()
    if request.method == "POST":
        form = LeadModelForm(request.POST)
        if form.is_valid():
            form.save()
            # first_name = form.cleaned_data["first_name"]
            # last_name = form.cleaned_data["last_name"]
            # age = form.cleaned_data["age"]
            # agent = form.cleaned_data["agent"]
            # Lead.objects.create(
            #     first_name=first_name,
            #     last_name=last_name,
            #     age=age,
            #     agent=agent
            # )
            return redirect("/leads")
    context = {
        "form": form
    }
    return render(request, "leads/lead_create.html", context)

# Update view for a lead using class-based view
class LeadUpdateView(generic.UpdateView):
    template_name = "leads/lead_update.html"
    queryset = Lead.objects.all()
    form_class = LeadModelForm

    def get_success_url(self):
        return reverse("leads:lead-list")

# Update view for a lead using function-based view
def lead_update(request, pk):
    lead = Lead.objects.get(id=pk)
    form = LeadModelForm(instance=lead)
    if request.method == "POST":
        form = LeadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect("/leads")
    context = {
        "lead": lead,
        "form": form
    }
    return render(request, "leads/lead_update.html", context)

# Delete view for a lead using class-based view
class LeadDeleteView(generic.DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")

# Delete view for a lead using function-based view
def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")


# Uncomment the following code if you want to use the non-model form version

# def lead_update(request, pk):
#     lead = Lead.objects.get(id=pk)
#     form = LeadForm()
#     if request.method == "POST":
#         form = LeadForm(request.POST)
#         if form.is_valid():
#             first_name = form.cleaned_data["first_name"]
#             last_name = form.cleaned_data["last_name"]
#             age = form.cleaned_data["age"]
#             lead.first_name = first_name
#             lead.last_name = last_name
#             lead.age = age
#             lead.save()
#             return redirect("/leads")
    # context = {
    #     "lead": lead,
    #     "form": form
    # }
    # return render(request, "leads/lead_update.html", context)


# Uncomment the following code if you want to use the non-model form version

# def lead_create(request):
    # form = LeadForm()
    # if request.method == "POST":
    #     form = LeadForm(request.POST)
    #     if form.is_valid():
    #         first_name = form.cleaned_data["first_name"]
    #         last_name = form.cleaned_data["last_name"]
    #         age = form.cleaned_data["age"]
    #         agent = Agent.objects.first()
    #         Lead.objects.create(
    #             first_name=first_name,
    #             last_name=last_name,
    #             age=age,
    #             agent=agent
    #         )
    #         return redirect("/leads")
    # context = {
    #     "form": form
    # }
    # return render(request, "leads/lead_create.html", context)



