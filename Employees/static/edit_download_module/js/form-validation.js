// this is for form submit action
$.validator.setDefaults( {
   debug: false,
   submitHandler: function () {
      alert( "submitted!" );
   }
} );

// this is for form validation
$( document ).ready( function () {
   $('#editProfileForm').validate({
      rules: {
         firstName: 'required',
         lastName: 'required',
         userId: {
            required: true,
            digits: true
         },
         
         aboutBio:{
            required: true,
            maxlength: 280,
         },
         websiteLink:{
            required: true,
            url: true,
         },
         email1: {
            required: true,
            email: true,
         },
         phoneInput: {
            required: true,
         },
         //conection details 
         fbLink: {
            url: true,
         },
         insLink: {
            url: true,
         },
         snapLink: {
            url: true,
         },
         linkdInLink: {
            url: true,
         },
         twiLink: {
            url: true,
         },
         tumblerLink: {
            url: true,
         },
         dribbleLink:{
            url: true,
         },
         behanceLink:{
            url: true,
         },
         pinLink:{
            url: true,
         },
         youtubeLink:{
            url: true,
         },
         teleGranLink:{
            url: true,
         },
         reditlink:{
            url: true,
         },
         // aditional form validation
         emailadi1:{
            email: true,
         },
         emailadi2:{
            email: true,
         },
         emailadi3:{
            email: true,
         },
         webLinkadi1:{
            url: true,
         },
         webLinkadi2:{
            url: true,
         },
         webLinkadi3:{
            url: true,
         },






      },
      messages: {
         firstName: 'Mandatory fields cannot be empty',
         lastName: 'Mandatory fields cannot be empty',
         userId:{
            required: 'Mandatory fields cannot be empty',
            digits: 'Please enter a valid USER ID',
         },
         aboutBio:{
            required: 'Mandatory fields cannot be empty',
            maxlength: "You've exceeded the character limit by {280}."
         },
         websiteLink: {
            required: 'Mandatory fields cannot be empty',
            url: 'Please enter a valid web address'
         },
         email1: {
            required: 'Mandatory fields cannot be empty',
            email: 'Please enter a valid email address'
         },
         phoneInput : 'Mandatory fields cannot be empty',
      },
   });


   // custom inputtype file image validation 
   $( document ).ready( function () {

      // preview image function
      function readURL(input) {
         if (input.files && input.files[0]) {
           var reader = new FileReader();
           
           reader.onload = function(e) {
             $('#profileViewImage').attr('src', e.target.result);
           }
           
           reader.readAsDataURL(input.files[0]); // convert to base64 string
         }
       }



      $('#profileImage').on('change',function(e){
         var val = $(this).val();
         var fileName = e.target.files[0].name;
         switch(val.substring(val.lastIndexOf('.') + 1).toLowerCase()){
            case 'gif': case 'jpg': case 'png':
               $('#ProfileError').html('')
               readURL(this);
               $('.profileImageFileNme').html(fileName);
               break;
            default:
            $(this).val('');
            // error message herr
            $('#ProfileError').html('Please select a valid .jpeg/.jpg./png file');
            break;
        }






      })
   });





















})