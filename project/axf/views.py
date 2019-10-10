from django.shortcuts import render, redirect

import time
import random
from django.conf import settings
import os

# Create your views here.

from .models import Wheel, Nav, MustBuy, Shop, FoodTypes, Goods, User, Cart, CartManager1, CartManager2
def home(request):
    wheelsList = Wheel.objects.all()
    navList = Nav.objects.all()
    mustbuyList = MustBuy.objects.all()
    shopList = Shop.objects.all()
    # shop1 = Shop.objects.all().filter(id=1)
    # shop2 = Shop.objects.all().filter(id=[2, 3, 4, 5])
    # shop3 = Shop.objects.all().filter(id=[6, 7, 8, 9])
    # shop4 = Shop.objects.all().filter(id=[10, 11])
    shop1 = shopList[0]
    shop2 = shopList[1:3]
    shop3 = shopList[3:7]
    shop4 = shopList[7:11]


    return render(request, 'axf/home.html', {"title":"主页",
                                             "wheelsList":wheelsList,
                                             "navList":navList,
                                             "mustbuyList":mustbuyList,
                                             "shop1": shop1,
                                             "shop2": shop2,
                                             "shop3": shop3,
                                             "shop4": shop4,
                                             })

def market(request, categoryid, cid, sortid):
    leftSliderList = FoodTypes.objects.all()

    if cid == '0':
        productList = Goods.objects.filter(categoryid=categoryid)
    else:
        productList = Goods.objects.filter(childcid=cid, categoryid=categoryid)

    # 排序
    if sortid == "1":
        productList = productList.order_by("productnum")
    elif sortid == "2":
        productList = productList.order_by("price")
    elif sortid == "3":
        productList = productList.order_by("-price")

    cartList = Cart.objects.all()
    group = leftSliderList.get(typeid=categoryid)
    childList = []
    childnames = group.childtypenames
    arr1 = childnames.split('#')
    flag = 0
    for str in arr1:
    #  全部分类：0
        arr2 = str.split(":")
        obj = {"childName":arr2[0], "childId":arr2[1]}
        childList.append(obj)


    cartList = []
    token = request.session.get("token")
    if token :
        user = User.objects.get(userToken=token)
        cartList = Cart.objects.filter(userAccount=user.userAccount)

        for p in productList:
            for c in cartList:
                if c.productid == p.productid:
                    p.num = c.productnum
                    continue


    # cartlistnum = len(cartList)

    return render(request, 'axf/market.html', {"title":"闪送超市",
                                               "leftSlider":leftSliderList,
                                               "productList":productList,
                                               "childList":childList,
                                               "childName":childnames,
                                               "categoryid":categoryid,
                                               "cid":cid,
                                               "cartList":cartList,
                                               # "cartlistnum":cartlistnum,
                                               "flag":flag,
                                               })

def cart(request):
    cartslist = []
    # 判断用户是否登录
    token = request.session.get("token")
    if token != None:
        #登录
        user = User.objects.get(userToken=token)
        cartslist = Cart.objects.filter(userAccount=user.userAccount)
    return render(request, 'axf/cart.html', {"title":"购物车","cartslist":cartslist})

# 修改购物车
def changecart(request, flag):
    # 判断用户是否登录
    token = request.session.get("token")
    if token == None:
        #没登录
        return JsonResponse({"data":-1, "status":"error"})
    else:
        pass

    productid = request.POST.get('productid')


    product = Goods.objects.get(productid=productid)
    # product = Goods.objects.get(productid)
    user = User.objects.get(userToken=token)


    if flag =='0':
        if product.storenums == 0:
            return JsonResponse({"data": -2, "status": "error"})
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = None
        if carts.count() == 0:
            # 直接增加一条订单
            c = Cart.createcart(user.userAccount, productid, 1, product.price, True, product.productimg, product.productlongname, False)
            c.save()
            pass
        else:
            try:
                c = carts.get(productid=productid)
                # 修改数量和价格
                c.productnum += 1
                c.productprice = "%.2f"%(float(product.price) * c.productnum)
                c.save()
            except Cart.DoesNotExist as e:
                c = Cart.createcart(user.userAccount, product.productid, 1, product.price, True, product.productimg,
                                    product.productlongname, False)
                c.save()
        # 库存减一
        product.storenums -= 1
        product.save()
        return JsonResponse({"data":c.productnum, "price":c.productprice,"status":"success"})

    elif flag =='1':
        # print("减一条订单")
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = None
        if carts.count() == 0:
            # 直接增加一条订单
            # c = Cart.createcart(user.userAccount, productid, 1, product.price, True, product.productimg, product.productlongname, False)
            # c.save()
            # pass
            return JsonResponse({"data":-2, "status":"error"})
        else:
            try:
                c = carts.get(productid=productid)
                # 修改数量和价格
                c.productnum -= 1
                c.productprice = "%.2f"%(float(product.price) * c.productnum)
                if c.productnum==0:
                    c.delete()
                else:
                    c.save()
            except Cart.DoesNotExist as e:
                # c = Cart.createcart(user.userAccount, product.productid, 1, product.price, True, product.productimg,
                #                     product.productlongname, False)
                # c.save()
                return JsonResponse({"data": -2, "status": "error"})
        # 库存加一
        product.storenums += 1
        product.save()
        return JsonResponse({"data": c.productnum,"price":c.productprice, "status": "success"})

    elif flag =='2':
        # print("view")
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = carts.get(productid=productid)
        c.isChose = not c.isChose
        c.save()
        return JsonResponse({"data":c.isChose,"status" : "success"})


    # elif flag =='3':
    #     pass




