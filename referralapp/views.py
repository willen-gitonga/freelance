from django.shortcuts import render
from django.contrib.auth import login,authenticate, logout
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.urls import reverse
from django.views.generic import UpdateView,TemplateView,CreateView,ListView
from .forms import SignupForm,JobQuoteForm,ProfileCreationForm,RegisterProfileForm,PostJobForm,DigitalMediaForm,FreelanceSkillAdvertiseForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect,response
import requests
from requests.auth import HTTPBasicAuth
import json
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from celery.schedules import crontab
from celery.task import periodic_task
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
User = get_user_model()
import os, hashlib, warnings, requests, json
import base64
from Crypto.Cipher import DES3
from django.views import View



class HomePageView(TemplateView):
    template_name = 'index.html'



@periodic_task(run_every=crontab(minute='*/5'))
def delete_old_skill():
    # Query all the foos in our database
    foos = FreelanceSkills.objects.all()

    # Iterate through them
    for foo in foos:

        # If the expiration date is bigger than now delete it
        if foo.expiry_date < timezone.now():
            foo.delete()

@periodic_task(run_every=crontab(minute='*/5'))
def delete_old_business():
    # Query all the foos in our database
    foos = MerchantPromote.objects.all()

    # Iterate through them
    for foo in foos:

        # If the expiration date is bigger than now delete it
        if foo.expiry_date < timezone.now():
            foo.delete()

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

def terms_conditions(request):

    return render(request,'terms-conditions.html')

@login_required
def jobs(request):

   
    jobs = Job.objects.order_by('-creation_date')
    current_user = request.user
    paginator = Paginator(jobs,8) #Show 8 jobs per page
    page = request.GET.get('page')
    available_jobs = paginator.get_page(page)

    return render(request, 'freelancer/jobs.html',{'available_jobs':available_jobs})

@login_required
def sort_price_highest(request):
    jobs = Job.objects.order_by('-upper_limit')
    paginator = Paginator(jobs,8) # Show 8 jobs per page 
    page = request.GET.get('page')
    sorted_jobs = paginator.get_page(page)


    return render(request, 'freelancer/jobs-sorted.html',{'sorted_jobs':sorted_jobs})

#Different categories of the jobs posted
@login_required
def sort_software_jobs(request):
    count_jobs = Job.objects.filter(job_category=1).count()
    sorted_jobs = Job.objects.filter(job_category=1)
   

    return render(request, 'freelancer/sort-software-jobs.html',{'sorted_jobs':sorted_jobs,'count_jobs':count_jobs})

@login_required
def sort_product_jobs(request):
    count_jobs = Job.objects.filter(job_category=2).count()
    sorted_jobs = Job.objects.filter(job_category=2)
   

    return render(request,'freelancer/sort-product-jobs.html',{'sorted_jobs':sorted_jobs,'count_jobs':count_jobs})


@login_required
def sort_marketing_jobs(request):
    count_jobs = Job.objects.filter(job_category=3).count()
    sorted_jobs = Job.objects.filter(job_category=3)
   

    return render(request,'freelancer/sort-marketing-jobs.html',{'sorted_jobs':sorted_jobs,'count_jobs':count_jobs})

@login_required
def sort_writing_jobs(request):
    count_jobs = Job.objects.filter(job_category=4).count()
    sorted_jobs = Job.objects.filter(job_category=4)
  

    return render(request,'freelancer/sort-writing-jobs.html',{'sorted_jobs':sorted_jobs,'count_jobs':count_jobs})

@login_required
def sort_customer_service_jobs(request):
    count_jobs = Job.objects.filter(job_category=5).count()
    sorted_jobs = Job.objects.filter(job_category=5)


    return render(request,'freelancer/sort-customerservice-jobs.html',{'sorted_jobs':sorted_jobs,'count_jobs':count_jobs})

