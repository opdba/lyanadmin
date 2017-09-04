(function(jq){
	function ErrorMessage(container,msg){
		$error = container.find("label[class='error']");
		$error.text(msg);
		$error.parent().parent().css("display","inline-block")

	}

	function EmptyError(ths){
		$error = ths.find("label[class='error']");//找到class='error'的label标签
		if($error.length>0){//如果已经显示，移除该div
			var remove_div=ths.find("div[class='err-popover-out']");
			remove_div.remove();
		}
	}
    jq.extend({
        'login':function(form){
            $(form).find(':submit').click(function(){
				var flag = true;
				$(form).find('#username,#password').each(function(){

					var name = $(this).attr('name');
					var label = $(this).attr('label');
					var val = $(this).val();
					var ths = $(this).parent();
					console.log(name,label);
					var required = $(this).attr('require');//需要验证才有require属性
					if(required){
						if(!val || val.trim() == ''){
							flag = false;
							ErrorMessage(ths,label+'不能为空.');
							return false;
						}
					}
					EmptyError(ths);
				});
				return flag;
			});
        },
		'register':function(form){
			$(form).find(':submit').click(function(){
				var flag = true;
				$(form).find(':text,:password').each(function(){
					var name = $(this).attr('name');
					var label = $(this).attr('label');
					var val = $(this).val();
					var ths = $(this).parent();

					var required = $(this).attr('require');//需要验证才有require属性
					if(required){
						if(!val || val.trim() == ''){
							flag = false;
							ErrorMessage(ths,label+'不能为空.');
							return false;
						}
					}
					//手机号码格式验证
					var mobile = $(this).attr('mobile');
					if(mobile){
						var reg = /^1[3|5|8]\d{9}$/;
						if(!reg.test(val)){
							flag = false;
							ErrorMessage(ths,label+'格式错误.');
							return false;
						}
					}
					//用户名验证
					var field = $(this).attr('Field');
					if(field=='string'){
						var reg = /^\w+$/;
						if(!reg.test(val)){
							flag = false;
							ErrorMessage(ths,label+'只能由英文、数字及"_"组成.');
							return false;
						}
					}
					//两次密码是否一致
					var confirm_to = $(this).attr('pwd_to');
					if(confirm_to){
						var pwd = $(form).find("input[name='pwd']");
						if(pwd.val().trim()!=val.trim()){
							flag = false;
							ErrorMessage(ths,'两次密码输入不一致.');
							return false;
						}
					}
					//密码最小长度
					var min = $(this).attr('min_len');
					if(min){
						var len = parseInt(min);
						if(val.length<len){
							flag = false;
							ErrorMessage(ths,label+'最小长度为'+min+'.');
							return false;
						}
					}
					EmptyError(ths);
				});
				return flag;
			});
		}
    })
})(jQuery);