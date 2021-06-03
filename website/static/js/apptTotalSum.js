$(function() {
    $('.sum-param, #client').change(function() {
        const serviceText = $('#service option:selected').text();
        let tip = $('#tip').val();
        if(tip === '') {
            tip = 0;
        }
        let service =serviceText.split(' ')[1].replace('$', '')
        
        const sum = parseFloat(service) + parseFloat(tip);
        console.log("sum: " + sum + " services: " + service + " tip: " + tip)
        $('#tip').val(tip);
        $('#total').val(sum.toFixed(2));
    });
});