@login_required
def sort_referral_jobs(request):
    count_jobs = Job.objects.filter(job_category=6).count()
    sorted_jobs = Job.objects.filter(job_category=6)
  


    return render(request,'freelancer/sort-referral-jobs.html',{'sorted_jobs':sorted_jobs,'count_jobs':count_jobs})

@login_required
def sort_data_entry_jobs(request):
    count_jobs = Job.objects.filter(job_category=7).count()
    sorted_jobs = Job.objects.filter(job_category=7)
   

    return render(request,'freelancer/sort-dataentry-jobs.html',{'sorted_jobs':sorted_jobs,'count_jobs':count_jobs})

@login_required
def sort_other_unspecified_jobs(request):
    count_jobs = Job.objects.filter(job_category=8).count()
    sorted_jobs = Job.objects.filter(job_category=8)
   
    return render(request,'freelancer/sort-unspecified-jobs.html',{'sorted_jobs':sorted_jobs,'count_jobs':count_jobs})

#End of job category part
@login_required
def bid_job(request,pk):
   
    current_user = request.user 
    try:
        job = Job.objects.get(id=pk)
    except:
        return HttpResponseRedirect(reverse('404page'))
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = None

    offers_count = Quote.objects.filter(job__id=job.id).count()

    if request.method == 'POST':
        form = JobQuoteForm(request.POST)
        if form.is_valid():
            quote = form.save(commit=False)
            quote.user = current_user
            quote.job = job
            quote.profile = profile 
            quote.save()
            try:
                token = Token.objects.get(user=request.user)  
                token.user = current_user  
                token.bid_token-=1
                token.save()
            except:
                token = None    

            return redirect('sent-quotes')
            
    else:
        form = JobQuoteForm()
    try:
        remaining_token = Token.objects.get(user=request.user)
    except:
        remaining_token = None
    
    return render (request,'freelancer/particular-job.html',{'job':job,'form':form,'remaining_token':remaining_token,'offers_count':offers_count})

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

    return render(request, 'general/profile.html',{'current_user':current_user,'remaining_token':remaining_token,'form':form,'profile':current_profile})

@login_required
def all_promoted_business(request):
    all_business = MerchantPromote.objects.all()


    return render(request,'general/all-businesses.html',{'all_business':all_business})

@login_required
def all_promoted_skills(request):
    all_skills = FreelanceSkills.objects.all()

    return render(request,'general/all-skills.html',{'all_skills':all_skills})



@login_required
def work_place(request):

    return render(request,'general/workplace.html')


@login_required
def eclid_digital_nomad(request):

    return render(request,'general/digital-nomad.html')

#check the url of this function to redirect to another page
@login_required
def post_digital_job(request):
    digital_job_amount = 1000

    current_user = request.user
    try:
        post_business = BusinessPromotePayment.objects.get(user=request.user)
    except:
        post_business = None
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = None


    if request.method == 'POST':
        form = DigitalMediaForm(request.POST, request.FILES)
        if form.is_valid():
            business = form.save(commit=False)
            business.user = current_user
            business.profile = profile
            business.save() 
            post_business.user = current_user
            post_business.business_post_paid = False
            post_business.save()
            return redirect('promoted-business-user',request.user.username)   
    else:
        form = DigitalMediaForm()


    return render(request,'merchant/digital-media.html',{'form':form,'post_business':post_business,'digital_job_amount':digital_job_amount}) 

@login_required
def digital_job_purchase(request):
    digital_job_amount = 1000

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
            return redirect('digital-job-purchase')
                   
    else:
        form = RegisterProfileForm()


    return render(request,'merchant/digitaljob-purchase.html',{'digital_job_amount':digital_job_amount,'form':form,'profile':current_profile})


#Write views for this function in url

@login_required
def promoted_business_user(request,slug):
    try:
        user = User.objects.get(username=slug)
    except:
        return HttpResponseRedirect(reverse('404page'))

    business_renew_amount = 500
    current_user = request.user
    all_business_user_count = MerchantPromote.objects.filter(user=current_user).count()
    all_business_user = MerchantPromote.objects.filter(user=current_user)


    return render(request,'merchant/promoted-business-user.html',{'all_business_user':all_business_user,'business_renew_amount':business_renew_amount,'all_business_user_count':all_business_user_count})


