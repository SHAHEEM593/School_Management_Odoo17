/** @odoo-module */
import PublicWidget from "@web/legacy/js/public/public_widget";

    PublicWidget.registry.NewLeaveForm = PublicWidget.Widget.extend({

        selector: "#end_date",
        events:{
            'change':"_Total_Days",
        },
        _Total_Days: function(tot){
        var d1 = $("#start_date").val();
        var d2 = $("#end_date").val();
        var startDate = new Date(d1);
        var endDate = new Date(d2);
        const dayArray = [];
        for (
          let date = startDate;
          date <= endDate;
          date.setDate(date.getDate() + 1)
        )
        {
          dayArray.push(new Date(date).getDay());
        }

        var len = []
         for (var i in dayArray){
            if(dayArray[i]!=0 && dayArray[i]!=6){

                  len.push(dayArray[i])

            }
        }
        var total_day = len.length
        $('#total_days').val(total_day)

        }

 });




