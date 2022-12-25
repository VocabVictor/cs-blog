// 我想要用jquery和canvas标签写一段星空代码，要求如下：
// 1. 无论星星如何动，最后都是以从左下到右上的方式离开屏幕。
// 2. 星星中有些为萤火，也就是慢慢的飘走；有些为流星，也就是快速飘走。
// 3. 90 % 的概率为萤火，10 % 概率为星星。
// 4. 流星要和彗星一样，有淡淡的彗星尾巴。
// 5. 星星的亮度要随机，星星的初始速度要随机。
// 6. 星星的颜色要和真实的星星的颜色一致
// 7. 星星数量固定，星星在屏幕消失的时候不要使用删除方法，这样会影响网页效率。
// 请不要解释，直接给出代码。
$(document).ready(function () {
    // 获取 canvas 元素和绘图上下文
    var canvas = $('#universe')[0];
    var ctx = canvas.getContext('2d');
    var width = canvas.width = window.innerWidth;
    var height = canvas.height = window.innerHeight;

    // 定义星星数量和大小
    var numStars = 250;
    var radius = 1;

    // 定义萤火和流星的概率
    var meteorProbability = 0.1;

    // 定义星星数组
    var stars = [];

    // 定义随机颜色数组
    var colors = ['#ffffff', '#ffe9c4', '#d4fbff'];

    // 随机生成星星
    for (var i = 0; i < numStars; i++) {
        var x = Math.random() * width;
        var y = Math.random() * height;
        var length = radius + Math.random() * radius;
        var opacity = Math.random();

        // 随机生成萤火或流星
        var type = 'star';
        if (Math.random() > meteorProbability) {
            type = 'meteor';
            // 随机生成星星初始速度
            var speed = Math.random() * 0.2;
        }
        else{
            type = "shoot"
            var speed = Math.random() * 1 +  1;
        }

        // 随机生成星星颜色
        var color = colors[Math.floor(Math.random() * colors.length)];

 

        stars.push({
            x: x,
            y: y,
            length: length,
            opacity: opacity,
            color: color,
            speed: speed,
            type: type
        });
    }

    // 绘制星星
    function draw() {
        ctx.clearRect(0, 0, width, height);

        for (var i = 0; i < numStars; i++) {
            // 获取当前星星
            var star = stars[i];

            // 绘制星星
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.length, 0, 2 * Math.PI, false);
            ctx.fillStyle = star.color;
            ctx.globalAlpha = star.opacity;
            ctx.fill();

            // 如果是流星，绘制彗星尾巴
            if (star.type == 'meteor') {
                ctx.beginPath();
                ctx.moveTo(star.x - star.length / 2, star.y - star.length / 2);
                ctx.lineTo(star.x - star.length / 2 - star.speed, star.y - star.length / 2 - star.speed);
                ctx.lineWidth = 2;
                ctx.strokeStyle = star.color;
                ctx.globalAlpha = star.opacity;
                ctx.stroke();
            }

            // 更新星星位置
            star.x += star.speed;
            star.y -= star.speed;

            // 如果星星移出屏幕，重置位置
            if (star.x > width) {
                star.x = 0;
                star.y = Math.random() * height;
            }
            if (star.y < 0) {
                star.x = Math.random() * width;
                star.y = height;
            }
        }

        // 循环绘制
        requestAnimationFrame(draw);
    }
    draw();
});