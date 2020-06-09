from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    HomePageView,profile_dashboard,jobs,bid_job,
    signup,
    pagenotfound,sort_price_highest,messaging_dashboard,
    register_urls,confirmation,validation,call_back,
    check_transaction,token_purchase,low_purchase,medium_purchase,high_purchase,
    post_job,post_job_purchase,work_place,post_digital_job,digital_job_purchase,
    post_job_transaction,promote_business_transaction,
    received_quotes,posted_job_user,sent_quotes,

    #Sorted jobs for users to view
    sort_software_jobs,sort_product_jobs,sort_marketing_jobs,
    sort_writing_jobs,sort_customer_service_jobs,sort_referral_jobs,
    sort_data_entry_jobs,sort_other_unspecified_jobs,
   
    all_promoted_business,promoted_business_user,renew_business_transaction,

    all_promoted_skills,freelance_skills_post,promoted_skill_user, freelance_skill_purchase,renew_skill_transaction,promote_skill_transaction,

    eclid_digital_nomad,terms_conditions
  

    

    )

urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('signup/', signup, name="signup"),
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
    path('subscription/45<int:pk>3/business/transaction',renew_business_transaction,name='renew-business-transaction'), #This validates the transaction

   

  
    #Url for freelancer to advertise their skills with a form
    path('posted/skills/<slug>',promoted_skill_user,name='promoted-skill-user'),
    path('skill/post',freelance_skills_post,name='freelance-skill-post'),
    path('promote/skill/purchase',freelance_skill_purchase,name='freelance-skill-purchase'),
    path('renew/skill/transaction/17<int:pk>8',renew_skill_transaction,name='check-skill-renewal-transaction'),
    path('promoted/skills',all_promoted_skills,name='promoted-skills'),
    path('promote/skill/transaction',promote_skill_transaction,name='check-skill-post-transaction'),
    #url for social media adverts/jobs and promote businesses
    path('myworkplace/',work_place,name='work-place'),
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
    path('buy/1',low_purchase,name='token-low'),
    path('buy/2',medium_purchase,name='token-medium'),
    path('buy/3',high_purchase,name='token-high'),

    path('404pagenotfound/',pagenotfound,name='404page'),
    path('terms&conditions',terms_conditions,name='terms-conditions'),

    #url for checking the three transactions have occured succcesfully or are invalid
    path('validate/',check_transaction,name='validate-transaction'),
    path('validate/transaction',post_job_transaction,name='post-job-transaction'),
    path('validate/transact',promote_business_transaction,name='promote-business-transaction'),

    #url for mpesa API 
    # register, confirmation, validation and callback urls
    path('c2b/register',register_urls, name="register_mpesa_validation"),
    path('confirmation/',confirmation, name="confirmation"),
    path('validation/',validation, name="validation"),
    path('callback/',call_back, name="call_back"),
]
