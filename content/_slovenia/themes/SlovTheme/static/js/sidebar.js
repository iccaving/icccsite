
$(window).load(function() {
  var sbsection_search = "sbsection=";
  var sbsubsection_search = "sbsubsection=";
  var sbsection;
  var sbsubsection;
  var ca = document.cookie.split(';');
  for(var i=0; i<ca.length; i++) {
      var c = ca[i];
      while (c.charAt(0)==' ') c = c.substring(1);
      if (c.indexOf(sbsection_search) != -1) sbsection = c.substring(sbsection_search.length,c.length);
      if (c.indexOf(sbsubsection_search) != -1) sbsubsection = c.substring(sbsubsection_search.length,c.length);
  }
  if (sbsection != null) {
    var outerelement = $('#' + sbsection + '-outer');
    outerelement.css({
      'max-height': ''
    });
    outerelement.removeClass("collapsed");

    var innerelement = $('#' + sbsection + '-inner');
    innerelement.removeClass("nodisplay");
  }

  if (sbsubsection != null) {
    var outerelement = $('#' + sbsection + '-sub-outer-' + sbsubsection);
    outerelement.css({
      'max-height': ''
    });
    outerelement.removeClass("collapsed");

    var innerelement = $('#' + sbsection + '-sub-inner-' + sbsubsection);
    innerelement.removeClass("nodisplay");
  }
  //document.cookie = 'sbsection=' + ';Path=/rcc/caving/;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
  //document.cookie = 'sbsubsection=' + ';Path=/rcc/caving/;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
});

$(function() {
  $('div.sidebar-item, div.sidebar-sub-item').click(function() {
    //Check if in sub-menu. If so then set max-height of outer menu to default so it expands nicely with the sub menu transition.
    if ($(this).data("upidouter") != null && $(this).data("upidinner")) {
      var outer = $(this).data("upidouter");
      var inner = $(this).data("upidinner");
      var outerelement = $('#' + outer);
      var innerelement = $('#' + inner);
      if (!outerelement.hasClass('collapsed')) {
        //var newheight = parseInt(outerelement.css('max-height'), 10) + height;
        outerelement.css({
          'max-height': ''
        });
      }
    }

    var outer = $(this).data("idouter");
    var inner = $(this).data("idinner");
    var outerelement = $('#' + outer);
    var innerelement = $('#' + inner);

    // To prevent the menu from lagging on mobile devices, the inners are set to
    // display: none so this removes the nodisplay class for opening before the
    // the item opens so the css transition works
    var displayToggled = false;
    if (outerelement.hasClass('collapsed')) {
      innerelement.removeClass('nodisplay');
      displayToggled = true;
     }

    //Ensure that outer element knows the inner height
    //Needed to undo the sub-menus attribute removal from above
    var height = innerelement.outerHeight();
    outerelement.css({
      'max-height': (parseInt(height)).toString() + 'px'
    });
    //If collapsing, set max-height to 0. Delay to allow transition to work because we only just set the max-height
    if (!outerelement.hasClass('collapsed')) {
      setTimeout(function() {
        outerelement.css({
          'max-height': '0px'
        });
      }, 50);
    }
    outerelement.toggleClass('collapsed');

    // For collapsing items the inner elements are set back to nodisplay. Happens
    // after collapse so css transition works
    if (displayToggled == false) {
      setTimeout(function() {
        innerelement.addClass('nodisplay');
      }, 500);
    }

    //Collapse all sub menus when a menu is collapsed
    //Delay ensures outer transition looks nice
    if (outerelement.hasClass('collapsed')) {
      setTimeout(function() {
        outerelement.find(".sidebar-outer").addClass('collapsed').css({
          'max-height': '0px'
        });
        //alert("yo");
        outerelement.find(".sidebar-inner").each(function() {
          if (!$(this).hasClass("nodisplay")) {
            $(this).addClass('nodisplay');
          };
        });
      }, 400);
    }

    /*Script to remember sidebar submenu state and reopen things when you move
    to a trip report*/
    /*check if in a submenu*/
    if ($(this).data("upidouter") != null && $(this).data("upidinner")) {
      /*if yes get the id of the drawer wrappers, find them, also extract the section
      and sub section from them*/
      var upouter = $(this).data("upidouter");
      var sbsection = upouter.replace("-outer", "");
      var outer = $(this).data("idouter");
      var sbsubsection = outer.replace(sbsection + "-sub-outer-", "");
      var upouterelement = $('#' + upouter);
      var outerelement = $('#' + outer);

      /*If you're openeing a section/subsecton record it with a cookie
      if closing, delete that cookie*/
      if (!upouterelement.hasClass('collapsed')) {
        document.cookie = 'sbsection=' + sbsection  + ';Path=/rcc/caving/;';
      }
      else {
        document.cookie = 'sbsection=' + sbsection  + ';Path=/rcc/caving/;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
      }
      if (!outerelement.hasClass('collapsed')) {
        document.cookie = 'sbsubsection=' + sbsubsection  + ';Path=/rcc/caving/;';
      }
      else {
        document.cookie = 'sbsubsection=' + sbsubsection  + ';Path=/rcc/caving/;expires=Thu, 01 Jan 1970 00:00:01 GMT;';
      }
    }
    else {
      /*Same as above but if there's no subsection*/
      var outer = $(this).data("idouter");
      var sbsection = outer.replace("-outer", "");
      var outerelement = $('#' + outer);
      if (!outerelement.hasClass('collapsed')) {
        document.cookie = 'sbsection=' + sbsection  + ';Path=/rcc/caving/;';
      }
      else {
        document.cookie = 'sbsection=' + sbsection  + ';Path=/rcc/caving/;expires=Thu, 01 Jan 1970 00:00:01 GMT;';;
      }
    }

    //The scrollbar appearing can cause some elements to flow onto another line. This increses the size of the inner
    //and can oveflow out of the outer. This ensures that at the end of a menu openeing, overflowing elements
    //are adjusted.
    var outer = $(this).data("idouter");
    var outerelement = $('#' + outer);
    outerelement.one('webkitTransitionEnd otransitionend oTransitionEnd msTransitionEnd transitionend', function(e) {
      $(".sidebar-outer").each(function() {
        if ($(this).prop('scrollHeight') > $(this).height() && !($(this).hasClass("collapsed"))) {
          height  = $(this).children(".sidebar-inner").outerHeight()
          $(this).css({'max-height':height});
        }
      });
    });
  });
});
