$(document).ready(function () {
    var alltypebtn = document.getElementById("alltypebtn")
    var showsortbtn = document.getElementById("showsortbtn")

    var typediv = document.getElementById("typediv")
    var sortdiv = document.getElementById("sortdiv")

    typediv.style.display = "none"
    sortdiv.style.display = "none"


    alltypebtn.addEventListener("click", function () {
        typediv.style.display = "block"
        sortdiv.style.display= "none"
    },false)
    showsortbtn.addEventListener("click", function () {
        typediv.style.display = "none"
        sortdiv.style.display= "block"
    },false)

    typediv.addEventListener("click", function () {
        typediv.style.display = "none"
    },false)
    sortdiv.addEventListener("click", function () {
        sortdiv.style.display = "none"
    },false)


    // 修改购物车
    var addShoppings = document.getElementsByClassName("addShopping")
    var subShoppings = document.getElementsByClassName("subShopping")

    for (var i = 0; i < addShoppings.length; i++){
        addShopping = addShoppings[i]
        addShopping.addEventListener("click", function () {
            pid = this.getAttribute("ga")
            $.post("/changecart/0/", {"productid":pid}, function (data) {
                if (data.status=="success"){
                    // 添加成功，把中间的Span的InnerHtml变成当前的数据
                    document.getElementById(pid).innerHTML = data.data
                }else {
                    if(data.data == -1){
                        // console.log("$$$$$$$$$$$$$$$")
                        // $.get("/login")
                        window.location.href = "http://127.0.0.1:8000/login/"
                    }
                }
            })
        })
    }

    // 闪送超市页：1当选中数量大于1时，出现“-”按钮；2当选中数量为零时，“-”按钮消失

    for (var i = 0; i < subShoppings.length; i++){
        subShopping = subShoppings[i]
        subShopping.addEventListener("click", function () {
            pid = this.getAttribute("ga")
            $.post("/changecart/1/", {"productid":pid}, function (data) {
                if (data.status=="success"){
                    // 添加成功，把中间的Span的InnerHtml变成当前的数据
                    document.getElementById(pid).innerHTML = data.data
                }else {
                    if (data.data == -1){
                        // $.get('/login/')
                        // 写死，直接回那个地址
                        window.location.href ="http://127.0.0.1:8000/login/"
                    }
                }
            })
        })
    }

})