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
                  function () {},
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

         if (data.same == true) {
            // form to update profile avatar
            let form = document.createElement("form");
            form.onsubmit = function (event) {
               updateProfile(event, profileId);
            };
            form.classList.add("form-inline");
            form.appendChild(formInput("Bio", "bio"));
            form.appendChild(
               formInput("Avatar", "avatar", "file", "image/png, image/jpeg")
            );
            form.appendChild(
               buttonElement(
                  "Update profile",
                  null,
                  "submit",
                  "secondary",
                  true,
                  2,
                  3
               )
            );
            let formContainer = document.createElement("div");
            formContainer.classList.add(
               "col-9",
               "my-5",
               "shadow",
               "rounded",
               "p-5"
            );
            formContainer.appendChild(form);
            container.appendChild(formContainer);
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

function updateProfile(event, profileId) {
   event.preventDefault();

   let formData = new FormData();
   event.target[0].value !== "" &&
      formData.append("bio", event.target[0].value);
   event.target[1].files[0] != undefined &&
      formData.append("avatar", event.target[1].files[0]);

   makeRequest(
      `/api/profile/${profileId}/`,
      {
         Authorization: `token ${getCookie("token")}`,
      },
      "PUT",
      formData
   )
      .then(function () {
         changePageContent(profileDetails(profileId));
      })
      .catch(function (error) {
         console.error(error);
      });
}
