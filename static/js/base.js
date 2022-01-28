// Tokenizing
jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

loaderPage(false);
// loader
function loaderPage(stat) {
    if (stat == true) {
        $('.page_loader').show();
    } else {
        $('.page_loader').hide();
    }
};

displayResult(false)
// display result
function displayResult(stat) {
    if (stat == true) {
        $('#result_scr').show();
    } else {
        $('#result_scr').hide();
    }
};

function search(){
    var option = $("#optionScrap").val()
    var url = $("#urlScrap").val()
    loaderPage(true)

    $.ajax({
        url: 'scrapp',
        data: {
            'o': option,
            'u': url
        },
        type: 'POST',
        dataType: 'json',
        success: function(data) {
            loaderPage(false)
            
            if (data.code == 0){
                result = data.result
                if(result.code == 0){
                    displayResult(true)
                    $("#source").html(result.source)
                    $("#title").html(result.title)
                    $("#price_usd").html(`$`+result.price)
                    $("#price_idr").html(`Rp. `+result.id_price)
    
                    var list_img = result.image
                    var list_img_html = [];
                    for (i in list_img){
                        var img = ` <div class="col-md-3">
                                        <img src="`+ list_img[i] +`" class="img-thumbnail" style="min-width: 150px;">
                                    </div>`
    
                        list_img_html.push(img)
                    }
    
                    $("#img_s").html(list_img_html)    
                }else{
                    Swal.fire({
                        icon: 'error',
                        title: 'Oops...',
                        text: result.text,
                    })    
                }
                

            }else{
                Swal.fire({
                    icon: 'error',
                    title: 'Oops...',
                    text: data.result,
                })
            }
        }
    });
}