
//アコーディオンをクリックした時の動作
$('.title').on('click', function() {//タイトル要素をクリックしたら
  var findElm = $(this).next(".box");//直後のアコーディオンを行うエリアを取得し
  $(findElm).slideToggle();//アコーディオンの上下動作

  if($(this).hasClass('close')){//タイトル要素にクラス名closeがあれば
    $(this).removeClass('close');//クラス名を除去し
  }else{//それ以外は
    $(this).addClass('close');//クラス名closeを付与
  }
});


window.onload = function(){
  var count = document.getElementsByClassName('book_data').length
  for (var n = 0; n < count; n++){
    var value = document.getElementById("book_value_" + String(n)).value
    var lower_diff = document.getElementById("book_lower_diff_" + String(n)).value
    var upper_diff = document.getElementById('book_upper_diff_' + String(n)).value
    var star_id
    for (var i = 1; i < 6; i++){
      star_id = "value_star_" + String(i) + "_" + String(n)
      if (value >= i)
        document.getElementById(star_id).style.color = "yellow"
      star_id = "diff_star_" + String(i) + "_" + String(n)
      if (lower_diff <= i && upper_diff >= i)
        document.getElementById(star_id).style.color = "yellow"
    }
  }
}

