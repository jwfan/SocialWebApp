$(document).ready(function () {
    tab = 0;
    $("#add-post").click(addPost);
    $("#post-event13").keypress(function (e) {
        if (e.which == 13) addPost();
    });
    $("#followtab").click(function (e) {
        tab = 1
        updateposts()
    });
    $("#globaltab").click(function (e) {
        tab = 0
        updateposts()
    })

    updateposts();
    $("#post-event13").focus();

    window.setInterval(updateposts, 5000);

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

    var csrftoken = getCookie('csrftoken');
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    });
})


function updateposts() {
    if (tab == 0) {
        postdiv = $("#global");
        if (postdiv.data("max_time") == null) {
            var max_time = "1970-01-01 00:00:00.000000+00:00"
        } else {
            var max_time = postdiv.data("max_time")
        }
        $.get("/grumblr/get-changes/" + max_time)
            .done(function (data) {
                generatepost(data)
            })
    }
    else {
        postdiv = $("#following");
        if (postdiv.data("max_time") == null) {
            var max_time = "1970-01-01 00:00:00.000000+00:00"
        } else {
            var max_time = postdiv.data("max_time")
        }
        $.get("/grumblr/get-followchanges/" + max_time)
            .done(function (data) {
                generatepost(data)
            })
    }
}

function generatepost(data) {
    if (tab == 0) {
        postdiv = $("#global");
    } else {
        postdiv = $("#following");
    }
    postdiv.data("max_time", data['max_time']);
    for (var i = 0; i < data.posts.length; i++) {
        post = data.posts[i];
        var raw = $($("#post-template").val()).clone();
        raw.find("#profilehref").attr("href", post.profilehref);
        raw.find("#imagehref").attr("src", post.imagehref);
        raw.find("#profileusername").html(post.username);
        raw.find("#profileusername").attr("href", post.profilehref);
        raw.find("#postcontent").html(post.content);
        raw.find("#poststamp").html(post.timestamp);
        raw.find("#commentform").html(post.form);
        raw.attr("id", post.id);
        raw.find(".add-comment").click({post_id: post.id}, addComment);
        raw.find(".add-comment").data("postid", post.id);
        raw.find("#comment-event13").keypress(function (e) {
            if (e.which == 13) {
                addComment($(this).parents(".postiddiv").attr("id"));
            }
        });
        raw.find("#comment-event13").data("postid", post.id);
        postdiv.prepend(raw);
    }
    updatecomments();
}

function updatecomments() {
    if (tab == 0) {
        postdiv = $("#global");
        if (postdiv.data("max_commenttime") == null) {
            var max_commenttime = "1970-01-01 00:00:00.000000+00:00"
        } else {
            var max_commenttime = postdiv.data("max_commenttime")
        }
        $.get("/grumblr/get-comments/" + max_commenttime)
            .done(function (data) {
                generatecomments(data)
            })
    }
    else {
        postdiv = $("#following");
        if (postdiv.data("max_commenttime") == null) {
            var max_commenttime = "1970-01-01 00:00:00.000000+00:00"
        } else {
            var max_commenttime = postdiv.data("max_commenttime")
        }
        $.get("/grumblr/get-followcomments/" + max_commenttime)
            .done(function (data) {
                generatecomments(data)
            })
    }


}

function generatecomments(data) {
    if (tab == 0) {
        postdiv = $("#global");
    } else {
        postdiv = $("#following");
    }
    postdiv.data("max_commenttime", data['max_commenttime']);
    for (var i = 0; i < data.comments.length; i++) {
        comment = data.comments[i];
        var raw = $($("#comment-template").val()).clone();
        raw.find("#commenthref").attr("href",comment.profilehref);
        raw.find("#commentprofile").attr("href", comment.profilehref);
        raw.find("#commentimage").attr("src", comment.imagehref);
        raw.find("#commentusername").html(comment.username);
        raw.find("#commentusername").attr("href", comment.profilehref);
        raw.find("#commentcontent").html(comment.content);
        raw.find("#commentstamp").html(comment.timestamp);
        postid = "#" + comment.postid;
        commentdiv = postdiv.find(postid).find(".comments");
        commentdiv.append(raw);
    }
}

function addPost() {
    post = $("#post-event13");
    $.post("/grumblr/newpost", {'content': post.val()})
        .done(function (data) {
            updateposts();
            post.val("").focus();
        })
}

function addComment(post_id) {
    if (post_id.data != null) {
        post_id = post_id.data.post_id
    }
    if (tab == 0) {
        postdiv = $("#global");
    } else {
        postdiv = $("#following");
    }
    comment = postdiv.find("#" + post_id).find("#comment-event13");
    $.post("/grumblr/newcomment", {'content': comment.val(), 'post_id': post_id})
        .done(function (data) {
            updatecomments();
            comment.val("").focus();
        })
}
