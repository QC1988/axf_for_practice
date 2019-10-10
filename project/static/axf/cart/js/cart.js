$(document).ready(function () {
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
                    document.getElementById(pid+"price").innerHTML = data.price

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
                    // console.log(data.data)
                    document.getElementById(pid).innerHTML = data.data
                    document.getElementById(pid+"price").innerHTML = data.price
                    if(data.data ==0){
                        // window.location.href =
                        var li = document.getElementById(pid+"li")
                        li.parentNode.removeChild(li)
                    }
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
    var ischoses = document.getElementsByClassName("ischose")
    for (var j=0;j<ischoses.length;j++){

        ischose = ischoses[j]
        ischose.addEventListener("click", function () {
            pid = this.getAttribute("goodsid")
            // console.log(pid)
            $.post("/changecart/2/", {"productid":pid}, function (data) {
                if (data.status=="success"){
                    if (data.data){
                        document.getElementById(pid+"a").innerHTML = "√"
                    }else{
                        document.getElementById(pid+"a").innerHTML = ""
                    }


                        // document.getElementById(pid+"a").innerHTML = data.data
                        // console.log(data.data)
                    // window.location.href ="http://127.0.0.1:8000/login/"
                    // $(this).load()
                }
            })
        })
    }



    var ok = document.getElementById("ok")
    ok.addEventListener("click", function () {
        var f = confirm("确认下单？")
        if (f){
            $.post("/saveorder/", function (data) {
                if (data.status == "success"){
                    console.log("********")
                    window.location.href ="http://127.0.0.1:8000/cart/"
                    // console.log("********")
                }
                else if (data.status == "error" && data.data == -3){
                    alert("未选择商品")
                }

            })


        }
    },false)
})