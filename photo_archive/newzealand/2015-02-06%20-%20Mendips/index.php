<!DOCTYPE html>
<html lang="en">
<head>
  <title>Imperial College Caving Club</title>
  <!-- Using the latest rendering mode for IE -->
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">


    <meta name="author" content="Stores Gnomes" />

  <link rel="stylesheet" href="https://union.ic.ac.uk/rcc/caving/newzealand/theme/css/main.css" type="text/css"/>

  <script src="https://union.ic.ac.uk/rcc/caving/newzealand/theme/js/jquery.js"></script>

  <!-- http://detectmobilebrowsers.com/ -->
  <!-- script to detect mobile browsers and use mobile stylesheet-->
  <script>
  (function(a){(jQuery.browser=jQuery.browser||{}).mobile=/(android|bb\d+|meego).+mobile|avantgo|bada\/|blackberry|blazer|compal|elaine|fennec|hiptop|iemobile|ip(hone|od)|iris|kindle|lge |maemo|midp|mmp|mobile.+firefox|netfront|opera m(ob|in)i|palm( os)?|phone|p(ixi|re)\/|plucker|pocket|psp|series(4|6)0|symbian|treo|up\.(browser|link)|vodafone|wap|windows ce|xda|xiino/i.test(a)||/1207|6310|6590|3gso|4thp|50[1-6]i|770s|802s|a wa|abac|ac(er|oo|s\-)|ai(ko|rn)|al(av|ca|co)|amoi|an(ex|ny|yw)|aptu|ar(ch|go)|as(te|us)|attw|au(di|\-m|r |s )|avan|be(ck|ll|nq)|bi(lb|rd)|bl(ac|az)|br(e|v)w|bumb|bw\-(n|u)|c55\/|capi|ccwa|cdm\-|cell|chtm|cldc|cmd\-|co(mp|nd)|craw|da(it|ll|ng)|dbte|dc\-s|devi|dica|dmob|do(c|p)o|ds(12|\-d)|el(49|ai)|em(l2|ul)|er(ic|k0)|esl8|ez([4-7]0|os|wa|ze)|fetc|fly(\-|_)|g1 u|g560|gene|gf\-5|g\-mo|go(\.w|od)|gr(ad|un)|haie|hcit|hd\-(m|p|t)|hei\-|hi(pt|ta)|hp( i|ip)|hs\-c|ht(c(\-| |_|a|g|p|s|t)|tp)|hu(aw|tc)|i\-(20|go|ma)|i230|iac( |\-|\/)|ibro|idea|ig01|ikom|im1k|inno|ipaq|iris|ja(t|v)a|jbro|jemu|jigs|kddi|keji|kgt( |\/)|klon|kpt |kwc\-|kyo(c|k)|le(no|xi)|lg( g|\/(k|l|u)|50|54|\-[a-w])|libw|lynx|m1\-w|m3ga|m50\/|ma(te|ui|xo)|mc(01|21|ca)|m\-cr|me(rc|ri)|mi(o8|oa|ts)|mmef|mo(01|02|bi|de|do|t(\-| |o|v)|zz)|mt(50|p1|v )|mwbp|mywa|n10[0-2]|n20[2-3]|n30(0|2)|n50(0|2|5)|n7(0(0|1)|10)|ne((c|m)\-|on|tf|wf|wg|wt)|nok(6|i)|nzph|o2im|op(ti|wv)|oran|owg1|p800|pan(a|d|t)|pdxg|pg(13|\-([1-8]|c))|phil|pire|pl(ay|uc)|pn\-2|po(ck|rt|se)|prox|psio|pt\-g|qa\-a|qc(07|12|21|32|60|\-[2-7]|i\-)|qtek|r380|r600|raks|rim9|ro(ve|zo)|s55\/|sa(ge|ma|mm|ms|ny|va)|sc(01|h\-|oo|p\-)|sdk\/|se(c(\-|0|1)|47|mc|nd|ri)|sgh\-|shar|sie(\-|m)|sk\-0|sl(45|id)|sm(al|ar|b3|it|t5)|so(ft|ny)|sp(01|h\-|v\-|v )|sy(01|mb)|t2(18|50)|t6(00|10|18)|ta(gt|lk)|tcl\-|tdg\-|tel(i|m)|tim\-|t\-mo|to(pl|sh)|ts(70|m\-|m3|m5)|tx\-9|up(\.b|g1|si)|utst|v400|v750|veri|vi(rg|te)|vk(40|5[0-3]|\-v)|vm40|voda|vulc|vx(52|53|60|61|70|80|81|83|85|98)|w3c(\-| )|webc|whit|wi(g |nc|nw)|wmlb|wonu|x700|yas\-|your|zeto|zte\-/i.test(a.substr(0,4))})(navigator.userAgent||navigator.vendor||window.opera);
  </script>
  <script>
    if (jQuery.browser.mobile) {
      $("link").attr("href","https://union.ic.ac.uk/rcc/caving/newzealand/theme/css/mobile.css");
    }
  </script>
  <script>
  $( document ).ready(function() {
    if (jQuery.browser.mobile) {
      $('div.left-col').addClass('nodisplay');
    }
  });
  </script>
  <!-- script for opening/closing of sidebar on mobiles -->
  <script>
  $(function() {
    $('div.banner').click(function(){
          $('div.left-col').toggleClass('nodisplay');
      });
  });
  </script>


