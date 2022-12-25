// 颜色数组
var arr = ["#39c5bb", "#f14747", "#f1a247", "#f1ee47", "#b347f1", "#1edbff", "#ed709b", "#5636ed"];
// 颜色索引
var idx = 0;

// 切换颜色
function changeColor() {
    // 仅夜间模式才启用
    if ($('body').data('theme') === 'dark') {
        if (idx >= 8 ) {
            idx = 0;
        }
        // 遍历所有类名中包含 header、footer、title 的类，且不在 .page 内的标签
        $('[class*="header"], [class*="footer"], [class*="title"]').not('.page *').each(function() {
            $(this).css('text-shadow', arr[idx] + " 0 0 15px");
        });
        idx++;
    } else if( id <= 8 ){
        // 白天模式恢复默认
        $('[class*="header"], [class*="footer"], [class*="title"]').not('.page *').each(function() {
            $(this).css('text-shadow', "none");
        });
        id = 9;
    }
}

// 开启计时器
$(document).ready(function() {
  setInterval(changeColor, 1200);
});
