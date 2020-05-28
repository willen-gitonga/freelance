from django.shortcuts import render
from django.contrib.auth import login,authenticate, logout
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.generic import UpdateView,TemplateView,CreateView,ListView
from .forms import SignupForm,JobQuoteForm,SigninForm,ProfileCreationForm,RegisterProfileForm,PostJobForm,DigitalMediaForm
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
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect,response
import requests
from requests.auth import HTTPBasicAuth
import json
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.core.paginator import Paginator
from .mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword
from django.views.decorators.csrf import csrf_exempt
User = get_user_model()



class HomePageView(TemplateView):
    template_name = 'index.html'


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        p_form = RegisterProfileForm(request.POST)
        if form.is_valid() and p_form.is_valid():
            user = form.save()
            p_form = p_form.save(commit=False)
            p_form.user = user
            p_form.save()
            return redirect('login')
   
    else:
        form = SignupForm()
        p_form = RegisterProfileForm()
    context = {"form": form,'p_form':p_form}
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
    return redirect('signin')


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
        if form.is_valid() and current_profile is not None:
            current_profile.user = current_user
            current_profile.bio = form.cleaned_data['bio']
            current_profile.save()
            return redirect('profile-dashboard',request.user.username)
                   
    else:
        form = ProfileCreationForm()

    return render(request, 'profile.html',{'current_user':current_user,'remaining_token':remaining_token,'form':form,'profile':current_profile})



@login_required
def work_place(request):


    return render(request,'workplace.html')


@login_required
def post_digital_job(request):
    digital_job_amount = 1150

    current_user = request.user
    try:
        post_job = JobPayment.objects.get(user=request.user)
    except:
        post_job = None

    if request.method == 'POST':
        form = DigitalMediaForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = current_user
            job.save() 
            post_job.user = current_user
            post_job.job_post_paid = False
            post_job.save()
            return redirect('job-page')   
    else:
        form = DigitalMediaForm()


    return render(request,'digital-media.html',{'form':form,'post_job':post_job,'digital_job_amount':digital_job_amount}) 

@login_required
def digital_job_purchase(request):
    digital_job_amount = 1150

    current_user = request.user
    try:
        current_profile = Profile.objects.get(user=request.user)
    except:
        current_profile = None


    if request.method == 'POST':
        form = RegisterProfileForm(request.POST)
        if form.is_valid() and current_profile is not None:
            current_profile.user = current_user
            current_profile.phonenumber = form.cleaned_data['phonenumber']
            current_profile.save()
            return redirect('token-low')
                   
    else:
        form = RegisterProfileForm()


    return render(request,'digitaljob-purchase.html',{'digital_job_amount':digital_job_amount,'form':form,'profile':current_profile})


@login_required
def post_job(request):
    post_job_amount = 1350
    current_user = request.user
    try:
        post_job = JobPayment.objects.get(user=request.user)
    except:
        post_job = None

    if request.method == 'POST':
        form = PostJobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = current_user
            job.save() 
            post_job.user = current_user
            post_job.job_post_paid = False
            post_job.save()

            return redirect('job-page')   
    else:
        form = PostJobForm()

    return render(request,'post-job.html',{'form':form,'post_job':post_job,'post_job_amount':post_job_amount})

@login_required
def post_job_purchase(request):
    post_job_amount = 1350

    current_user = request.user
    try:
        current_profile = Profile.objects.get(user=request.user)
    except:
        current_profile = None


    if request.method == 'POST':
        form = RegisterProfileForm(request.POST)
        if form.is_valid() and current_profile is not None:
            current_profile.user = current_user
            current_profile.phonenumber = form.cleaned_data['phonenumber']
            current_profile.save()
            return redirect('token-low')
                   
    else:
        form = RegisterProfileForm()


    return render(request,'postjob-purchase.html',{'post_job_amount':post_job_amount,'form':form,'profile':current_profile})






@login_required
def token_purchase(request):
    
    low_amount = 300.0
    medium_amount = 850.0
    high_amount = 1200.0

    return render(request,'token-purchase.html',{'low_amount':low_amount,'medium_amount':medium_amount,'high_amount':high_amount})


@login_required
def low_purchase(request):
    low_amount = 300
    current_user = request.user
    try:
        current_profile = Profile.objects.get(user=request.user)
    except:
        current_profile = None


    if request.method == 'POST':
        form = RegisterProfileForm(request.POST)
        if form.is_valid() and current_profile is not None:
            current_profile.user = current_user
            current_profile.phonenumber = form.cleaned_data['phonenumber']
            current_profile.save()
            return redirect('token-low')
                   
    else:
        form = RegisterProfileForm()

    return render(request,'token-low.html',{'low_amount':low_amount,'form':form,'profile':current_profile})

