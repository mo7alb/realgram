/**
 * Function allows user to follow another users
 */
function followProfile(profileId) {
   console.log(profileId);
   let data = JSON.stringify({ follow: profileId });
   let header = getHeader();
   header["Content-Type"] = "application/json";
   console.log(header);
   makeRequest("/api/follow/", header, "POST", data)
      .then(function (data) {
         console.log(data);
         if (data.details == "Follow already exists") {
            alert("Already following user");
         } else {
            alert("Started Following user");
         }
      })
      .catch(function (error) {
         console.error(error);
      });
}
