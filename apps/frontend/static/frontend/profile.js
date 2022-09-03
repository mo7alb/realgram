/**
 * A function to fetch a user and display its details
 * @param {int} profileId Id of the profile to be fetched
 * @returns A HTML div element containing the profile details
 */
function profileDetails(profileId) {
   makeRequest(`/api/profile/${profileId}`, {
      Authorization: `token ${getCookie("token")}`,
   })
      .then(function (data) {
         let username = document.createElement("h6");
         username.textContent = `Username: ${data.user.username}`;
         container.appendChild(username);

         if (data.same == true) {
            // display user email
            let email = document.createElement("h6");
            email.textContent = `Email: ${data.user.email}`;
            container.appendChild(email);
         }

         if (data.bio != null) {
            // display profile bio
            let bio = document.createElement("p");
            bio.textContent = `Bio: ${data.bio}`;
            container.appendChild(bio);
         }

         if (data.avatar != null) {
            // display profile bio
            let avatar = document.createElement("img");
            avatar.classList.add("w-50", "mx-auto");
            avatar.src = data.avatar;
            container.appendChild(avatar);
         }

         if (data.same == false) {
            // send messages to user
            let buttonContainer = document.createElement("div");
            buttonContainer.classList.add("col-7", "mb-5");

            buttonContainer.appendChild(
               buttonElement(
                  `Message ${data.user.username}`,
                  function () {
                     getRoom(profileId);
                  },
                  "button",
                  "dark",
                  true,
                  0,
                  2,
                  0,
                  3
               )
            );
            // follow user
            buttonContainer.appendChild(
               buttonElement(
                  `Follow ${data.user.username}`,
                  function () {
                     followProfile(profileId);
                  },
                  "button",
                  "dark",
                  true,
                  0,
                  2,
                  0,
                  1
               )
            );
            container.appendChild(buttonContainer);
         }
      })
      .catch(function (error) {
         console.error(error);
      });

   let container = document.createElement("div");
   container.classList.add(
      "d-flex",
      "flex-column",
      "justify-content-center",
      "align-items-center"
   );
   let pageTitle = document.createElement("h3");
   pageTitle.textContent = "Profile details";
   pageTitle.classList.add("text-center", "my-5");
   container.appendChild(pageTitle);
   return container;
}
