from django.urls import path, re_path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    HomePageView,profile_dashboard,jobs,bid_job,token_low,token_medium,token_high,token_purchase,signin,signup,signout,pagenotfound,sort_price_highest,messaging_dashboard
    )

urlpatterns = [
    path('',HomePageView.as_view(),name='home'),
    path('signup/', signup, name="signup"),
    path('accounts/login/', signin, name="login"),
    path('signout/',signout, name="signout"),
    path('dashboard/<slug>/',profile_dashboard,name='profile-dashboard'),
    path('jobs/SORT=new/',jobs,name='job-page'),
    path('jobs/SORT=pay/',sort_price_highest,name='job-sort'),
    path('j/<slug>',bid_job,name='bid-job'),
    path('token-3/payment',token_low,name='token-low'),
    path('token-5/payment',token_medium,name='token-medium'),
    path('token-7/payment',token_high,name='token-high'),
    path('tokenpurchase/',token_purchase,name='token-purchase'),
    path('404pagenotfound/',pagenotfound,name='404page')
]
