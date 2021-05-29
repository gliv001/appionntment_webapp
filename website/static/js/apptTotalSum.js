$(function() {
    $('#service').change(function() {
        let service = $('#service').val();
        let tip = $('#tip').val();
        if(tip === '') {
            tip = 0;
        }
        let sum = parseFloat(service.split(' ')[1]) + parseFloat(tip);
        $('#total').val(sum)
    });

    $('#tip').change(function() {
        let service = $('#service').val();
        let tip = $('#tip').val();
        if(tip === '') {
            tip = 0;
        }
        let sum = parseFloat(service.split(' ')[1]) + parseFloat(tip);
        $('#total').val(sum)
    });
});