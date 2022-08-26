// 通过ajax向后台上传文件数据
function bindUploadBtnClick(){
     var $this=$(this);
    $("#upload_btn").on("click", function (event) {
        var $this=$(this);
        var formdata=new FormData();
        var upload_files=document.getElementById('upload_files');
        formdata.append('avatar',upload_files.files[0]);
        $.ajax(
            {
                url:"/upload_avatar/",
                method:"POST",
                data:formdata,
                processData:false,
                contentType:false,
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
        bindUploadBtnClick();
    }
);