//document.addEventListener('DOMContentLoaded', function() {
//window.addEventListener('load', function() {

//TopScript 및 TopStyle이 로딩 되어있지 않으면 로딩
if (typeof submitAction === "undefined") {

	// alert("undefined *********************************************");
	var head = document.head || document.getElementsByTagName('head')[0];

	// linkTop
	var linkTop = document.createElement('link');
	linkTop.setAttribute("rel", "stylesheet")
	linkTop.setAttribute("type", "text/css")
	linkTop.setAttribute("href", "/_templates/_css/_css.css")
	linkTop.async = true;
	// head.insertBefore(linkTop, head.firstChild);
	head.appendChild(linkTop);
	linkTop.onload = function() {
	};

	// scriptTop
	var scriptTop = document.createElement('script');
	scriptTop.setAttribute("type", "text/javascript");
	scriptTop.setAttribute("src", "/_templates/_js/_js.js");
	scriptTop.async = true;
	// head.insertBefore(scriptTop, head.firstChild);
	head.appendChild(scriptTop);

	scriptTop.onload = function() {
		Array.prototype.slice.call(document.getElementsByName("autoRun"))
				.forEach(function(item) {
					submitAction(item);
					item.setAttribute('name', 'autoRunFinish');
				});
	};
} else {
	Array.prototype.slice.call(document.getElementsByName("autoRun")).forEach(
			function(item) {
				submitAction(item);
				item.setAttribute('name', 'autoRunFinish');
			});
}
// });

