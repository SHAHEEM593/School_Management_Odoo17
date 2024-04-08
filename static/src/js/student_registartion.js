/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";

    PublicWidget.registry.NewStudentForm = PublicWidget.Widget.extend({
        selector: "#dob",
        events:{
            'change':"_onSubmitButton",
        },
        _onSubmitButton: function(evt){
        const date = new Date();
        var a = $('#dob').val()
        let day = date.getDate();
        let month = date.getMonth() + 1;
        let year = date.getFullYear();
        let currentDate = `${year}-${month}-${day}`;
        var age  = parseInt(currentDate) -  parseInt(a)

         var error = 0

        if( age > 1){
            $('#age').val(age);
            error = 0
        } else {
            alert("age should be positive");
            error  = 1
        }

        if(error == 1){

            $('#submit').attr('disabled', 'disabled')
        }
        if(error == 0){
             $('#submit').removeAttr('disabled')

        }
}
    });