#Write views for this functions in the url
@login_required
def freelance_skills_post(request):
    freelance_skills_amount = 1000

    current_user = request.user
    try:
        post_skill = SkillPromotePayment.objects.get(user=request.user)
    except:
        post_skill = None

    if request.method == 'POST':
        form = FreelanceSkillAdvertiseForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = current_user
            skill.save() 
            post_skill.user = current_user
            post_skill.skill_post_paid = False
            post_skill.save()
            return redirect('promoted-skill-user',request.user.username)   
    else:
        form = FreelanceSkillAdvertiseForm()

    return render(request,'freelancer/advertise-skills.html',{'freelance_skills_amount':freelance_skills_amount,'form':form,'post_skill':post_skill})

#fix redirect links
@login_required
def freelance_skill_purchase(request):
    freelance_skills_amount = 1000
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
            return redirect('freelance-skill-purchase')
                   
    else:
        form = RegisterProfileForm()


    return render(request,'freelancer/advertise-skill-purchase.html',{'freelance_skills_amount':freelance_skills_amount,'form':form,'profile':current_profile})



    
@login_required
def promoted_skill_user(request,slug):
    try:
        user = User.objects.get(username=slug)
    except:
        return HttpResponseRedirect(reverse('404page'))
    current_user = request.user

    freelance_skill_count = FreelanceSkills.objects.filter(user=current_user).count()
    freelance_skill = FreelanceSkills.objects.filter(user=current_user)

    freelance_skills_renew_amount = 500
    


    return render(request,'freelancer/promoted-skill-user.html',{'freelance_skill':freelance_skill,'freelance_skills_renew_amount':freelance_skills_renew_amount,'freelance_skill_count':freelance_skill_count})
#These views above need urls 

@login_required
def post_job(request):
    post_job_amount = 1300
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
            return redirect('posted-jobs-user')  
    else:
        form = PostJobForm()

    return render(request,'client/post-job.html',{'form':form,'post_job':post_job,'post_job_amount':post_job_amount})

@login_required
def posted_job_user(request):
    current_user = request.user
    post_jobs_user_count = Job.objects.filter(user=current_user).count()
    post_jobs_user = Job.objects.filter(user=current_user)

    return render(request,'client/posted-jobs-user.html',{'post_jobs_user':post_jobs_user,'post_jobs_user_count':post_jobs_user_count})

@login_required
def post_job_purchase(request):
    post_job_amount = 1300

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
            return redirect('post-job-purchase')
                   
    else:
        form = RegisterProfileForm()


    return render(request,'client/postjob-purchase.html',{'post_job_amount':post_job_amount,'form':form,'profile':current_profile})

@login_required
def received_quotes(request):
    current_user = request.user.id
   

    job_quotes_count = Quote.objects.filter(job__user_id=current_user).count()
    job_quotes = Quote.objects.filter(job__user_id=current_user)

    return render(request,'client/received-quotes.html',{'job_quotes':job_quotes,'job_quotes_count':job_quotes_count})

@login_required
def sent_quotes(request):
    current_user = request.user
    sent_job_quotes_count = Quote.objects.filter(user=current_user).count()
    sent_job_quotes = Quote.objects.filter(user=current_user)
    return render(request,'freelancer/sent-quotes.html',{'sent_job_quotes':sent_job_quotes,'sent_job_quotes_count':sent_job_quotes_count})

@login_required
def token_purchase(request):
    
    low_amount = 200.0
    medium_amount = 850.0
    high_amount = 1500.0

    return render(request,'freelancer/token-purchase.html',{'low_amount':low_amount,'medium_amount':medium_amount,'high_amount':high_amount})


