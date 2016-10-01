//script for opening/closing of sidebar on mobiles and ensuring it is visible if the viewport is enlarged beyond the mobile view
$(function() {
  $('div.banner').click(function() {
    /*if ($(window).width() < 750) {
        $('div.left-col').toggleClass("left-col-show");
        if ($('div.left-col').hasClass("left-col-show")) {
          $('div.sidebar-closer').css("display", "block");
        }
        else {
          $('div.sidebar-closer').css("display", "none");
        }
        $('body').css("scroll-y", "hidden")
    }*/
    if (document.getElementsByClassName("left-col")[0].style.width == "0px") {
      document.getElementsByClassName("left-col")[0].style.width = "180px";
      document.getElementsByClassName("center-col")[0].style.marginLeft = "180px";
      document.getElementsByClassName("center-col")[0].style.width = "calc(100% - 180px)";
    } else {
      document.getElementsByClassName("left-col")[0].style.width = "0";
      document.getElementsByClassName("center-col")[0].style.marginLeft = "0";
      document.getElementsByClassName("center-col")[0].style.width = "100%";
    }
  });
});
$(function() {
  $('div.sidebar-closer').click(function() {
    if ($(window).width() < 750) {
        $('div.left-col').removeClass("left-col-show");
        $('div.sidebar-closer').css("display", "none");
        $('body').css("scroll-y", "hidden")
    }
  });
});
$(window).resize(function() {
  if (!($(window).width() < 750)) {
    $(".left-col").removeAttr('style');
  }
});
/*<!--Script to ensure banner does not overlap centercol and that the logo is the same height as the banner-->
<!-- Also ensures that the caver image is a sutiable size for the page (so you dont just see his butt)-->
<!-- Also ensures that anchor links are offset so the content isnt under the banner -->*/

/*function bannerresizer() {
  if (!($(window).width() < 750)) {
    $(".center-col").css("margin-top", Math.floor($(".banner").height()));
    $(".logo").css("min-height", Math.floor($(".banner").height()));
    $(".logo").css("height", Math.floor($(".banner").height()));
    //$(".logo img").css("padding-top", (Math.floor($(".banner").height()) - 100) / 2);
    $(".anchor").css("margin-top", -Math.floor($(".banner").height()))
  } else {
    $(".center-col").css("margin-top", Math.floor($(".banner").height()));
    $(".anchor").css("margin-top", -Math.floor($(".banner").height()))
  }
}

function caverresizer() {
  var viewportHeight = $(window).height();
  var bannerHeight = Math.floor($(".banner").height());
  if (viewportHeight - bannerHeight < 689) {
    $(".right-col").css({"background-size": 'auto ' + String(viewportHeight - bannerHeight) + 'px'});
  }
  else {
    $(".right-col").removeAttr("style");
  }
}

$(window).resize(function() {
  bannerresizer();
  caverresizer();
});
$(window).load(function() {
  caverresizer();
  bannerresizer();
});
