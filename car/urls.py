
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.sign_in, name="sign_in"),
    path('home',views.home,name="home"),
    path('add_car',views.add_car,name="add_car"),
    path('thankyou',views.thankyou,name="thankyou"),
    path('get_email/<int:car_id>', views.send_mail, name="get_email"),
    path('logout', views.logout, name="logout"),
    path('register', views.new_user_registrion, name="register"),
    path('make_available/<int:car_id>', views.make_available, name="make_available"),


]