@login_required
def low_purchase(request):
    low_amount = 200
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

    return render(request,'freelancer/token-low.html',{'low_amount':low_amount,'form':form,'profile':current_profile})

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
    return render(request,'freelancer/token-medium.html',{'medium_amount':medium_amount,'form':form,'profile':current_profile})

@login_required
def high_purchase(request):
    high_amount = 1500
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
    return render(request,'freelancer/token-high.html',{'high_amount':high_amount,'form':form,'profile':current_profile})


@login_required
def messaging_dashboard(request):

    return render(request, 'messaging-board.html')

def pagenotfound(request):

    return render(request,'404.html')





#Change the validation urls
# @csrf_exempt
# def register_urls(request):
#     access_token = MpesaAccessToken.validated_mpesa_access_token
#     api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
#     headers = {"Authorization": "Bearer %s" % access_token}
#     options = {"ShortCode": LipanaMpesaPpassword.Test_c2b_shortcode,
#                "ResponseType": "Completed",
#                "ConfirmationURL": "https://eclidworkers.com/jobs/SORT=new/",
#                "ValidationURL": "https://eclidworkers.com/jobs/SORT=new/"}
#     response = requests.post(api_url, json=options, headers=headers)

#     return HttpResponse(response.text)


# @csrf_exempt
# def call_back(request):
#     pass


# @csrf_exempt
# def validation(request):

#     context = {
#         "ResultCode": 0,
#         "ResultDesc": "Accepted"
#     }
#     return JsonResponse(dict(context))


# @csrf_exempt
# def confirmation(request):
#     mpesa_body =request.body.decode('utf-8')
#     mpesa_payment = json.loads(mpesa_body)

#     payment = MpesaPayment(
#         first_name=mpesa_payment['FirstName'],
#         last_name=mpesa_payment['LastName'],
#         middle_name=mpesa_payment['MiddleName'],
#         description=mpesa_payment['TransID'],
#         phone_number=mpesa_payment['MSISDN'],
#         amount=mpesa_payment['TransAmount'],
#         reference=mpesa_payment['BillRefNumber'],
#         organization_balance=mpesa_payment['OrgAccountBalance'],
#         type=mpesa_payment['TransactionType'],

#     )
#     payment.save()

#     context = {
#         "ResultCode": 0,
#         "ResultDesc": "Accepted"
#     }

#     return JsonResponse(dict(context))


def getKey(secret_key):
    hashedseckey = hashlib.md5(secret_key.encode("utf-8")).hexdigest()
    hashedseckeylast12 = hashedseckey[-12:]
    seckeyadjusted = secret_key.replace('FLWSECK-', '')
    seckeyadjustedfirst12 = seckeyadjusted[:12]
    return seckeyadjustedfirst12 + hashedseckeylast12

    """This is the encryption function that encrypts your payload by passing the text and your encryption Key."""

def encryptData(key, plainText):
    blockSize = 8
    padDiff = blockSize - (len(plainText) % blockSize)
    cipher = DES3.new(key, DES3.MODE_ECB)
    plainText = "{}{}".format(plainText, "".join(chr(padDiff) * padDiff))
    # cipher.encrypt - the C function that powers this doesn't accept plain string, rather it accepts byte strings, hence the need for the conversion below
    test = plainText.encode('utf-8')
    encrypted = base64.b64encode(cipher.encrypt(test)).decode("utf-8")
    return encrypted


