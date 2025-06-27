from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.views import generic
from agents.mixins import OrganisorAndLoginRequiredMixin
from .models import Lead, Agent, Category
from .forms import LeadForm, LeadModelForm, CustomUserCreationForm, AssignAgentForm, LeadCategoryUpdateForm

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

class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            # ✅ Show only assigned leads
            return Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=False
            )
        else:
            return Lead.objects.filter(
                organisation=user.agent.organisation,
                agent__user=user
            )

    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            # ✅ Unassigned leads only shown here
            unassigned_leads = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True
            )
            context["unassigned_leads"] = unassigned_leads
        return context

'''class LeadListView(LoginRequiredMixin, generic.ListView):
    trmplate_name = "leads/lead_list.html"
    context_object_name = "leads"

    def get_queryset(self):
        user = self.request.user
        # Check if the user is an organizer or an agent
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation,
                agent__isnull=True
            )
            # filter for the agents that logged in
            queryset = queryset.filter(agent__user=user)
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super(LeadListView, self).get_context_data(**kwargs)
        user = self.request.user
        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
                agent__isnull=True
            )
            context.update({
                "unassigned_leads" : queryset
            })
        return context'''

# List view for leads using function-based view
def lead_list(request):
    leads = Lead.objects.all()
    context = {
        "leads" : leads
    }
    return render(request, "leads/lead_list.html", context)

# Detail view for a single lead using class-based view
class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    trmplate_name = "leads/lead_detail.html"
    context_object_name = "lead"

    def get_queryset(self):
        user = self.request.user
        # Check if the user is an organizer or an agent
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agents that logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

# Detail view for a single lead using function-based view
def lead_detail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {
        "lead": lead
    }
    return render(request, "leads/lead_detail.html", context)

# Create view for a new lead using class-based view
class LeadCreateView(OrganisorAndLoginRequiredMixin, generic.CreateView):
    template_name = "leads/lead_create.html"
    form_class = LeadModelForm
    
    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        # TODO send email
        lead = form.save(commit=False)
        lead.organisation = self.request.user.userprofile  # ✅ Set the organisation
        lead.save()
        
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
class LeadUpdateView(OrganisorAndLoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_update.html"
    form_class = LeadModelForm

    def get_queryset(self):
        user = self.request.user
        # initial queryset for the entire organisation  
        return Lead.objects.filter(organisation=user.userprofile)

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
class LeadDeleteView(OrganisorAndLoginRequiredMixin, generic.DeleteView):
    template_name = "leads/lead_delete.html"
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse("leads:lead-list")

    def get_queryset(self):
        user = self.request.user
        # initial queryset for the entire organisation  
        return Lead.objects.filter(organisation=user.userprofile)

# Delete view for a lead using function-based view
def lead_delete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect("/leads")

class AssignAgentView(OrganisorAndLoginRequiredMixin, generic.FormView):
    template_name = "leads/assign_agent.html"
    form_class = AssignAgentForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(AssignAgentView, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request": self.request
        })
        return kwargs

    def get_success_url(self):
        return reverse("leads:lead-list")
    
    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs["pk"])
        lead.agent = agent
        lead.save()
        return super(AssignAgentView, self).form_valid(form)

class CategoryListView(LoginRequiredMixin, generic.ListView):
    template_name = "leads/category_list.html"
    context_object_name = "category_list"

    def get_context_data(self, **kwargs):
        context = super(CategoryListView, self).get_context_data(**kwargs)
        user = self.request.user

        if user.is_organisor:
            queryset = Lead.objects.filter(
                organisation=user.userprofile,
            )
        else:
            queryset = Lead.objects.filter(
                organisation=user.agent.organisation,
            )
        
        context.update({
            "unassigned_lead_count": queryset.filter(category__isnull=True).count(),
        })
        return context

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            return Category.objects.filter(
                organisation=user.userprofile,
            )
        else:
            return Category.objects.filter(
                organisation=user.agent.organisation,
            )

class CategoryDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = "leads/category_detail.html"
    context_object_name = "category"

    # This method commented because same logic is implemented in the template(category_detail.html)
    # Uncomment if you want to use it for additional context data
    '''def get_context_data(self, **kwargs):
        context = super(CategoryDetailView, self).get_context_data(**kwargs)
        leads = self.get_object().leads.all()
        context.update({
            "leads": leads
        })
        return context'''

    def get_queryset(self):
        user = self.request.user
        if user.is_organisor:
            return Category.objects.filter(
                organisation=user.userprofile,
            )
        else:
            return Category.objects.filter(
                organisation=user.agent.organisation,
            )
        
class LeadCategoryUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = "leads/lead_category_update.html"
    form_class = LeadCategoryUpdateForm

    def get_queryset(self):
        user = self.request.user
        # Check if the user is an organizer or an agent
        if user.is_organisor:
            queryset = Lead.objects.filter(organisation=user.userprofile)
        else:
            queryset = Lead.objects.filter(organisation=user.agent.organisation)
            # filter for the agents that logged in
            queryset = queryset.filter(agent__user=user)
        return queryset

    def get_success_url(self):
        return reverse("leads:lead-detail", kwargs={"pk": self.get_object().id})



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



