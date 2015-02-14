{% extends "base.html" %}

{% block head %}
<script type="text/javascript">
window.onscroll = function()
    {
      var pagey = document.body.scrollTop;
    var suby = document.getElementById("thumb_box").scrollTop;
    document.cookie = "pagey=" + pagey + ";"
      document.cookie = "suby=" + suby + ";";
    }
window.onload = function()
{
document.getElementById("thumb_box").onscroll = function()
    {
      var pagey = document.body.scrollTop;
    var suby = document.getElementById("thumb_box").scrollTop;
    document.cookie = "pagey=" + pagey + ";"
      document.cookie = "suby=" + suby + ";";
    }
}
</script>

<style>
body {
  height:100%;
  overflow: scroll;
}
.prevlink {
  display: table-cell;
  text-align: center;
  vertical-align: middle;
  width: 50%;
  }
.nextlink {
  display: table-cell;
  text-align: center;
  vertical-align: middle;
  width: 50%;
  }
.link-container {
  display: table;
  width: 100%;
}
.maindisplay {
  max-width: 780px;
  max-height: 600px;
}

.image-wrapper {
  height: 600px;
  display: table;
  width: 100%;
}
.image-cell {
  display: table-cell;
  text-align: center;
  vertical-align: middle;
}

.r-sidebar {
  float:right;
  width: 185px;
}

.thumb_box {
  height: 150px;
  /*width: 100%;*/
  overflow-y: scroll;
  overflow-x: hidden;
  bottom: 5px;
  /*position: absolute;*/
}
.select-thumbnail {
  border: 5px solid white;
}
.thumbnail {
  border: 5px solid transparent;
}
</style
</head>

{% endblock %}

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

echo '<div class="image-wrapper"><div class="image-cell">';
if ($files[$imagekey] != null)
  {
  echo '<a id="mainlink" href="' . $files[$imagekey] . '">';
  echo '<img class="maindisplay" id="maindisplay" alt="Click thumbnails below to see image. Click image to get original" src="' . $files[$imagekey] . '"></a></div></div>' . "\n";
  }
else
  {
  echo '<a id="mainlink">';
  echo '<img class="maindisplay" id="maindisplay" alt="Click thumbnails below to see image. Click image to get original"></a></div></div>' . "\n";
  }
echo '<div class="link-container">' . "\n";
if ( $files[$imagekey-1] != null)
  {
  echo '<div class="prevlink"><a id="prevlink" href=".?image=' . $files[$imagekey-1] . '">Previous</a></div>' . "\n";
  }
else
  {
  echo '<div class="prevlink" ><a id="prevlink">Previous</a></div><br>' . "\n";
  }
if ( $files[$imagekey+1] != null)
  {
  echo '<div class="nextlink"><a id="nextlink" href=".?image=' . $files[$imagekey+1] . '">Next</a></div>' . "\n";
  }
else
  {
  echo '<div class="nextlink" ><a id="nextlink">Next</a></div><br>' . "\n";
  }

echo '<div style="clear: both;"></div>' . "\n";
echo '</div>' . "\n";

echo '<div id ="thumb_box" class="thumb_box">' . "\n";

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

include('/home/users/website/rcc/caving/end.php');

echo '<div class="r-sidebar">';

begintextbox("Directories");

echo '<div class="dirlist">' . "\n";
foreach (scandir('.') as $file)
{
    $file_parts = pathinfo($file);
    if(is_dir($file) and $file != ".")
    {
        echo "<a href=$file/>$file</a>";
        echo "<br>" . "\n";
    }
}
echo '</div>' . "\n";
endtextbox();
echo '</div>' . "\n";
?>

<script type="text/javascript">
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
</script>
