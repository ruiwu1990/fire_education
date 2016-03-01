$(document).ready(function(){ 
  // url for overlay image
  var imgURL;
  // TODO
  // need to grab this value from json
  var rectLatLngStart = new google.maps.LatLng(43.732738, -116.14286);
  var rectLatLngEnd = new google.maps.LatLng(43.729389, -116.13766);
  var map;
  var imageBounds;
  var imgOverlay;

  overlayImageOnMap();

  //google.maps.event.addDomListener(window, 'load', initialize);

  function initialize() {
    // imageBounds = new google.maps.LatLngBounds(
    //     rectLatLngStart,
    //     rectLatLngEnd);
    imageBounds = {
      // north is bigger than south, east is bigger than west
      north: 43.732738,
      south: 43.729389,
      east: -116.13766,
      west: -116.14286
    };


    var mapOptions = {
      zoom: 15,
      center: rectLatLngStart,
      mapTypeId: google.maps.MapTypeId.SATELLITE
    };

    map = new google.maps.Map(document.getElementById('googleMapDiv'),
        mapOptions);

    imgOverlay = new google.maps.GroundOverlay(
        imgURL,
        imageBounds);

    imgOverlay.setMap(map);
  }


  function overlayImageOnMap()
  {
    // should create map when myCanvas is fully done
    html2canvas(document.getElementById("myCanvas"), 
      {
        onrendered: function(canvas) {
          imgURL = canvas.toDataURL();
           // d3.select("#test").append("img")
           //  .attr('src',imgURL);
          google.maps.event.addDomListener(window, 'load', initialize);
          
          
        }
      }); 
  }


});