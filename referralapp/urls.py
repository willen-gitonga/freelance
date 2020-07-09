from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    choose_service,
    pay_low_token,pay_medium_token,pay_high_token,verify_token_transaction,
    pay_business_promote,verify_business_transaction,pay_business_renewal,confirm_business_renewal,
    verify_business_renewal,
    pay_post_job,verify_job_transaction,
    pay_skill_promote,pay_skill_renewal,confirm_skill_renewal,verify_skill_renewal,verify_skill_transaction,
    HomePageView,profile_dashboard,jobs,bid_job,
    signup,
    pagenotfound,sort_price_highest,
    token_purchase,confirm_purchase,
    post_job,post_job_purchase,post_digital_job,digital_job_purchase,
    received_quotes,posted_job_user,sent_quotes,

    #Sorted jobs for users to view
    sort_software_jobs,sort_product_jobs,sort_marketing_jobs,
    sort_writing_jobs,sort_customer_service_jobs,sort_referral_jobs,
    sort_data_entry_jobs,sort_other_unspecified_jobs,
   
    all_promoted_business,promoted_business_user,

    all_promoted_skills,freelance_skills_post,promoted_skill_user, freelance_skill_purchase,

    eclid_digital_nomad,terms_conditions

    )

urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('signup/', signup, name="signup"),
    path('service/select',choose_service,name='choose-service'),
    path('dashboard/<slug>/',profile_dashboard,name='profile-dashboard'),
    path('jobs/SORT=new/',jobs,name='job-page'),
    path('jobs/SORT=pay/',sort_price_highest,name='job-sort'),
    path('j/34<int:pk>53/availablejobs',bid_job,name='bid-job'),

    #Sorted jobs for user 
    path('jobs/software-development',sort_software_jobs,name='sorted-software-jobs'),
    path('jobs/product-service',sort_product_jobs,name='sorted-product-jobs'),
    path('jobs/marketing',sort_marketing_jobs,name='sorted-marketing-jobs'),
    path('jobs/writing',sort_writing_jobs,name='sorted-writing-jobs'),
    path('jobs/customersevice',sort_customer_service_jobs,name='sorted-customer-service-jobs'),
    path('jobs/referralagent',sort_referral_jobs,name='sorted-referral-jobs'),
    path('jobs/dataentry',sort_data_entry_jobs,name='sorted-data-entry-jobs'),
    path('jobs/other',sort_other_unspecified_jobs,name='sorted-unspecified-jobs'),

    path('digitalnomad/',eclid_digital_nomad,name='digital-nomad'),
    #promoting businesses and freelance skills to all users to view
    path('promoted/businesses',all_promoted_business,name='promoted-businesses'),
 
    path('posted/business/<slug>',promoted_business_user,name='promoted-business-user'),

   

  
    #Url for freelancer to advertise their skills with a form
    path('posted/skills/<slug>',promoted_skill_user,name='promoted-skill-user'),
    path('skill/post',freelance_skills_post,name='freelance-skill-post'),
    path('promote/skill/purchase',freelance_skill_purchase,name='freelance-skill-purchase'),
    path('promoted/skills',all_promoted_skills,name='promoted-skills'),
    #url for social media adverts/jobs and promote businesses
    path('promote/post',post_digital_job,name='digital-media'),
    path('promote/validate',digital_job_purchase,name='digital-job-purchase'),
   
    #url for posting normal jobs
    path('job/post',post_job,name='post-job'), #url for posting jobs
    path('post/validate',post_job_purchase,name='post-job-purchase'), #url for normal job payment
    path('myposted/jobs',posted_job_user,name='posted-jobs-user'),

    path('quotes/received',received_quotes,name='received-quotes'),
    path('quotes/sent',sent_quotes,name='sent-quotes'),
    #url for buying tokens for freelancers
    path('buy/tokens',token_purchase,name='token-purchase'),
    path('confirm/payment',confirm_purchase,name='token-low'),
    

    path('404pagenotfound/',pagenotfound,name='404page'),
    path('terms&conditions',terms_conditions,name='terms-conditions'),

#These are the good payments
    path('rave/',pay_low_token,name='rave-low-pay'),
    path('rave/medium',pay_medium_token,name='rave-medium-pay'),
    path('rave/high',pay_high_token,name='rave-high-pay'),
    path('verify/rave',verify_token_transaction,name='verify-rave'),

# These are the transaction for the  jobs posted by client
    
    path('job/payment',pay_post_job,name='pay-post-job'),
    path('job/verify/payment',verify_job_transaction,name='verify-job-transaction'),


    path('skill/payment',pay_skill_promote,name='pay-skill-promote'),
    path('verify/skill/',verify_skill_transaction,name='verify-skill-transaction'),
    path('rave/skill/384<int:pk>/renewal',pay_skill_renewal,name='rave-skill-renewal'),
    path('skill/38<int:pk>43/renewal',verify_skill_renewal,name='verify-skill-renewal'),
    path('skill/38<int:pk>46/renew',confirm_skill_renewal,name='confirm-skill-renewal'),

    path('rave/business',pay_business_promote,name='rave-business-pay'),
    path('verify/business',verify_business_transaction,name='rave-business-verify'),
    path('rave/business/45<int:pk>3/renewal',pay_business_renewal,name='rave-business-renewal'),
    path('verify/business/45<int:pk>3/renewal',verify_business_renewal,name='verify-business-renewal'),
    path('business/45<int:pk>3/renew',confirm_business_renewal,name='confirm-business-renewal'),

]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)
