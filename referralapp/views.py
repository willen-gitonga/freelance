from django.shortcuts import render
from django.contrib.auth import login,authenticate, logout
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.generic import UpdateView,TemplateView,CreateView,ListView
from .forms import SignupForm,TokenForm,JobQuoteForm,SigninForm,ProfileEditForm,ProfileCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,JsonResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.core.paginator import Paginator
# from account.views import SignupView as BaseSignupView
# from .mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
User = get_user_model()



class HomePageView(TemplateView):
    template_name = 'index.html'


       

def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            return redirect('job-page')
        
    else:
        form = SignupForm()
    context = {"form": form}
    return render(request, "registration/signup.html", context)


def signin(request):
    if request.method=="POST":
        form = SigninForm(request.POST)
        # username = req.POST["username"]
        # password = req.POST["password"]
        username = form["username"].value()
        password = form["password"].value()
        user = authenticate(request, username=username,  password=password)
        if user is not None:
            login(request, user)
            return redirect("job-page")
    else:
        form = SigninForm()
    context = {"form": form}
    return render(request, "registration/login.html", context)

@login_required
def signout(request):
    logout(request)
    return redirect('login')


@login_required
def jobs(request):
    jobs = Job.objects.order_by('-creation_date')
    current_user = request.user
    paginator = Paginator(jobs,8) #Show 8 jobs per page
    page = request.GET.get('page')
    available_jobs = paginator.get_page(page)

    return render(request, 'jobs.html',{'available_jobs':available_jobs})

@login_required
def sort_price_highest(request):
    jobs = Job.objects.order_by('-upper_limit')
    paginator = Paginator(jobs,8) # Show 8 jobs per page 
    page = request.GET.get('page')
    sorted_jobs = paginator.get_page(page)


    return render(request, 'jobs-sorted.html',{'sorted_jobs':sorted_jobs})


@login_required
def bid_job(request,slug):
   
    current_user = request.user 
    try:
        job = Job.objects.get(slug=slug)
    except:
        return HttpResponseRedirect(reverse('404page'))


    if request.method == 'POST':
        form = JobQuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = current_user
            quote.job = job
            quote.save()
            try:
                token = Token.objects.get(user=request.user)  
                token.user = current_user  
                token.bid_token-=1
                token.save()
            except:
                token = None    
           
            return redirect('job-page')
            
               
       
    else:
        form = JobQuoteForm()
    
    try:
        remaining_token = Token.objects.get(user=request.user)
    except:
        remaining_token = None
    
        
   
    return render (request,'particular-job.html',{'job':job,'form':form,'remaining_token':remaining_token})

@login_required
def profile_dashboard(request,slug):
    try:
        user = User.objects.get(username=slug)
    except:
        return HttpResponseRedirect(reverse('404page'))
    current_user = request.user
    try:
        remaining_token = Token.objects.get(user=request.user)
    except:
        remaining_token = None
    try:
        current_profile = Profile.objects.get(user=request.user)
    except:
        current_profile = None


    if request.method == 'POST':
        form = ProfileCreationForm(request.POST)
        if form.is_valid() and current_profile is None:
            profile = form.save(commit=False)
            profile.user = current_user
            profile.save()
            return redirect('profile-dashboard',request.user.username)
        elif form.is_valid() and current_profile is not None:
            current_profile.user = current_user
            current_profile.first_name = form.cleaned_data['first_name']
            current_profile.last_name = form.cleaned_data['last_name']
            current_profile.bio = form.cleaned_data['bio']
            current_profile.save()
            return redirect('profile-dashboard',request.user.username)
                   
    else:
        form = ProfileCreationForm()




   
# end
    
   
    
    return render(request, 'profile.html',{'current_user':current_user,'remaining_token':remaining_token,'form':form,'profile':current_profile})



@login_required    
def token_purchase(request):
    current_user = request.user
    if request.method == 'POST':
        form = TokenForm(request.POST)
        if form.is_valid():
            token = form.save(commit=False)
            token.user = current_user
            if form.cleaned_data['token_price'] == 3:
                return redirect('token-low')
            elif form.cleaned_data['token_price'] == 5:
                return redirect('token-medium')
            elif form.cleaned_data['token_price'] == 7:
                return redirect('token-high') 

    else:
        form = TokenForm()
    return render(request, 'token.html',{"form":form})





@login_required
def token_low(request):

    return render(request, 'token-low.html')



@login_required
def token_medium(request):

    return render(request, 'token-medium.html')


@login_required
def token_high(request):

    return render(request, 'token-high.html')



@login_required
def messaging_dashboard(request):

    return render(request, 'messaging-board.html')
def pagenotfound(request):

    return render(request,'404.html')





# def getAccessToken(request):
#     consumer_key = 'cHnkwYIgBbrxlgBoneczmIJFXVm0oHky'
#     consumer_secret = '2nHEyWSD4VjpNh2g'
#     api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'
#     r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
#     mpesa_access_token = json.loads(r.text)
#     validated_mpesa_access_token = mpesa_access_token['access_token']
#     return HttpResponse(validated_mpesa_access_token)

# def lipa_na_mpesa_online(request):

#     access_token = MpesaAccessToken.validated_mpesa_access_token
#     api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
#     headers = {"Authorization": "Bearer %s" % access_token}
#     request = {
#         "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
#         "Password": LipanaMpesaPpassword.decode_password,
#         "Timestamp": LipanaMpesaPpassword.lipa_time,
#         "TransactionType": "CustomerPayBillOnline",
#         "Amount": 10,
#         "PartyA": 254743303681,  # replace with your phone number to get stk push
#         "PartyB": LipanaMpesaPpassword.Business_short_code,
#         "PhoneNumber": 254743303681,  # replace with your phone number to get stk push
#         "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
#         "AccountReference": "Henry",
#         "TransactionDesc": "Testing stk push"
#     }
#     response = requests.post(api_url, json=request, headers=headers)
#     return HttpResponse('success')







        

