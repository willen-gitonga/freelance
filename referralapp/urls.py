from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    HomePageView,profile_dashboard,jobs,
    bid_job,signin,signup,signout,
    pagenotfound,sort_price_highest,messaging_dashboard,
    register_urls,confirmation,validation,call_back,
    check_transaction,token_purchase,low_purchase,medium_purchase,high_purchase,
    post_job,post_job_purchase,work_place,post_digital_job,digital_job_purchase,
    post_job_transaction,promote_business_transaction
    )

urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('signup/', signup, name="signup"),
    path('signin/', signin, name="signin"),
    path('signout/',signout, name="signout"),
    path('dashboard/<slug>/',profile_dashboard,name='profile-dashboard'),
    path('jobs/SORT=new/',jobs,name='job-page'),
    path('jobs/SORT=pay/',sort_price_highest,name='job-sort'),
    path('j/<slug>',bid_job,name='bid-job'),
    #url for social media adverts/jobs
    path('myworkplace/',work_place,name='work-place'),
    path('promote/post',post_digital_job,name='digital-media'),
    path('promote/validate',digital_job_purchase,name='digital-job-purchase'),
    #url for posting normal jobs
    path('job/post',post_job,name='post-job'), #url for posting jobs
    path('post/validate',post_job_purchase,name='post-job-purchase'), #url for normal job payment
    #url for buying tokens for freelancers
    path('buy/tokens',token_purchase,name='token-purchase'),
    path('buy/1',low_purchase,name='token-low'),
    path('buy/2',medium_purchase,name='token-medium'),
    path('buy/3',high_purchase,name='token-high'),

    path('404pagenotfound/',pagenotfound,name='404page'),
    #url for checking the three transactions that occur
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
