var paintStar = function(v){
    var star_id
    for (var i = 1; i <= 5; i++){
        star_id = "value_star_" + String(i)
        if (i <= v)
            document.getElementById(star_id).style.color = "yellow"
        else
            document.getElementById(star_id).style.color = "white"
    }
    document.getElementById('value_value').value = String(v)
}

$('#value_star_1').on('click', function(e) {e.preventDefault();paintStar(1);})
$('#value_star_2').on('click', function(e) {e.preventDefault();paintStar(2);})
$('#value_star_3').on('click', function(e) {e.preventDefault();paintStar(3);})
$('#value_star_4').on('click', function(e) {e.preventDefault();paintStar(4);})
$('#value_star_5').on('click', function(e) {e.preventDefault();paintStar(5);})


var lower_value = 3
var upper_value = 3

var max = function(a,b){if (a > b) return a; else return b;}
var min = function(a,b){if (a < b) return a; else return b;}

var paintLowerStar = function(v){
    var star_id
    if (v > upper_value) paintUpperStar(v)
    lower_value = v
    for (var i = 1; i <= 5; i++){
        star_id = "lower_diff_star_" + String(i)
        if (i <= v)
            document.getElementById(star_id).style.color = "yellow"
        else
            document.getElementById(star_id).style.color = "white"
    }
    document.getElementById('lower_diff_value').value = String(v)
}

var paintUpperStar = function(v){
    var star_id
    if (v < lower_value) paintLowerStar(v)
    upper_value = v
    for (var i = 1; i <= 5; i++){
        star_id = "upper_diff_star_" + String(i)
        if (i <= v)
            document.getElementById(star_id).style.color = "yellow"
        else
            document.getElementById(star_id).style.color = "white"
    }
    document.getElementById('upper_diff_value').value = String(v)
}

$('#lower_diff_star_1').on('click', function(e) {e.preventDefault();paintLowerStar(1);})
$('#lower_diff_star_2').on('click', function(e) {e.preventDefault();paintLowerStar(2);})
$('#lower_diff_star_3').on('click', function(e) {e.preventDefault();paintLowerStar(3);})
$('#lower_diff_star_4').on('click', function(e) {e.preventDefault();paintLowerStar(4);})
$('#lower_diff_star_5').on('click', function(e) {e.preventDefault();paintLowerStar(5);})

$('#upper_diff_star_1').on('click', function(e) {e.preventDefault();paintUpperStar(1);})
$('#upper_diff_star_2').on('click', function(e) {e.preventDefault();paintUpperStar(2);})
$('#upper_diff_star_3').on('click', function(e) {e.preventDefault();paintUpperStar(3);})
$('#upper_diff_star_4').on('click', function(e) {e.preventDefault();paintUpperStar(4);})
$('#upper_diff_star_5').on('click', function(e) {e.preventDefault();paintUpperStar(5);})