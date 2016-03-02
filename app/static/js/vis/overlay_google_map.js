function overlayCanvasonGoogleMap(xllcorner,xurcorner,yllcorner,yurcorner)
{
  // url for overlay image
  var imgURL;
  // TODO
  // need to grab this value from json
  //var rectLatLngStart = new google.maps.LatLng(xllcorner, yurcorner);
  var rectLatLngStart = new google.maps.LatLng(39.028019, -114.21300990625019);
  var rectLatLngEnd = new google.maps.LatLng(xurcorner, yllcorner);
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
      north: -114.21300990625019,
      south: -114.323106,
      east: 39.028019,
      west: 38.983181122448883
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

}




