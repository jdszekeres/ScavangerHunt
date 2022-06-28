/*
https://github.com/gabmontes/fast-haversine for vanilla js
*/
const R = 6378137;
const PI_360 = Math.PI / 360;

function distance(a, b) {

  const cLat = Math.cos((a[0] + b[0]) * PI_360);
  const dLat = (b[0] - a[0]) * PI_360;
  const dLon = (b[1] - a[1]) * PI_360;

  const f = dLat * dLat + cLat * cLat * dLon * dLon;
  const c = 2 * Math.atan2(Math.sqrt(f), Math.sqrt(1 - f));

  return R * c;
}
function bearing (a,b) {
    return geolib.getGreatCircleBearing(
        { latitude: a[0], longitude: a[1] },
        { latitude: b[0], longitude: b[1] }
    );
}