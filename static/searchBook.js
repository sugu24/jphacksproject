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

var createBooksData = function(title, isbn, imageUrl){
    var res = ""
    res += '<div class="book_data">'
    res += '<div class="book_image">'
    res += '<img src="' + imageUrl + '" alt="book of image">'
    res += '</div>'
    res += '<div class="book_title">'
    res += '<p>' + title + '</p>'
    res += '</div>'
    res += '<div class="btn-div">'
    res += '<input hidden type="text" name="' + isbn + '_title" value="' + title + '" id="' + title + '">'
    res += '<input hidden type="text" name="' + isbn + '_imageUrl" value="' + imageUrl + '" id="' + imageUrl + '">'
    res += '<button type="submit" name="selectBook" class="btn btn-sub btn-block btn-large" value="' + isbn + '">これを読んだ</button>'
    res += '</div>'
    res += '</div>'
    return res
}

$('#post_form').on('submit', function(e) {
    e.preventDefault()
    document.getElementById('error').innerText = ""
    var book_name = document.getElementById('search_book_name').value
    if (book_name.length === 0){
        document.getElementById("error").innerText = "検索する本のタイトルを入力してください"　
        return
    }
    
    document.getElementById('error').innerText = ""
    $.ajax({
        'url': '',
        'type': 'POST',
        'data': {'type': 'searchBookTitle', 'bookTitle': book_name},
        'dataType': 'json'
    })
    .done(function(response){
        const Titles = response.titles
        const Isbns = response.isbns
        const ImageUrls = response.image_urls
        console.log(Titles)
        var books_datas = document.getElementById('books')
        books_datas.innerHTML = ""
        var add_html
        for (var i = 0; i < Titles.length; i++){
            add_html = createBooksData(Titles[i], Isbns[i], ImageUrls[i])
            books_datas.innerHTML += add_html
        }
    })
})

