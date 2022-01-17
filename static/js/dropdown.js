$(".default1").click(function () {
    $(this).siblings(".dropdown1 ul").toggleClass("active");
});

$(".dropdown1 ul li").click(function () {
    var text = $(this).text();
    $(".default1 div:first-child").text(text);
    $(".dropdown1 ul").removeClass("active");
});

$(".default2").click(function () {
    $(this).siblings(".dropdown2 ul").toggleClass("active");
});

$(".dropdown2 ul li").click(function () {
    var text = $(this).text();
    $(".default2 div:first-child").text(text);
    $(".dropdown2 ul").removeClass("active");
});

$(".default3").click(function () {
    $(this).siblings(".dropdown3 ul").toggleClass("active");
});

$(".dropdown3 ul li").click(function () {
    var text = $(this).text();
    $(".default3 div:first-child").text(text);
    $(".dropdown3 ul").removeClass("active");
});

function check(){
    if ($(window).width() < 1000) {
        console.log("here");
        document.getElementById("nav-toggle").checked = true;
    }
    else {
        document.getElementById("nav-toggle").checked = false;

    }
}

check();