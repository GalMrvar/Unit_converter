jQuery(document).ready(function($) {
function whichAnimationEvent(){
  var t,
      el = document.createElement("fakeelement");

  var animations = {
    "animation"      : "animationend",
    "OAnimation"     : "oAnimationEnd",
    "MozAnimation"   : "animationend",
    "WebkitAnimation": "webkitAnimationEnd"
  }

  for (t in animations){
    if (el.style[t] !== undefined){
      return animations[t];
    }
  }
}
if (sessionStorage.getItem("loading") != 1) {
	
var animationEvent = whichAnimationEvent();
  $("#content").hide();
  $("#overlay").show();
  $("#loading").addClass("animation");
  $("#loading").one(animationEvent,
              function(event) {
    $("#overlay").delay(500).hide(200);
	setTimeout(function() {
		window.location.href = "index.html";
	}, 700);
  });
}
});