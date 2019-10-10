#coding=utf-8
#@Time      :2019/9/28 21:53
#@Author    :QQC
#@Email     :sekikishuo@gmail.com
#@File      :urls.py.py
#@Software  :PyCharm


from django.contrib import admin
from django.urls import path, re_path
from . import views

app_name = "axf"

urlpatterns = [
    re_path('^home/$', views.home, name="home"),
    re_path('^market/(\d+)/(\d+)/(\d+)/$', views.market, name="market"),
    re_path('^cart/$', views.cart, name="cart"),

    # 修改购物车

    re_path('^changecart/(\d+)/$', views.changecart, name="changecart"),

    re_path('^mine/$', views.mine, name="mine"),
    #登录
    re_path('^login/$', views.login, name="login"),
    # 注册
    re_path('^register/$', views.register, name="register"),
    #验证账号是否被注册
    re_path('^checkuserid/$', views.checkuserid, name="checkuserid"),
    # 退出登录
    re_path('^quit/$', views.quit, name="quit"),
    # 下订单
    re_path('^saveorder/$', views.saveorder, name="saveorder"),

]
