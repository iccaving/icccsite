// Check for stored sidebar state and if exists open specified sidebar elements
function load() {
  list = window.localStorage.getItem("sidebar").split(',');
  if (list != null) {
    var outers = document.querySelectorAll(".sidebar-outer");
    for (var i=0; i < outers.length; i++) {
      if (list[i] == 1) {
        outers[i].children[0].classList.remove("nodisplay");
        outers[i].classList.remove("collapsed");
        outers[i].style.maxHeight = outers[i].children[0].offsetHeight + "px";
        adjustHeights(outers[i], outers[i].children[0].offsetHeight);
      }
    }
  }
};
// Store the currently open sidebar elements as a list of 1s and 0s
function store() {
  var outers = document.querySelectorAll(".sidebar-outer");
  var list = []
  for (var i=0; i < outers.length; i++) {
    if (outers[i].classList.contains("collapsed")) {
      list.push(0);
    } else {
      list.push(1);
    };
  };
  window.localStorage.setItem("sidebar", list);
};
// Recursively look at parent elements and add height of newly opened element
// to any parent outer container. Stop at sidebar element.
function adjustHeights(element, amount) {
  outer = element.parentElement
  if (outer.classList.contains("sidebar-outer")) {
    outer.style.maxHeight = parseInt(outer.style.maxHeight) + amount  + "px";
    adjustHeights(outer, amount);
  } else if (!outer.classList.contains("sidebar")) {
    adjustHeights(outer, amount);
  }
}

// Var to prevent rapid sidebar item opening/closing from breaking things
var go = true;

function clicked(event) {
  if (go) {
    go = false
    var outerContainer =  event.target.parentElement.nextSibling.nextSibling;
    var innerContainer = outerContainer.children[0];
    var transitionEvent = whichTransitionEvent();
    transitionEvent && outerContainer.addEventListener(transitionEvent, function(event) {
      if (event.target.classList.contains("collapsed")) {
        event.target.children[0].classList.add("nodisplay");
        outers = event.target.children[0].querySelectorAll(".sidebar-outer");
        inners = event.target.children[0].querySelectorAll(".sidebar-inner");
        for (var i=0; i < outers.length; i++) {
          outers[i].style.maxHeight = 0;
          outers[i].classList.add("collapsed");
          inners[i].classList.add("nodisplay");
        }
      }
      go = true
    });

    if (innerContainer.classList.contains("nodisplay")) {
      innerContainer.classList.remove("nodisplay");
      outerContainer.style.maxHeight = innerContainer.offsetHeight + "px";
      outerContainer.classList.remove("collapsed");
    } else {
      outerContainer.style.maxHeight = "0";
      outerContainer.classList.add("collapsed");
    }
    adjustHeights(event.target, innerContainer.offsetHeight);
    store();
  }
}

window.addEventListener("load", function() {
  var divs = document.querySelectorAll('.expandable-menu');
  for (var i = 0; i < divs.length; i++) {
    divs[i].addEventListener("click", clicked, false);
  }
  load();
}, false);

// Helper function for detecting when css transitions are over
function whichTransitionEvent(){
    var t;
    var el = document.createElement('fakeelement');
    var transitions = {
      'transition':'transitionend',
      'OTransition':'oTransitionEnd',
      'MozTransition':'transitionend',
      'WebkitTransition':'webkitTransitionEnd'
    }
    for(t in transitions){
        if( el.style[t] !== undefined ){
            return transitions[t];
        }
    }
}
