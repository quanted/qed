$(document).ready(function() {
            $(function() {
                $("#sortable").sortable();
                $("#sortable").disableSelection();
                $('#sortable').shuffle()
            });		

					
					$.validator.addMethod(
						"human",
						function() 
						{   
							return humantest()
						},
						"Please prove you are a human by draging the below numbers into order."
					)	
					
					function humantest() {
						var res = false;
						$('#sortable').each(function(){
							var arr = $('#sortable').children();
							res =  	((arr[0].innerHTML==1)&&
								(arr[1].innerHTML==2)&&
								(arr[2].innerHTML==3)&&
								(arr[3].innerHTML==4)&&
								(arr[4].innerHTML==5)&&
								(arr[5].innerHTML==6));
						});
						
						return res
					}	

		
					$("#form").validate({
					submitHandler:function(form) {
						SubmittingForm()
						},
					rules: {
						nm_name: "required",		
						nm_email:{required:true,
								  email:true
								},
						nm_sub:"required",
						nm_msg:{required:true,
								human:true
						}
						}
				})	
//				
//	$("#formsubmit").click(function(){
//		alert(humantest())
//	})
});