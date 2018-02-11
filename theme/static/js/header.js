//script for opening/closing of sidebar on mobiles and ensuring it is visible if the viewport is enlarged beyond the mobile view
window.addEventListener("load", function() {
  var leftCol = document.getElementsByClassName("left-col")[0];
  var centreCol = document.getElementsByClassName("center-col")[0];
  var sidebarCloser = document.getElementsByClassName("sidebar-closer")[0];
  document.getElementsByClassName('banner')[0].addEventListener('click', function() {
    if (window.innerWidth < 750) {
      if ((leftCol.style.marginLeft == "" && window.getComputedStyle(leftCol).marginLeft == "-185px") || leftCol.style.marginLeft == "-185px") {
        leftCol.style.marginLeft = "0";
        document.getElementsByClassName("center-col")[0].style.marginLeft = "185px";
        centreCol.style.marginRight = "-185px";
        sidebarCloser.style.display = "block";
      } else {
        leftCol.style.marginLeft = "-185px";
        centreCol.style.marginLeft = "0";
        centreCol.style.marginRight = "0";
        sidebarCloser.style.display = "none";
      }
    }
  }, false);
  
  document.getElementsByClassName('sidebar-closer')[0].addEventListener('click', function() {
    if (window.innerWidth < 750) {
      leftCol.style.marginLeft = "-185px";
      centreCol.style.marginLeft = "0";
      centreCol.style.marginRight = "0";
      sidebarCloser.style.display = "none";
    }
  }, false);

  window.addEventListener('resize', function() {
    if (window.innerWidth > 750) {
      leftCol.removeAttribute('style');
      centreCol.removeAttribute('style');
      sidebarCloser.style.display = "none";
    }
  });

}, false);
