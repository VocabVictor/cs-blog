$(function () {
    $('.recent_posts .recent_post:first-child').addClass('active');
    $('.blog-slider__pagination .swiper-pagination-bullet:first-child').addClass('active');

    //设置循环轮播的时间间隔为5000毫秒
    var intervalId_recent_posts = setInterval(function(){
        var current = $('.recent_post.active'),
            bullets = $('.swiper-pagination-bullet.active'),
            recent_posts = $('.recent_post'),
            bullets_all = $('.swiper-pagination-bullet');
        if(current.next('.recent_post').length != 0){
            current.removeClass('active');
            bullets.removeClass('active');
            current.next('.recent_post').addClass('active');
            bullets.next('.swiper-pagination-bullet').addClass('active');
        }else{
            current.removeClass('active');
            bullets.removeClass('active');
            recent_posts.first().addClass('active');
            bullets_all.first().addClass('active');
        }
    }, 5000);

});



// $('.recent_posts').on('mousewheel', function(e){
//     e.preventDefault();
//     var current = $('.recent_post.active'),
//         bullets = $('.swiper-pagination-bullet.active'),
//         recent_posts = $('.recent_post'),
//         bullets_all = $('.swiper-pagination-bullet');
//     if(e.originalEvent.wheelDelta /120 > 0) {
//         //向上滚动
//         if(current.prev('.recent_post').length != 0){
//             current.removeClass('active');
//             bullets.removeClass('active');
//             current.prev('.recent_post').addClass('active');
//             bullets.prev('.swiper-pagination-bullet').addClass('active');
//         }else{
//             current.removeClass('active');
//             bullets.removeClass('active');
//             recent_posts.last().addClass('active');
//             bullets_all.last().addClass('active');
//         }
//     }
//     else{
//         //向下滚动
//         if(current.next('.recent_post').length != 0){
//             current.removeClass('active');
//             bullets.removeClass('active');
//             current.next('.recent_post').addClass('active');
//             bullets.next('.swiper-pagination-bullet').addClass('active');
//         }else{
//             current.removeClass('active');
//             bullets.removeClass('active');
//             recent_posts.first().addClass('active');
//             bullets_all.first().addClass('active');
//         }
//     }
// });
