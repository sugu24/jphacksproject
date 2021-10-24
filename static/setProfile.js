window.onload = function(){
    var languages = document.getElementById('hidden_user_languages').innerText
    var junres = document.getElementById('hidden_user_junres').innerText
    var token = ""
    var asi
    for (var i = 0; i < languages.length; i++){
        asi = languages[i].charCodeAt(0)
        if (asi === 32 || asi === 10 || i == languages.length-1){
            console.log(token)
            document.getElementById(token).checked = true
            token = ""
        }
        else token += languages[i]
    }
    for (var i = 0; i < junres.length; i++){
        asi = junres[i].charCodeAt(0)
        if (asi === 10 || asi === 32 || i == junres.length-1){
            document.getElementById(token).checked = true
            token = ""
        }
        else token += junres[i]
    }
}