def pay_via_card(request):
    data = {
    "PBFPubKey": "FLWPUBK-598d91106bd24476ed494f86531cbeb0-X",
    "currency": "KES",
    "country": "KE",
    "amount": "1",
    "phonenumber": "254706274750",
    "email": "shawgitonga@gmail.com",
    "txRef": "rj-222",
    "payment_type": "mpesa",
    "is_mpesa": "1",
    "is_mpesa_lipa": 1
    }

    sec_key = 'FLWSECK-c2a456efd68204aa7f2ee92d5ba61b55-X'

        # hash the secret key with the get hashed key function
    hashed_sec_key = getKey(sec_key)

        # encrypt the hashed secret key and payment parameters with the encrypt function

    encrypt_3DES_key = encryptData(hashed_sec_key, json.dumps(data))

        # payment payload
    payload = {
        "PBFPubKey": "FLWPUBK-598d91106bd24476ed494f86531cbeb0-X",
        "client": encrypt_3DES_key,
        "alg": "3DES-24",
    }

        # card charge endpoint
    endpoint = "https://api.ravepay.co/flwv3-pug/getpaidx/api/charge"

        # set the content type to application/json
    headers = {
        'content-type': 'application/json',
    }

    response = requests.post(endpoint, headers=headers, data=json.dumps(payload))
    print(response.json())
    messages.success(request,'Payment has been initiated.Kindly wait for confirmation.')
    return redirect('token-low')

@require_http_methods(["POST"])
@csrf_exempt
def my_webhook_view(request):

    # Retrieve the request's body
    request_json = request.body
    

    payment = RavePayment(

    amount=request_json['amount'],
    phone_number=request_json['customer']['phone'],
    
  
    )
    payment.save()


    # Do something with request_json

    return HttpResponse(status=200)



def callback_function(response):
    data = {
    "txref": "jw-222", #this is the reference from the payment button response after customer paid.
    "SECKEY": 'FLWSECK_TEST-edaf6d57def71f454450e6bc0d3ebafe-X'#this is the secret key of the pay button generated
    }
    url = "https://api.ravepay.co/flwv3-pug/getpaidx/api/verify"

    #make the http post request to our server with the parameters
    thread = requests.post(url, headers={"Content-Type":"application/json"}, params=data,callback=callback_function)


    if response.body['data']['status'] == 'successful' and response.body['data']['chargecode']== '00':
 
        if response.body['data']['amount'] == 200:

                print("Payment successful")


   



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
        valid_transaction = RavePayment.objects.get(phone_number=user_phone_number)
        amount_transacted = valid_transaction.amount
        if amount_transacted == 200 and eclid_token is None:
            token = Token(user=current_user,bid_token=1)
            token.save()
        elif amount_transacted == 200 and eclid_token is not None:
            eclid_token.user = current_user
            eclid_token.bid_token = 1
            eclid_token.save()

        if amount_transacted == 850 and eclid_token is None:
            token = Token(user=current_user,bid_token=12)
            token.save()
        elif amount_transacted == 850 and eclid_token is not None:
            eclid_token.user = current_user
            eclid_token.bid_token = 12
            eclid_token.save()

        if amount_transacted == 1500 and eclid_token is None:
            token = Token(user=current_user,bid_token=25)
            token.save()
        elif amount_transacted == 1500 and eclid_token is not None:
            eclid_token.user = current_user
            eclid_token.bid_token = 25
            eclid_token.save()
        valid_transaction.delete()
        messages.success(request, 'You have received Eclid tokens to your user dashboard.') 
        return redirect('profile-dashboard',request.user.username)

    except ObjectDoesNotExist:
        messages.warning(request, 'Payment has been initiated.Kindly wait for confirmation.') 
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
        valid_transaction = RavePayment.objects.get(phone_number=user_phone_number)
        amount_transacted = valid_transaction.amount
        if amount_transacted == 1300 and job_to_post is None:
            posted_job = JobPayment(user=current_user,job_post_paid=True)
            posted_job.save()

        elif amount_transacted == 1300 and job_to_post is not None:
            job_to_post.user = current_user
            job_to_post.job_post_paid = True
            job_to_post.save()
        
        valid_transaction.delete()
        messages.success(request, 'Payment has been confirmed.Post your job in the form below') 
        return redirect('post-job')

    except ObjectDoesNotExist:
        messages.warning(request, 'Payment has been initiated.Kindly wait for confirmation.') 
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
        business_to_post = BusinessPromotePayment.objects.get(user=request.user)
    except:
        business_to_post = None

    try:
        valid_transaction = RavePayment.objects.get(phone_number=user_phone_number)
        amount_transacted = valid_transaction.amount
        if amount_transacted == 1000 and business_to_post is None:
            posted_business = BusinessPromotePayment(user=current_user,business_post_paid=True)
            posted_business.save()

        elif amount_transacted == 1000 and business_to_post is not None:
            business_to_post.user = current_user
            business_to_post.business_post_paid = True
            business_to_post.save()
        
        valid_transaction.delete()
        messages.success(request, 'Payment has been confirmed.Promote your business below.') 
        return redirect('digital-media')

    except ObjectDoesNotExist:
        messages.warning(request, 'Payment has been initiated.Kindly wait for confirmation.') 
        return redirect('digital-job-purchase')

