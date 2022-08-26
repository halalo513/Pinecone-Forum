// 通过ajax向后台传递个人信息修改数据
function bindAlterBasicInfoBtnClick(){
     var $this=$(this);
    $("#alter_btn").on("click", function (event) {
        var new_username=$("input[name='new_username']").val();
        var new_password=$("input[name='new_password']").val();
        var new_signature=document.getElementById('new_signature').value;
        $.ajax(
            {
                url:"/alter_basic_info/",
                method:"POST",
                data:{
                    "new_username":new_username,
                    "new_password":new_password,
                    "new_signature":new_signature
                },
                success: function (res) {
                    var code=res['code'];
                    if (code==200){
                        $this.off("click");
                        alert(res['message']);
                    }else{
                        alert(res['message']);
                    }

                }
            }
        )
    });
}
$(function () {
        bindAlterBasicInfoBtnClick();
    }
);