from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.views.generic import TemplateView
from .forms import SignupForm,JobQuoteForm,ProfileCreationForm,RegisterProfileForm,PostJobForm,DigitalMediaForm,FreelanceSkillAdvertiseForm
from django.contrib.auth.decorators import login_required
from .models import *
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse,JsonResponse,HttpResponseRedirect,response
from requests.auth import HTTPBasicAuth
from django.core.paginator import Paginator
from django.utils import timezone
from datetime import timedelta
from celery.schedules import crontab
from celery.task import periodic_task
from django.contrib import messages
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import os, hashlib, warnings,requests,json
import base64
from Crypto.Cipher import DES3
import random,string




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
        prof_form = RegisterProfileForm(request.POST)
        if prof_form.is_valid() and current_profile is not None:
            current_profile.user = current_user
            current_profile.phonenumber = prof_form.cleaned_data['phonenumber']
            current_profile.save()
            return redirect('profile-dashboard',request.user.username)          
    else:
        prof_form = RegisterProfileForm()

    if request.method == 'POST':
        form = ProfileCreationForm(request.POST)
        if form.is_valid() and current_profile is not None:
            current_profile.user = current_user
            current_profile.bio = form.cleaned_data['bio']
            current_profile.save()
            return redirect('profile-dashboard',request.user.username)
                   
    else:
        form = ProfileCreationForm()

    return render(request, 'general/profile.html',{'current_user':current_user,'remaining_token':remaining_token,'form':form,'profile':current_profile,'prof_form':prof_form})

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
    

    return render(request,'merchant/digitaljob-purchase.html')


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
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = None

    if request.method == 'POST':
        form = FreelanceSkillAdvertiseForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = current_user
            skill.profile = profile
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
    
    return render(request,'freelancer/advertise-skill-purchase.html')



    
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
    try:
        profile = Profile.objects.get(user=request.user)
    except:
        profile = None

    if request.method == 'POST':
        form = PostJobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.user = current_user
            job.profile = profile
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
    
    return render(request,'client/postjob-purchase.html')

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
def confirm_purchase(request):
    
    return render(request,'freelancer/token-low.html')





def pagenotfound(request):

    return render(request,'404.html')

def handler500(request,exception=None):
    return render(request, '500.html', status=500)



@login_required
def confirm_business_renewal(request,pk):
    try:
        business_to_renew = MerchantPromote.objects.get(id=pk)
    except:
        business_to_renew = None


    return render(request,'merchant/business-renew-confirm.html',{'business':business_to_renew})


@login_required
def confirm_skill_renewal(request,pk):
    try:
        skill_to_renew = FreelanceSkills.objects.get(id=pk)
    except:
        skill_to_renew = None
    return render(request,'freelancer/skill-renew-confirm.html',{'skill':skill_to_renew})



def randomString(stringLength=8):
    lettersAndDigits = string.ascii_letters + string.digits
    return ''.join((random.choice(lettersAndDigits) for i in range(stringLength)))
    


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


