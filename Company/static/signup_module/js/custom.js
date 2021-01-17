$(document).ready(function() {
    var school = $(window);
    var page = $('html, body');
    
    // this is all popup mpodel action
    $('#signupbtn-modal').on('click',function(){
       $('#signup-modal').modal('hide'); 
    })
    $('#demoPopupBtn').on('click',function(){
        $('#emailpopupmodal').modal('hide'); 
    })

    $('#signinmodal-btn').on('click',function(){
        $('#signup-modal').modal('hide'); 
    })


    $('.create-new-account-link a').on('click',function(){
        $('#signin-modal').modal('hide'); 
    })

    $('#forgotepass-modal-btn').on('click',function(){
        $('#signup-modal').modal('hide'); 
        $('#signin-modal').modal('hide'); 
    })

    $('#passfor-createnew').on('click',function(){
        $('#forgotpass-modal').modal('hide'); 
    })

    $('#passfor-signin').on('click',function(){
        $('#forgotpass-modal').modal('hide'); 
    })
    
    $('#login-forgote-pass').on('click',function(){
        $('#signin-modal').modal('hide'); 
    })

    $('#forgotepass-modal-btn2').on('click',function(){
        $('#signin-modal').modal('hide'); 
    })

    $('#set-passmodal-btn').on('click',function(){
        $('#forgotpass-modal').modal('hide'); 
    })
    



     // password revel function
    $('.passwordShowBtn.show').on('click',function(){
        var password = document.getElementById("passwordFild");
        if(password.type == 'password') {
            password.type = 'text';
            $(this).addClass('hide');
            $(this).removeClass('show');
        }
        else{
            password.type = 'password';
            $(this).addClass('show');
            $(this).removeClass('hide');
        }
    })

    $('.passwordShowBtn.show').on('click',function(){
        var password = document.getElementById("passwordFild2");
        if(password.type == 'password') {
            password.type = 'text';
            $(this).addClass('hide');
            $(this).removeClass('show');
        }
        else{
            password.type = 'password';
            $(this).addClass('show');
            $(this).removeClass('hide');
        }
    })

    $('.passwordShowBtn.show').on('click',function(){
        var password = document.getElementById("passwordFild3");
        if(password.type == 'password') {
            password.type = 'text';
            $(this).addClass('hide');
            $(this).removeClass('show');
        }
        else{
            password.type = 'password';
            $(this).addClass('show');
            $(this).removeClass('hide');
        }
    })

    $('.passwordShowBtn2.show').on('click',function(){
        var password = document.getElementById("passwordFild4");
        if(password.type == 'password') {
            password.type = 'text';
            $(this).addClass('hide');
            $(this).removeClass('show');
        }
        else{
            password.type = 'password';
            $(this).addClass('show');
            $(this).removeClass('hide');
        }
    })

    // start mobile menu toggle area
    $('.mobileHeadeToggle span').on('click',function(){
        $('#mobileHederContent').toggleClass('show');
    })

    $('.menuCLose').on('click',function(){
        $('#mobileHederContent').toggleClass('show');
    })





});