<!--Control expansion of thumbnail box"-->
<script>
$(function() {
  $('div.thumb-toggle').click(function(){
        $('div.thumb_box').toggleClass('expand-thumb-box');
        $('div.thumb-toggle').toggleClass('nodisplay');

        var thumbox = ""
        var ca = document.cookie.split(';');
        for(var i=0; i<ca.length; i++) {
            var c = ca[i];
            while (c.charAt(0)==' ') c = c.substring(1);
            if (c.indexOf("thumbox=") != -1) thumbox = c.substring("thumbox=".length,c.length);
        }
        if (thumbox == "expand") {
          document.cookie = "thumbox=" + "collapse" + ";";
        }
        else if (thumbox == "collapse") {
          document.cookie = "thumbox=" + "expand" + ";";
        }
        else {
          document.cookie = "thumbox=" + "collapse" + ";";
        }
    });
});

$( window ).load(function()
{
  var thumbox = "";
  var ca = document.cookie.split(';');
  for(var i=0; i<ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0)==' ') c = c.substring(1);
      if (c.indexOf("thumbox=") != -1) thumbox = c.substring("thumbox=".length,c.length);
  }
  if (thumbox == "expand") {
    $('div.thumb-toggle').each(function() {
      if ($(this).hasClass("thcollapse")) {
        $(this).removeClass("nodisplay");
      } else if ($(this).hasClass("thexpand")) {
        $(this).addClass("nodisplay");
      }
    });
    $('div.thumb_box').addClass('expand-thumb-box');
  }
  else if (thumbox == "collapse") {
    $('div.thumb-toggle').each(function() {
      if ($(this).hasClass("thcollapse")) {
        $(this).addClass("nodisplay");
      } else if ($(this).hasClass("thexpand")) {
        $(this).removeClass("nodisplay");
      }
    });
    $('div.thumb_box').removeClass('expand-thumb-box');
  }
  else {
    document.cookie = "thumbox=" + "collapse" + ";";
    $('div.thumb-toggle').each(function() {
      if ($(this).hasClass("thexpand")) {
        $(this).addClass("nodisplay");
      } else if ($(this).hasClass("thcollapse")) {
        $(this).removeClass("nodisplay");
      }
    });
    $('div.thumb_box').removeClass('expand-thumb-box');
  }
});

</script>

<!--Remember scroll positions of page and selected item in the thumb box-->
<script>
function scroll(evt) {
  var pagey = document.body.scrollTop;
  document.cookie = "pagey=" + pagey + ";";
}
function mobscroll(evt) {
  var pagey = document.body.scrollTop;
  document.cookie = "pagey=" + pagey + ";";
}

$( window ).load(function()
{
  document.addEventListener("touchend", mobscroll, false);
  document.addEventListener("scroll", scroll, false);

  var suby = $(".select-thumbnail").offset().top - $("#thumbnails-top").offset().top;
  document.cookie = "suby=" + suby + ";";

  var pagey_search = "pagey=";
  var suby_search = "suby=";
  var ca = document.cookie.split(';');
  for(var i=0; i<ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0)==' ') c = c.substring(1);
      if (c.indexOf(pagey_search) != -1) pagey = c.substring(pagey_search.length,c.length);
      if (c.indexOf(suby_search) != -1) suby = c.substring(suby_search.length,c.length);
  }
  document.body.scrollTop = pagey;
  document.getElementById("thumb_box").scrollTop = suby;
});
</script>


</head>
<body>
  <div class="banner">
    <div class="logo"></div>
    <div class="banner-title">
Photos    </div>
    <div class="banner-title-menu">Menu</div>
  </div>

  <div style="clear: both;"></div>

  <div class="left-col">
