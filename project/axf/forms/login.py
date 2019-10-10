#coding=utf-8
#@Time      :2019/10/2 20:42
#@Author    :QQC
#@Email     :sekikishuo@gmail.com
#@File      :login.py
#@Software  :PyCharm


from django import forms
# from ..models import



class LoginForm(forms.Form):
    #required 必要要填，不能为空
    username = forms.CharField(max_length=12, min_length=6, required=True, error_messages={"required":"用户账号不能为空", "invalid":"格式错误"},widget=forms.TextInput(attrs={"class":"c"}))
    # passwordInput 密文类
    passwd = forms.CharField(max_length=16, min_length=6, widget=forms.PasswordInput)


# class registerForm(forms.Form):
#     class Meta:
#         model =