@login_required
def medium_purchase(request):
    medium_amount = 850
    current_user = request.user
    try:
        current_profile = Profile.objects.get(user=request.user)
    except:
        current_profile = None


    if request.method == 'POST':
        form = RegisterProfileForm(request.POST)
        if form.is_valid() and current_profile is not None:
            current_profile.user = current_user
            current_profile.phonenumber = form.cleaned_data['phonenumber']
            current_profile.save()
            return redirect('token-medium')
                   
    else:
        form = RegisterProfileForm()
    return render(request,'token-medium.html',{'medium_amount':medium_amount,'form':form,'profile':current_profile})

@login_required
def high_purchase(request):
    high_amount = 1200
    current_user = request.user
    try:
        current_profile = Profile.objects.get(user=request.user)
    except:
        current_profile = None


    if request.method == 'POST':
        form = RegisterProfileForm(request.POST)
        if form.is_valid() and current_profile is not None:
            current_profile.user = current_user
            current_profile.phonenumber = form.cleaned_data['phonenumber']
            current_profile.save()
            return redirect('token-high')
                   
    else:
        form = RegisterProfileForm()
    return render(request,'token-high.html',{'high_amount':high_amount,'form':form,'profile':current_profile})


@login_required
def messaging_dashboard(request):

    return render(request, 'messaging-board.html')

def pagenotfound(request):

    return render(request,'404.html')


@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Test_c2b_shortcode,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://eclidworkers.com/jobs/SORT=new/",
               "ValidationURL": "https://eclidworkers.com/jobs/SORT=new/"}
    response = requests.post(api_url, json=options, headers=headers)

    return HttpResponse(response.text)


@csrf_exempt
def call_back(request):
    pass


@csrf_exempt
def validation(request):

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    return JsonResponse(dict(context))


@csrf_exempt
def confirmation(request):
    mpesa_body =request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)

    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],

    )
    payment.save()

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    return JsonResponse(dict(context))


@login_required
def check_transaction(request):
    current_user = request.user
    try:
        phone_number_available = Profile.objects.get(user=request.user)
        user_phone_number = phone_number_available.phonenumber
    except:
        phone_number_available = None
    try:
        eclid_token = Token.objects.get(user=request.user)  
    except:
        eclid_token = None

    try:
        valid_transaction = MpesaPayment.objects.get(phone_number=user_phone_number)
        amount_transacted = valid_transaction.amount
        if amount_transacted == 300.00 and eclid_token is None:
            token = Token(user=current_user,bid_token=3)
            token.save()
        elif amount_transacted == 300.00 and eclid_token is not None:
            eclid_token.user = current_user
            eclid_token.bid_token = 3
            eclid_token.save()

        if amount_transacted == 850.00 and eclid_token is None:
            token = Token(user=current_user,bid_token=12)
            token.save()
        elif amount_transacted == 850.00 and eclid_token is not None:
            eclid_token.user = current_user
            eclid_token.bid_token = 12
            eclid_token.save()

        if amount_transacted == 1200.00 and eclid_token is None:
            token = Token(user=current_user,bid_token=25)
            token.save()
        elif amount_transacted == 1200.00 and eclid_token is not None:
            eclid_token.user = current_user
            eclid_token.bid_token = 25
            eclid_token.save()
        valid_transaction.delete()
        return redirect('profile-dashboard',request.user.username)

    except ObjectDoesNotExist:
        return redirect('token-purchase')
        


@login_required
def post_job_transaction(request):
    current_user = request.user
    try:
        available_phone_number = Profile.objects.get(user=request.user)
        user_phone_number = available_phone_number.phonenumber
    except:
        available_phone_number = None
    try:
        job_to_post = JobPayment.objects.get(user=request.user)
    except:
        job_to_post = None

    try:
        valid_transaction = MpesaPayment.objects.get(phone_number=user_phone_number)
        amount_transacted = valid_transaction.amount
        if amount_transacted == 1300.00 and job_to_post is None:
            posted_job = JobPayment(user=current_user,job_post_paid=True)
            posted_job.save()

        elif amount_transacted == 1300.00 and job_to_post is not None:
            posted_job.user = current_user
            posted_job.job_post_paid = True
            posted_job.save()
        
        valid_transaction.delete()
        return redirect('post-job')

    except ObjectDoesNotExist:
        return redirect('post-job-purchase')



@login_required
def promote_business_transaction(request):
    current_user = request.user
    try:
        available_phone_number = Profile.objects.get(user=request.user)
        user_phone_number = available_phone_number.phonenumber
    except:
        available_phone_number = None
    try:
        job_to_post = JobPayment.objects.get(user=request.user)
    except:
        job_to_post = None

    try:
        valid_transaction = MpesaPayment.objects.get(phone_number=user_phone_number)
        amount_transacted = valid_transaction.amount
        if amount_transacted == 1150.00 and job_to_post is None:
            posted_job = JobPayment(user=current_user,job_post_paid=True)
            posted_job.save()

        elif amount_transacted == 1150.00 and job_to_post is not None:
            posted_job.user = current_user
            posted_job.job_post_paid = True
            posted_job.save()
        
        valid_transaction.delete()
        return redirect('digital-media')

    except ObjectDoesNotExist:
        return redirect('digital-job-purchase')



    



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



