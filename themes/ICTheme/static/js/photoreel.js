function move(newcount) {
  clickQuick = true;
  if (newcount >= maxcount) {
    newcount = 0;
  }
  if (newcount <= -1) {
    newcount = maxcount - 1;
  }

  if (count > newcount) {
    var big = count;
    var small = newcount;
  } else {
    var big = newcount;
    var small = count;
  }
  for (var i = 0; i < maxcount; ++i) {
    var photo = document.querySelector('.photoreel-photo-' + i)
    var moves = i - newcount;
    var percents = (moves) * 100;
    if (i >= small && i <= big) {
      photo.style.transition = "left " + transtime + "s linear";
    }
    else {
      photo.style.transition = ""
    }
    photo.style.left = percents + "%";
    if (i == newcount) {
      document.querySelector('.photoreel-dot-' + i).classList.add('selected');
    }
    else {
      document.querySelector('.photoreel-dot-' + i).classList.remove('selected');
    }
  }
  document.querySelector('.photoreel-container').style.height = document.querySelector('.photoreel-photo-' + newcount).offsetHeight + "px";
  count = newcount;
  setTimeout(function() {
    clickQuick = false;
  }, transtime*1000);
}

function moveright() {
  if (!clickQuick) {
    move(count + 1);
  }
}
function moveleft() {
  if (!clickQuick) {
    move(count - 1);
  }
}
function dotClick(e) {
  if (!clickQuick) {
    move(parseInt(e.target.dataset.count));
  }
}

var count = 0;
var clickQuick = false;

document.querySelector('.photoreel-right').addEventListener("click", moveright, false);
document.querySelector('.photoreel-left').addEventListener("click", moveleft, false);
document.querySelector('.photoreel-right').addEventListener("click", function() {clearInterval(intervalID);}, false);
document.querySelector('.photoreel-left').addEventListener("click", function() {clearInterval(intervalID);}, false);
var dots = document.querySelectorAll('.photoreel-dot');
document.querySelector('.photoreel-dot-0').classList.add("selected");
for (i = 0; i < dots.length; ++i) {
    dots[i].addEventListener("click", dotClick, false);
    dots[i].addEventListener("click", function() {clearInterval(intervalID);}, false);
}
var intervalID = window.setInterval(moveright, nextslidetime*1000);

// Set the heights/widths that css can't manage
var titles = document.querySelectorAll('.photoreel-title');
for (i = 0; i < titles.length; ++i) {
    titles[i].style.left = "calc(50% - " + (titles[i].offsetWidth / 2) + "px)";
}
var dotscont = document.querySelector('.photoreel-dots');
dotscont.style.left = "calc(50% - " + (dotscont.offsetWidth / 2) + "px)";

window.addEventListener("resize", function() {
  document.querySelector('.photoreel-container').style.height = document.querySelector('.photoreel-photo-' + count).offsetHeight + "px";
});
window.addEventListener("load", function() {
  document.querySelector('.photoreel-container').style.height = document.querySelector('.photoreel-photo-' + count).offsetHeight + "px";
});

window.addEventListener("keydown", function(e) {
  e = e || window.event;
  if (e.keyCode == '37') {
    clearInterval(intervalID);
    moveleft();
  }
  else if (e.keyCode == '39') {
    clearInterval(intervalID);
    moveright();
  }
});
