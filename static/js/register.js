function binCaptchaClick() {
    $("#captcha-btn").on("click", function (event) {
        var $this = $(this);  // 定义一个变量等于$("#captcha-btn")对象, 方便后续调用
        var email = $("input[name='email']").val();
        if (!email) {    // 判断邮箱是否为空
            alert("请先输入邮箱")
            return;
        }
        // 通过js发送网络请求: ajax
        $.ajax({
            url: "/user/captcha",
            method: "POST",
            data: {
                "email": email
            },
            success: function (res) {
                var code = res['code'];
                if (code === 200) {
                    $this.off("click")   // 取消点击时间
                    var countDown = 60;
                    var timer = setInterval(function () {
                        countDown -= 1;
                        if (countDown > 0) {
                            $this.text(countDown + "秒后重新发送");
                        } else {
                            $this.text("获取验证码");
                            binCaptchaClick();  // 重新执行函数，重新绑定事件
                            clearInterval(timer);    // 清除倒计时, 否则会一直执行
                        }
                    }, 1000);
                    alert("验证码发送成功");
                } else {
                    alert(res['message']);
                }
            }
        })
    });
}


$(function () {
    binCaptchaClick();
});