<div class="sidebar">
      <hr class="hrsidebartop">

      <div class="sidebar-content-box">
        <div class="sidebar-item"><a href="https://union.ic.ac.uk/rcc/caving/newzealand/">Home</a></div>
        <div class="sidebar-item"><a href="https://union.ic.ac.uk/rcc/caving/newzealand/pages/introduction.html">Introduction</a></div>
        <div class="sidebar-item"><a href="https://union.ic.ac.uk/rcc/caving/newzealand/pages/team.html">Team</a></div>
        <div class="sidebar-item"><a href="https://union.ic.ac.uk/rcc/caving/newzealand/pages/itinerary.html">Itinerary</a></div>
      </div>

      <hr class="hrsidebar">

      <div class="sidebar-content-box">
        <div class="sidebar-item" data-idouter="posts-outer" data-idinner="posts-inner"><a>Trips and Posts</a></div>
        <div class="sidebar-outer collapsed" id="posts-outer">
          <div class="sidebar-inner" id="posts-inner">
                <div class="sidebar-sub-item"><a href="https://union.ic.ac.uk/rcc/caving/newzealand/articles/mendips.html">Mendips</a></div>
          </div>
        </div>
      </div>

      <hr class="hrsidebar">

      <div class="sidebar-content-box">
        <div class="sidebar-item"><a href="https://union.ic.ac.uk/rcc/caving/newzealand/photo_archive/">Photos</a></div>
      </div>

      <script>
      $(function() {
        $('div.sidebar-item, div.sidebar-sub-item').click(function(){
          var outer = $(this).data("idouter");
          var inner = $(this).data("idinner");
          var outerelement = $('#' + outer);
          var innerelement = $('#' + inner);
          if (outerelement.hasClass('collapsed')) {
            outerelement.css({ 'max-height': innerelement.outerHeight() + 'px' });
            var height = innerelement.outerHeight();
          } else {
            outerelement.css({ 'max-height': '0px' });
          }
          outerelement.toggleClass('collapsed');

          if ($(this).data("upidouter") != null && $(this).data("upidinner")) {
            var outer = $(this).data("upidouter");
            var inner = $(this).data("upidinner");
            var outerelement = $('#' + outer);
            var innerelement = $('#' + inner);
            if (!outerelement.hasClass('collapsed')) {
              var newheight = parseInt(outerelement.css('max-height'), 10) + height;
              outerelement.css({ 'max-height': newheight + 'px' });
            }
          }

        });
      });
      </script>

</div>  </div>

  <div style="clear: both;"></div>

    <div class="center-col">

<div class="container">

<?php

$files = array();

foreach (scandir('.') as $file)
{
    $file_parts = pathinfo($file);
    if (strcasecmp($file_parts['extension'], 'gif') == 0 || strcasecmp($file_parts['extension'], 'jpg') == 0 ||strcasecmp($file_parts['extension'], 'png') == 0)
    {
        if (strpos($file, '--thumb') == false and strpos($file, '--orig') == false)
        {
            $files[] = $file;
        }
    }
}

$search = $_GET["image"];
$imagekey = array_search($search, $files);

echo '<div class="link-container">' . "\n";
if ( $files[$imagekey-1] != null)
  {
  echo '<div class="prevlink"><a id="prevlink" href=".?image=' . $files[$imagekey-1] . '">Previous</a></div>' . "\n";
  }
else
  {
  echo '<div class="prevlink" ><a id="prevlink">Previous</a></div><br>' . "\n";
  }
if ( $files[$imagekey] != null)
  {
  $file_parts = pathinfo($files[$imagekey]);
  echo '<div class="currlink"><a id="currlink" href="' . $file_parts['filename'] . '--orig.' . $file_parts['extension'] . '">Original</a></div>' . "\n";
  }
else
  {
  echo '<div class="currlink" ><a id="prevlink">Original</a></div><br>' . "\n";
  }
if ( $files[$imagekey+1] != null)
  {
  echo '<div class="nextlink"><a id="nextlink" href=".?image=' . $files[$imagekey+1] . '">Next</a></div>' . "\n";
  }
else
  {
  echo '<div class="nextlink" ><p id="nextlink">Next</a></div><br>' . "\n";
  }

echo '<div style="clear: both;"></div>' . "\n";
echo '</div>' . "\n";

?>

<div class="article-content">

<?php

echo '<div class="image-wrapper"><div class="image-cell">';
if ($files[$imagekey] != null)
  {
  if ( $files[$imagekey+1] != null)
  {
    echo '<a id="mainlink" href=".?image=' . $files[$imagekey+1] . '">';
  }
  else
  {
    echo '<a id="mainlink" href=".?image=' . $files[0] . '">';
  }
  echo '<img class="maindisplay" id="maindisplay" alt="Click thumbnails below to see image. Click image to go to next image" src="' . $files[$imagekey] . '"></a></div></div>' . "\n";
  }
else
  {
  echo '<a id="mainlink">';
  echo '<img class="maindisplay" id="maindisplay" alt="Click thumbnails below to see image. Click image to get original"></a></div></div>' . "\n";
  }

echo '<div class="thumb-toggle nodisplay thcollapse">Collapse</div>' . "\n";
echo '<div class="thumb-toggle thexpand">Expand</div>' . "\n";

echo '<div id ="thumb_box" class="thumb_box">' . "\n";
echo '<div id="thumbnails-top"></div>' . "\n";

foreach ($files as $key=>$file) {
    $file_parts = pathinfo($file);
    echo '<a class="thumbnail" id=' . $file . ' href=".?image=' . $file . '">' . "\n";
    if ($imagekey == $key)
  {
    echo '<img id=image-' . $file . ' class="select-thumbnail" src="' . $file_parts['filename'] . '--thumb.' . $file_parts['extension'] . '"></a>' . "\n";
  }
  else
  {
    echo '<img id=image-' . $file . ' class="thumbnail" src="' . $file_parts['filename'] . '--thumb.' . $file_parts['extension'] . '"></a>' . "\n";
  }
}

echo '</div>' . "\n";

?>

</div>
</div>

    </div>

    <div class="right-col">
    </div>


</body>
</html>