@login_required
def pay_low_token(request):
    random_string = randomString(stringLength=8)
    try:
        current_profile = Profile.objects.get(user=request.user)
        current_profile.prof_ref = random_string
        current_profile.save()
    except:
        current_profile = None
    
    data = {
    "PBFPubKey": 'FLWPUBK-598d91106bd24476ed494f86531cbeb0-X',
    "currency": "KES",
    "country": "KE",
    "amount": "235",
    "phonenumber": current_profile.phonenumber,
    "email": request.user.email,
    "txRef": current_profile.prof_ref,
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
        "PBFPubKey": 'FLWPUBK-598d91106bd24476ed494f86531cbeb0-X',
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
    return redirect('token-low')


@login_required
def pay_medium_token(request):
    random_string = randomString(stringLength=8)
    try:
        current_profile = Profile.objects.get(user=request.user)
        current_profile.prof_ref = random_string
        current_profile.save()
    except:
        current_profile = None
    
    data = {
    "PBFPubKey": 'FLWPUBK-598d91106bd24476ed494f86531cbeb0-X',
    "currency": "KES",
    "country": "KE",
    "amount": "885",
    "phonenumber": current_profile.phonenumber,
    "email": request.user.email,
    "txRef": current_profile.prof_ref,
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
        "PBFPubKey": 'FLWPUBK-598d91106bd24476ed494f86531cbeb0-X',
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
    return redirect('token-low')


@login_required
def pay_high_token(request):
    random_string = randomString(stringLength=8)
    try:
        current_profile = Profile.objects.get(user=request.user)
        current_profile.prof_ref = random_string
        current_profile.save()
    except:
        current_profile = None
    
    data = {
    "PBFPubKey": 'FLWPUBK-598d91106bd24476ed494f86531cbeb0-X',
    "currency": "KES",
    "country": "KE",
    "amount": "1545",
    "phonenumber": current_profile.phonenumber,
    "email": request.user.email,
    "txRef": current_profile.prof_ref,
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
        "PBFPubKey": 'FLWPUBK-598d91106bd24476ed494f86531cbeb0-X',
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
    return redirect('token-low')

@login_required
def pay_post_job(request):
    random_string = randomString(stringLength=8)
    try:
        current_profile = Profile.objects.get(user=request.user)
        current_profile.prof_ref = random_string
        current_profile.save()
    except:
        current_profile = None
    
    data = {
    "PBFPubKey": 'FLWPUBK-598d91106bd24476ed494f86531cbeb0-X',
    "currency": "KES",
    "country": "KE",
    "amount": "1345",
    "phonenumber": current_profile.phonenumber,
    "email": request.user.email,
    "txRef": current_profile.prof_ref,
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
        "PBFPubKey": 'FLWPUBK-598d91106bd24476ed494f86531cbeb0-X',
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
    return redirect('post-job-purchase')


@login_required
def pay_business_promote(request):
    random_string = randomString(stringLength=8)
    try:
        current_profile = Profile.objects.get(user=request.user)
        current_profile.prof_ref = random_string
        current_profile.save()
    except:
        current_profile = None
    
    data = {
    "PBFPubKey": 'FLWPUBK-598d91106bd24476ed494f86531cbeb0-X',
    "currency": "KES",
    "country": "KE",
    "amount": "1035",
    "phonenumber": current_profile.phonenumber,
    "email": request.user.email,
    "txRef": current_profile.prof_ref,
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
        "PBFPubKey": 'FLWPUBK-598d91106bd24476ed494f86531cbeb0-X',
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
    return redirect('digital-job-purchase')

@login_required
def pay_business_renewal(request,pk):

    random_string = randomString(stringLength=8)
    try:
        current_profile = Profile.objects.get(user=request.user)
        current_profile.prof_ref = random_string
        current_profile.save()
    except:
        current_profile = None
    try:
        business_to_renew = MerchantPromote.objects.get(id=pk)
    except:
        business_to_renew = None
    
    data = {
    "PBFPubKey": 'FLWPUBK-598d91106bd24476ed494f86531cbeb0-X',
    "currency": "KES",
    "country": "KE",
    "amount": "535",
    "phonenumber": current_profile.phonenumber,
    "email": request.user.email,
    "txRef": current_profile.prof_ref,
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
        "PBFPubKey": 'FLWPUBK-598d91106bd24476ed494f86531cbeb0-X',
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
    return redirect('confirm-business-renewal',business_to_renew.id)


@login_required
def pay_skill_promote(request):
    random_string = randomString(stringLength=8)
    try:
        current_profile = Profile.objects.get(user=request.user)
        current_profile.prof_ref = random_string
        current_profile.save()
    except:
        current_profile = None
    
    data = {
    "PBFPubKey": 'FLWPUBK-598d91106bd24476ed494f86531cbeb0-X',
    "currency": "KES",
    "country": "KE",
    "amount": "1035",
    "phonenumber": current_profile.phonenumber,
    "email": request.user.email,
    "txRef": current_profile.prof_ref,
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
        "PBFPubKey": 'FLWPUBK-598d91106bd24476ed494f86531cbeb0-X',
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
    return redirect('freelance-skill-purchase')


@login_required
def pay_skill_renewal(request,pk):

    random_string = randomString(stringLength=8)
    try:
        current_profile = Profile.objects.get(user=request.user)
        current_profile.prof_ref = random_string
        current_profile.save()
    except:
        current_profile = None
    try:
        skill_to_renew = FreelanceSkills.objects.get(id=pk)
    except:
        skill_to_renew = None
    
    data = {
    "PBFPubKey": 'FLWPUBK-598d91106bd24476ed494f86531cbeb0-X',
    "currency": "KES",
    "country": "KE",
    "amount": "535",
    "phonenumber": current_profile.phonenumber,
    "email": request.user.email,
    "txRef": current_profile.prof_ref,
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
        "PBFPubKey": 'FLWPUBK-598d91106bd24476ed494f86531cbeb0-X',
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
    return redirect('confirm-skill-renewal',skill_to_renew.id)






@login_required
def verify_token_transaction(request):
    current_user = request.user
    try:
        current_profile = Profile.objects.get(user=request.user)
    except:
        current_profile = None
    data = {
    "txref": current_profile.prof_ref, #this is the reference from the payment button response after customer paid.
    "SECKEY": "FLWSECK-c2a456efd68204aa7f2ee92d5ba61b55-X",
    }

    url = "https://api.ravepay.co/flwv3-pug/getpaidx/api/v2/verify"

    #make the http post request to our server with the parameters
    
    thread = requests.post(url, headers={"Content-Type":"application/json"}, data=json.dumps(data))
    # print(thread.json())
    response = thread.json()
    try:
        eclid_token = Token.objects.get(user=request.user)  
    except:
        eclid_token = None

    if response['data']['txref'] == current_profile.prof_ref and response['data']['status'] == 'successful':
        if response['data']['amount'] == 235 and eclid_token is None:
            token = Token(user=current_user,bid_token=1)
            token.save()
            messages.success(request, 'You have received an Eclid token to your freelancer dashboard.') 
            return redirect('profile-dashboard',request.user.username)
        elif response['data']['amount'] == 235 and eclid_token is not None:
            eclid_token.user = current_user
            eclid_token.bid_token = 1
            eclid_token.save()
            messages.success(request, 'You have received an Eclid token to your freelancer dashboard.') 
            return redirect('profile-dashboard',request.user.username)
        if response['data']['amount'] == 885 and eclid_token is None:
            token = Token(user=current_user,bid_token=12)
            token.save()
            messages.success(request, 'You have 12 received Eclid tokens to your freelancer dashboard.') 
            return redirect('profile-dashboard',request.user.username)
        elif response['data']['amount'] == 885 and eclid_token is not None:
            eclid_token.user = current_user
            eclid_token.bid_token = 12
            eclid_token.save()
            messages.success(request, 'You have 12 received Eclid tokens to your freelancer dashboard.') 
            return redirect('profile-dashboard',request.user.username)
        if response['data']['amount'] == 1545 and eclid_token is None:
            token = Token(user=current_user,bid_token=25)
            token.save()
            messages.success(request, 'You have 25 received Eclid tokens to your freelancer dashboard.') 
            return redirect('profile-dashboard',request.user.username)
        elif response['data']['amount'] == 1545 and eclid_token is not None:
            eclid_token.user = current_user
            eclid_token.bid_token = 25
            eclid_token.save()
            messages.success(request, 'You have 25 received Eclid tokens to your freelancer dashboard.') 
            return redirect('profile-dashboard',request.user.username)
        else:
            messages.success(request, 'Transaction has been initiated.Kindly wait for confirmation.') 
            return redirect('token-low')
    elif response['data']['acctmessage'] == 'The balance is insufficient for the transaction':
        messages.warning(request, 'Insufficient M-pesa balance.Kindly top up and try again.') 
        return redirect('token-purchase')
    else:
        messages.warning(request, 'Payment has been initiated.We will notify you when we have received the transaction.') 
        return redirect('token-low')

@login_required
def verify_job_transaction(request):
    current_user = request.user
    try:
        current_profile = Profile.objects.get(user=request.user)
    except:
        current_profile = None
    data = {
    "txref": current_profile.prof_ref, #this is the reference from the payment button response after customer paid.
    "SECKEY": "FLWSECK-c2a456efd68204aa7f2ee92d5ba61b55-X",
    }

    url = "https://api.ravepay.co/flwv3-pug/getpaidx/api/v2/verify"

    #make the http post request to our server with the parameters
    
    thread = requests.post(url, headers={"Content-Type":"application/json"}, data=json.dumps(data))
    # print(thread.json())
    response = thread.json()
    try:
        job_to_post = JobPayment.objects.get(user=request.user)
    except:
        job_to_post = None
    
    if response['data']['txref'] == current_profile.prof_ref and response['data']['status'] == 'successful':
        if response['data']['amount'] == 1345 and job_to_post is None:
            posted_job = JobPayment(user=current_user,job_post_paid=True)
            posted_job.save()
            messages.success(request, 'Payment has been confirmed.Post your job in the form below') 
            return redirect('post-job')

        elif response['data']['amount'] == 1345 and job_to_post is not None:
            job_to_post.user = current_user
            job_to_post.job_post_paid = True
            job_to_post.save()
            messages.success(request, 'Payment has been confirmed.Post your job in the form below') 
            return redirect('post-job')
        else:
            messages.success(request, 'Transaction has been initiated.Kindly wait for confirmation.') 
            return redirect('post-job-purchase')
    elif response['data']['acctmessage'] == 'The balance is insufficient for the transaction':
        messages.warning(request, 'Insufficient M-pesa balance.Kindly top up and try again.') 
        return redirect('post-job')
    else:
        messages.warning(request, 'Payment has been initiated.We will notify you when we have received the transaction.') 
        return redirect('post-job-purchase')



@login_required
def verify_business_transaction(request):
    current_user = request.user
    try:
        current_profile = Profile.objects.get(user=request.user)
    except:
        current_profile = None
    data = {
    "txref": current_profile.prof_ref, #this is the reference from the payment button response after customer paid.
    "SECKEY": "FLWSECK-c2a456efd68204aa7f2ee92d5ba61b55-X",
    }

    url = "https://api.ravepay.co/flwv3-pug/getpaidx/api/v2/verify"

    #make the http post request to our server with the parameters
    
    thread = requests.post(url, headers={"Content-Type":"application/json"}, data=json.dumps(data))
    # print(thread.json())
    response = thread.json()
    try:
        business_to_post = BusinessPromotePayment.objects.get(user=request.user)
    except:
        business_to_post = None

    if response['data']['txref'] == current_profile.prof_ref and response['data']['status'] == 'successful':
        if response['data']['amount'] == 1035 and business_to_post is None:
            posted_business = BusinessPromotePayment(user=current_user,business_post_paid=True)
            posted_business.save()
            messages.success(request, 'Payment has been confirmed.Promote your in the form below')
            return redirect('digital-media') 
        elif response['data']['amount'] == 1035 and business_to_post is not None:
            business_to_post.user = current_user
            business_to_post.business_post_paid = True
            business_to_post.save()
            messages.success(request, 'Payment has been confirmed.Promote your business in the form below')
            return redirect('digital-media') 
        else:
            messages.success(request, 'Transaction has been initiated.Kindly wait for confirmation.') 
            return redirect('digital-media')
    elif response['data']['acctmessage'] == 'The balance is insufficient for the transaction':
        messages.warning(request, 'Insufficient M-pesa balance.Kindly top up and try again.') 
        return redirect('digital-media')
    else:
        messages.warning(request, 'Payment has been initiated.We will notify you when we have received the transaction.') 
        return redirect('digital-job-purchase')
    

@login_required
def verify_business_renewal(request,pk):
    current_user = request.user
    try:
        current_profile = Profile.objects.get(user=request.user)
    except:
        current_profile = None
    data = {
    "txref": current_profile.prof_ref, #this is the reference from the payment button response after customer paid.
    "SECKEY": "FLWSECK-c2a456efd68204aa7f2ee92d5ba61b55-X",
    }

    url = "https://api.ravepay.co/flwv3-pug/getpaidx/api/v2/verify"

    #make the http post request to our server with the parameters
    
    thread = requests.post(url, headers={"Content-Type":"application/json"}, data=json.dumps(data))
    # print(thread.json())
    response = thread.json()
    next_renewal = timezone.now()+timedelta(days=30)
          
    try:
        business_to_renew = MerchantPromote.objects.get(id=pk)
    except:
        business_to_renew = None
    
    if response['data']['txref'] == current_profile.prof_ref and response['data']['status'] == 'successful':
        if response['data']['amount'] == 535 and business_to_renew is not None:
            business_to_renew.expiry_date = next_renewal
            business_to_renew.save()
            messages.warning(request, 'Payment has been confirmed.The renewal is valid for the next 1 month.') 
            return redirect('promoted-business-user',request.user.username)
        else:
            messages.warning(request, 'Payment has been initiated.Kindly wait for confirmation.') 
            return redirect('promoted-business-user',request.user.username)

    elif response['data']['acctmessage'] == 'The balance is insufficient for the transaction':
        messages.warning(request, 'Insufficient M-pesa balance.Kindly top up and try again.') 
        return redirect('promoted-business-user',request.user.username)
    else:
        messages.warning(request, 'Payment has been initiated.We will notify you when we have received the transaction.') 
        return redirect('confirm-business-renewal',business_to_renew.id)




@login_required
def verify_skill_transaction(request):
    current_user = request.user
    try:
        current_profile = Profile.objects.get(user=request.user)
    except:
        current_profile = None
    data = {
    "txref": current_profile.prof_ref, #this is the reference from the payment button response after customer paid.
    "SECKEY": "FLWSECK-c2a456efd68204aa7f2ee92d5ba61b55-X",
    }

    url = "https://api.ravepay.co/flwv3-pug/getpaidx/api/v2/verify"

    #make the http post request to our server with the parameters
    
    thread = requests.post(url, headers={"Content-Type":"application/json"}, data=json.dumps(data))
    # print(thread.json())
    response = thread.json()
    try:
        skill_to_post = SkillPromotePayment.objects.get(user=request.user)
    except:
        skill_to_post = None


    if response['data']['txref'] == current_profile.prof_ref and response['data']['status'] == 'successful':
        if response['data']['amount'] == 1035 and skill_to_post is None:
            posted_skill = SkillPromotePayment(user=current_user,skill_post_paid=True)
            posted_skill.save()
            messages.success(request, 'Payment has been confirmed.Promote your skill in the form below')
            return redirect('freelance-skill-post') 
        elif response['data']['amount'] == 1035 and skill_to_post is not None:
            skill_to_post.user = current_user
            skill_to_post.skill_post_paid = True
            skill_to_post.save()
            messages.success(request, 'Payment has been confirmed.Promote your skill in the form below')
            return redirect('freelance-skill-post') 
        else:
            messages.success(request, 'Transaction has been initiated.Kindly wait for confirmation.') 
            return redirect('freelance-skill-post')
    elif response['data']['acctmessage'] == 'The balance is insufficient for the transaction':
        messages.warning(request, 'Insufficient M-pesa balance.Kindly top up and try again.') 
        return redirect('freelance-skill-post')
    else:
        messages.warning(request, 'Payment has been initiated.We will notify you when we have received the transaction.') 
        return redirect('freelance-skill-purchase')
    


@login_required
def verify_skill_renewal(request,pk):
    current_user = request.user
    try:
        current_profile = Profile.objects.get(user=request.user)
    except:
        current_profile = None
    data = {
    "txref": current_profile.prof_ref, #this is the reference from the payment button response after customer paid.
    "SECKEY": "FLWSECK-c2a456efd68204aa7f2ee92d5ba61b55-X",
    }

    url = "https://api.ravepay.co/flwv3-pug/getpaidx/api/v2/verify"

    #make the http post request to our server with the parameters
    
    thread = requests.post(url, headers={"Content-Type":"application/json"}, data=json.dumps(data))
    # print(thread.json())
    response = thread.json()
    next_renewal = timezone.now()+timedelta(days=30)
    try:
        skill_to_renew = FreelanceSkills.objects.get(id=pk)
    except:
        skill_to_renew = None
    
    if response['data']['txref'] == current_profile.prof_ref and response['data']['status'] == 'successful':
        if response['data']['amount'] == 535 and skill_to_renew is not None:
            skill_to_renew.expiry_date = next_renewal
            skill_to_renew.save()
            messages.warning(request, 'Payment has been confirmed.The renewal is valid for the next 1 month.') 
            return redirect('promoted-skill-user',request.user.username)
        else:
            messages.warning(request, 'Payment has been initiated.Kindly wait for confirmation.') 
            return redirect('promoted-skill-user',request.user.username)
    elif response['data']['acctmessage'] == 'The balance is insufficient for the transaction':
        messages.warning(request, 'Insufficient M-pesa balance.Kindly top up and try again.') 
        return redirect('promoted-skill-user',request.user.username)
    else:
        messages.warning(request, 'Payment has been initiated.We will notify you when we have received the transaction.') 
        return redirect('confirm-skill-renewal',skill_to_renew.id)








