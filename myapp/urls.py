from django.urls import path
from myapp import views
app_name = 'myapp'
urlpatterns = \
    [
      path('', views.home , name='home'),
      path('about/', views.about, name='about'),
      path('products', views.products, name='products'),
      path('placeorder', views.place_order, name='place_order'),
      path('detail/<int:cat_no>/', views.detail, name='detail'),
      path('index0/', views.index0, name='index0'),
      path('<int:user_id>/', views.index, name='index'),
      path('products/<int:prod_id>/', views.productdetail, name='product_detail'),
      path('login', views.login, name='login'),
      path('user_login', views.user_login, name='userlogin'),
      path('myorders', views.myorders, name='myorders'),
      path('logout', views.user_logout, name='userlogout'),
      ]
