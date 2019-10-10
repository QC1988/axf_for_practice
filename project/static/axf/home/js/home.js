$(document).ready(function () {
    setTimeout(function () {
        swiper1()
        swiper2()
    },100)

})

function swiper1() {
    // 加载topSwiper，创建Swiper对象
    var mySwiper1 = new Swiper('#topSwiper', {
        // 方向
        direction: 'horizontal',
        // 是否循环轮播
        loop: true,
        speed: 500,
        // 切换的时间，图片停留时间
        autoplay: 2000,
        // 下面那个小圆点
        pagination: '.swiper-pagination',
        // 控制左右的控制器
        control: true,
    });
};

function swiper2() {
    // 加载topSwiper，创建Swiper对象
    var mySwiper2 = new Swiper('#swiperMenu', {
        // // 方向
        direction: 'horizontal',
        // 是否循环轮播
        // loop: true,
        speed: 500,
        // // 切换的时间，图片停留时间
        autoplay: 2000,
        // // 下面那个小圆点
        pagination: '.swiper-pagination',
        // // 控制左右的控制器
        // control: true,
        slidesPerView:3,
        paginationClickable:true,
        spaceBetween:2,
        loop:true,
    });
};