def mine(request):

    username = request.session.get("username", "未登录")


    return render(request, 'axf/mine.html', {"title":"我的", "username":username})


from .forms.login import LoginForm
from django.http import  HttpResponse
def login(request):
    if request.method == "POST":
        f = LoginForm(request.POST)
        if f.is_valid():
            # 说明信息格式没问题，验证账号密码的正确性

            nameid = f.cleaned_data["username"]
            pswd = f.cleaned_data["passwd"]
            try:
                user =User.objects.get(userAccount=nameid)
                if user.userPasswd != pswd:
                   #错误信息
                    return redirect('/login/')
            except User.DoesNotExist as e:
                #错误信息
                return redirect('/login/')

            #登录成功
            token = time.time() + random.randrange(1, 1000000)
            user.userToken = str(token)
            user.save()
            request.session["username"] = user.userName
            request.session["token"] = user.userToken
            return redirect('/mine/')
        else:
            return render(request, 'axf/login.html', {"title": "登录", "error": "errors"})
    else:
        f = LoginForm()
        return render(request, 'axf/login.html', {"title":"登录", "form":f})


import time
import random
from django.conf import settings
import os


def register(request):
    if request.method == "POST":
        userAccount = request.POST.get("userAccount")
        userPasswd = request.POST.get("userPass")
        userName = request.POST.get("userName")
        userPhone = request.POST.get("userPhone")
        userAddress = request.POST.get("userAddress")
        userRank = 0
        token = time.time() + random.randrange(1, 1000000)
        userToken = str(token)

        # 图片
        f = request.FILES["userImg"]
        userImg = os.path.join(settings.MEDIA_ROOT, userAccount+".png")
        with open(userImg, "wb") as fp:
            for data in f.chunks():
                fp.write(data)
        user = User.createuser(userAccount, userPasswd, userName, userPhone, userAddress, userImg, userRank, userToken)
        user.save()
        return redirect('/mine/')


        request.session["username"] = userName
        request.session["token"] = userToken





    else:
        return render(request, 'axf/register.html', {"title":"注册"})

# 退出登录

from django.contrib.auth import logout
def quit(request):
    logout(request)
    return redirect('/mine/')



from django.http import JsonResponse
def checkuserid(request):
    userid = request.POST.get("userid")

    print("userid=", userid)
    try:
        uesr = User.objects.get(userAccount=userid)
        print("$$$$")
        return JsonResponse({"data":"该用户已经被注册", "status":"error"})
    except User.DoesNotExist as e:
        return JsonResponse({"data":"可以注册", "status":"success"})


from .models import Order
from datetime import datetime

def saveorder(request):
    token = request.session.get("token")
    if token != None:
        # 登录
        user = User.objects.get(userToken=token)
        carts = Cart.objects.filter(userAccount=user.userAccount, isChose=True)
        if carts.count() == 0:
            # 若返回"data":-3 弹出提示：未选择商品
            return JsonResponse({"data":-3, "status": "error"})
        # 订单表数据操作
        userid = user.userAccount
        neworderid = ""
        neworderid = str(userid)
        neworderid = neworderid + str(datetime.now())
        # print(type(neworderid))
        o = Order.createorder(neworderid, userid, progress=1)
        o.save()
        for cart in carts:
            # Order.progress:1 买完
            # 购物车表数据操作
            cart.orderid = o.orderid
            cart.isDelete = True
        # o.progress = 1
        # o.save()
            cart.save()
        return JsonResponse({"status":"success"})
    else:
        return JsonResponse({"data":-1, "status":"error"})