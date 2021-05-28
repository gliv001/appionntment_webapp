function apptTotalSum() {
    const services = $('#service').val();
    let sum = 0;
    services.forEach(s => {
        sum += parseInt(s.split(' ')[1]);
    });
    const tip = $('#tip').val();
    sum += tip;
    $('#total').val(sum)
}

$(function() {
    $('#service').change(function() {
        const services = $('#service').val();
        let sum = 0;
        services.forEach(s => {
            sum += parseFloat(s.split(' ')[1]);
        });
        let tip = $('#tip').val();
        if(tip === '') {
            tip = 0;
        }
        console.log(tip)
        sum += parseFloat(tip);
        $('#total').val(sum)
    });

    $('#tip').change(function() {
        const services = $('#service').val();
        let sum = 0;
        services.forEach(s => {
            sum += parseInt(s.split(' ')[1]);
        });
        let tip = $('#tip').val();
        if(tip === '') {
            tip = 0;
        }
        sum += parseFloat(tip);
        $('#total').val(sum)
    });
});