// ------------------ Ajax設定 ------------------ //
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

// ------------------ 終了 ------------------ //

var createBookRanking = function(i, name, isbn, image, language, junre, value, sample){
    var res = ""
    res += '<button class="none_btn" type="submit" id="search_btn" name="isbn" value="' + isbn + '">'
    res += '<div class="book_data">'
    res += '<div class="book_rank">' + String(i+1) + '位</div>'
    res += '<div class="book_image">'
    res += '<img src="' + image + '" alt="book image">'
    res += '</div>'
    res += '<div class="book_detail">'
    res += '<div class="book_name">' + name + '</div>'
    res += '<div class="book_language">言語 : ' + language + '</div>'
    res += '<div class="book_junre">ジャンル : ' + junre + '</div>'
    res += '<div class="book_value">平均評価 : ' + String(value) + '</div>'
    res += '<div class="book_sample">読んだ人数 : ' + String(sample) + '</div>'
    res += '</div>'
    res += '</div>'
    res += '</button>'
    return res
}


$('#post_form').on('submit', function(e) {
    e.preventDefault()
    document.getElementById('error').innerText = ""
    var search_text = document.getElementById('search_text').value
    var lower_sample = document.getElementById('search_sample').value
    var search_diff = document.getElementById('search_diff').value
    
    if (search_text.length === 0 || lower_sample.length === 0  || search_diff.length === 0){
        document.getElementById("error").innerText = "言語またはジャンルとサンプルの下限を見直してください"　
        return
    }

    var lanjas = document.getElementsByTagName('option')
    var miss = true

    for (var i = 0; i < lanjas.length; i++){
        if (search_text == lanjas[i]['innerText'])
        miss = false
    }
    
    if (miss || isNaN(lower_sample)  || isNaN(search_diff)){
        document.getElementById("error").innerText = "言語またはジャンルとサンプルの下限を見直してください"　
        return
    }

    document.getElementById('error').innerText = ""
    $.ajax({
        'url': '',
        'type': 'POST',
        'data': {'type': 'booksSearch', 'search_text': search_text, 'lower_sample': lower_sample, "diff": search_diff},
        'dataType': 'json'
    })
    .done(function(response){
        const error = response.error
        if (error.length > 0){
            document.getElementById('error').innerText = error
            return
        }
        const names = response.names
        const isbns = response.isbns
        const images = response.images
        const languages = response.languages
        const junres = response.junres
        const values = response.values
        const samples = response.samples
        var book_ranking = document.getElementById('bookRanking')
        book_ranking.innerHTML = ""
        for (var i = 0; i < names.length; i++)
            book_ranking.innerHTML += createBookRanking(i, names[i], isbns[i], images[i], languages[i], junres[i], values[i], samples[i])
    })
});