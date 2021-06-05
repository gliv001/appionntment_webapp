function Currency(num) {
    return `$${parseFloat(num).toFixed(2)}`
}

function RegenerateAppointmentTableFromJson(json_data) {
    if (!$('#appt-table').length) { // check table element exists, if not create it
        var table = $('<table>', {id: 'appt-table'});
        var header_row = $('<tr>');
        header_row.append($('<th>', {html: 'Client'}));
        header_row.append($('<th>', {html: 'Service'}));
        header_row.append($('<th>', {html: 'Employee'}));
        header_row.append($('<th>', {html: 'Appointment Date/Time'}));
        header_row.append($('<th>', {html: 'Tips'}));
        header_row.append($('<th>', {html: 'Total'}));
        header_row.append($('<th>', {html: 'Update?'}));
        table.append(header_row);
        table.insertAfter($('#empty-table-placeholder'));
        $('#empty-table-placeholder').remove()
    }
    else {
        $('#appt-table').find("tr:gt(0)").remove(); // delete all rows
    }
    
    var table_obj = $('#appt-table');
    if(json_data.length === 0) {
        var placeholder = $('<h4>', {id: "empty-table-placeholder", style: "text-align: center", html: "There are no appointments"});
        placeholder.insertAfter(table_obj);
        table_obj.remove();
    }
    else {
        $.each(json_data, function(index, item){
            var table_row = $('<tr>', {id: item.id});
            table_row.append($('<td>', {html: item.client}));
            table_row.append($('<td>', {html: item.service}));
            table_row.append($('<td>', {html: item.employee}));
            table_row.append($('<td>', {html: item.apptDateTime}));
            if(item.tips === 0) {
                table_row.append($('<td>---</td>')); 
            }
            else {
                table_row.append($('<td>', {html: Currency(item.tips)}));
            }
            if(item.total === 0) {
                table_row.append($('<td>---</td>')); 
            }
            else {
                table_row.append($('<td>', {html: Currency(item.total)}));
            }
            table_row.append($(`<td class="action"><a href="/appointments/delete/${item.id}">Delete</a> <a href="/appointments/update/${item.id}">Update</a></td>`))
            table_obj.append(table_row);
        })
    }
    
}

$(function() {
  $('#viewAllSwitch').click(function() {
   if($("#viewAllSwitch").is(":checked")) {
        document.getElementById("viewAllSwitchStatus").textContent = "Toggle View All: On";
        $.ajax({
            type: "get",
            contentType: "application/json",
            url: "/appointments/table",
            dataType: "json",
            data: {viewall: 1},
            success: function(response) {
                RegenerateAppointmentTableFromJson(response)
            },
            error: function(xhr) {
                console.log(xhr);
            }
        });
   }
   else {
        document.getElementById("viewAllSwitchStatus").textContent = "Toggle View All: Mine";
        $.ajax({
            type: "get",
            contentType: "application/json",
            url: "/appointments/table",
            dataType: "json",
            data: {viewall: 0},
            success: function(response) {
                RegenerateAppointmentTableFromJson(response)
            },
            error: function(xhr) {
                console.log(xhr);
            }
        });
   }
  });
});