#Work on this function to redirect to the correct page after user renews business post
@login_required
def renew_business_transaction(request,pk):
    current_user = request.user
    try:
        available_phone_number = Profile.objects.get(user=request.user)
        user_phone_number = available_phone_number.phonenumber
    except:
        available_phone_number = None

    next_renewal = timezone.now()+timedelta(days=30)
          
    try:
        business_to_renew = MerchantPromote.objects.get(id=pk)
    except:
        business_to_renew = None
    try:
        valid_transaction = RavePayment.objects.get(phone_number=user_phone_number)
        amount_transacted = valid_transaction.amount
        if amount_transacted == 500 and business_to_renew is not None:
            business_to_renew.expiry_date = next_renewal
            business_to_renew.save()

        valid_transaction.delete()
        return redirect('promoted-business-user',request.user.username)
    except ObjectDoesNotExist:
        messages.warning(request, 'Payment has been initiated.Kindly wait for confirmation.') 
        return redirect('promoted-business-user',request.user.username)
       

#work on this function to redirect to the correct url after payment has been made.
@login_required
def promote_skill_transaction(request):
    current_user = request.user
    try:
        available_phone_number = Profile.objects.get(user=request.user)
        user_phone_number = available_phone_number.phonenumber
    except:
        available_phone_number = None
    try:
        skill_to_post = SkillPromotePayment.objects.get(user=request.user)
    except:
        skill_to_post = None

    try:
        valid_transaction = RavePayment.objects.get(phone_number=user_phone_number)
        amount_transacted = valid_transaction.amount
        if amount_transacted == 1000 and skill_to_post is None:
            posted_skill = SkillPromotePayment(user=current_user,skill_post_paid=True)
            posted_skill.save()
        
        elif amount_transacted == 1000 and skill_to_post is not None:
            skill_to_post.user = current_user
            skill_to_post.skill_post_paid = True
            skill_to_post.save()

        valid_transaction.delete()
        messages.success(request, 'Payment has been confirmed.Promote your skill in the form below.') 
        return redirect('freelance-skill-post')

    except ObjectDoesNotExist:
        messages.warning(request, 'Payment has been initiated.Kindly wait for confirmation.') 
        return redirect('freelance-skill-purchase')

@login_required
def renew_skill_transaction(request,pk):
    current_user = request.user
    try:
        available_phone_number = Profile.objects.get(user=request.user)
        user_phone_number = available_phone_number.phonenumber
    except:
        available_phone_number = None

    next_renewal = timezone.now()+timedelta(days=30)
    try:
        skill_to_renew = FreelanceSkills.objects.get(id=pk)
    except:
        skill_to_renew = None
    try:
        valid_transaction = RavePayment.objects.get(phone_number=user_phone_number)
        amount_transacted = valid_transaction.amount
        if amount_transacted == 500 and skill_to_renew is not None:
            skill_to_renew.expiry_date = next_renewal
            skill_to_renew.save()

        valid_transaction.delete()
        return redirect('promoted-skill-user',request.user.username)
    except ObjectDoesNotExist:
        messages.warning(request, 'Payment has been initiated.Kindly wait for confirmation.') 
        return redirect('promoted-skill-user',request.user.username)









