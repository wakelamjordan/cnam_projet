/**
 * Récupère les données associées à un cookie
 * @param {string} name Nom du cookie à récupérer
 * @return {string|null}
 */
function GetCookie({name}) {
  const cookies = document.cookie.split("; ");
  const value = cookies.find((c) => c.startsWith(name + "="))?.split("=")[1];
  if (value === undefined) {
    return null;
  }
  return decodeURIComponent(value);
}

export default GetCookie;
