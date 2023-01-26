$(document).ready(function() {
    $("#id_teacher").change(function () {
        var url = $("#themeForm").attr("data-themes-url");  
        var teacherId = $(this).val();  
    
        $.ajax({                      
          url: url,                    
          data: {
            'teacher': teacherId       
          },
          success: function (data) {  
            $("#id_theme").html(data);  
          }
        });
    
      });
});
