/*
https://github.com/gabmontes/fast-haversine for vanilla js
*/
const R = 6378137;
const PI_360 = Math.PI / 360;

function bad(a, b) {

  const cLat = Math.cos((a[0] + b[0]) * PI_360);
  const dLat = (b[0] - a[0]) * PI_360;
  const dLon = (b[1] - a[1]) * PI_360;

  const f = dLat * dLat + cLat * cLat * dLon * dLon;
  const c = 2 * Math.atan2(Math.sqrt(f), Math.sqrt(1 - f));
  console.log([cLat,dLat,dLon,f,c,R*c])
  return R * c;
}
function bearing (a,b) {
    return geolib.getGreatCircleBearing(
        { latitude: a[0], longitude: a[1] },
        { latitude: b[0], longitude: b[1] }
    );
}
function distance(a,b) {

  var R = 6371000; 
  const dLat = (b[0] - a[0]) * PI_360;
  const dLon = (b[1] - a[1]) * PI_360;
  var a = 
    Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.cos(deg2rad(lat1)) * Math.cos(deg2rad(lat2)) * 
    Math.sin(dLon/2) * Math.sin(dLon/2)
    ; 
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
  var d = R * c; // Distance in km
  return d;
}
function distance(a,b) {
  lat1=a[0]
  lat2=b[0]
  lon1=a[1]
  lat1=b[1]
  var p = 0.017453292519943295;    // Math.PI / 180
  var c = Math.cos;
  var a = 0.5 - c((lat2 - lat1) * p)/2 + 
          c(lat1 * p) * c(lat2 * p) * 
          (1 - c((lon2 - lon1) * p))/2;

  return 12742 * Math.asin(Math.sqrt(a)); // 2 * R; R = 6371 km
}
function deg2rad(deg) {
  return deg * (Math.PI/180)
}
function calcCrow(lat1, lon1, lat2, lon2) 
{
  var R = 6371000; // m
  var dLat = toRad(lat2-lat1);
  var dLon = toRad(lon2-lon1);
  var lat1 = toRad(lat1);
  var lat2 = toRad(lat2);

  var a = Math.sin(dLat/2) * Math.sin(dLat/2) +
    Math.sin(dLon/2) * Math.sin(dLon/2) * Math.cos(lat1) * Math.cos(lat2); 
  var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1-a)); 
  var d = R * c;
  console.log(d);
  return d;
}

// Converts numeric degrees to radians
function toRad(Value) 
{
    return Value * Math.PI / 180;
}