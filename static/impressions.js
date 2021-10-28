window.onload = function(){
    var count = document.getElementById('count').innerText
    var diff1 = document.getElementById('diff1').value
    var diff2 = document.getElementById('diff2').value
    var diff3 = document.getElementById('diff3').value
    var diff4 = document.getElementById('diff4').value
    var diff5 = document.getElementById('diff5').value
    var val1 = document.getElementById('val1').value
    var val2 = document.getElementById('val2').value
    var val3 = document.getElementById('val3').value
    var val4 = document.getElementById('val4').value
    var val5 = document.getElementById('val5').value
    document.getElementById("diff1_chart").classList.add('chart--p' + String(parseInt(diff1/count)*100))
    document.getElementById("diff2_chart").classList.add('chart--p' + String(parseInt(diff2/count)*100))
    document.getElementById("diff3_chart").classList.add('chart--p' + String(parseInt(diff3/count)*100))
    document.getElementById("diff4_chart").classList.add('chart--p' + String(parseInt(diff4/count)*100))
    document.getElementById("diff5_chart").classList.add('chart--p' + String(parseInt(diff5/count)*100))
    document.getElementById("val1_chart").classList.add('chart--p' + String(parseInt(val1/count)*100))
    document.getElementById("val2_chart").classList.add('chart--p' + String(parseInt(val2/count)*100))
    document.getElementById("val3_chart").classList.add('chart--p' + String(parseInt(val3/count)*100))
    document.getElementById("val4_chart").classList.add('chart--p' + String(parseInt(val4/count)*100))
    document.getElementById("val5_chart").classList.add('chart--p' + String(parseInt(val5/count)*100))
}
