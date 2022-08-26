// 通过ajax向后台传递邮箱地址
function bindCaptchaBtnClick(){
    $("#captcha-btn").on("click", function (event) {
        var $this=$(this); // 获取$("#captcha-btn")
        var email = $("input[name='email']").val();
        if(!email){
            alert("请先输入邮箱!");
            return;
        }
        // 通过js发送网络请求：Ajax
        $.ajax({
            url:"/user/captcha/",
            method:'POST',
            data:{
                "email": email
            },
            success: function (res){
                var code = res['code'];
                if(code==200){
                    // 取消点击事件
                    $this.off("click");
                    // 开始倒计时
                    var countDown=60;
                    var timer=setInterval(function(){
                        countDown-=1;
                        if(countDown>0){
                            $this.text(countDown+"秒后重新发送");
                        }else{
                            $this.text("重新获取");
                            // 重新执行这个函数，绑定点击事件
                            bindCaptchaBtnClick();
                            // 清除倒计时，防止死循环
                            clearInterval(timer);
                        }

                    }, 1000);
                    alert("验证码发送成功");
                }else{
                    alert(res['message']);
                }
            }
        })


    });
}

// 等待网页元素都加载完成后再执行
$(function () {
        bindCaptchaBtnClick();
    }
);