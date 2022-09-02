function postsList() {
   let container = document.createElement("div");
   container.classList.add(
      "container-fluid",
      "text-center",
      "mt-5",
      "row",
      "d-flex",
      "justify-content-evenly"
   );

   let title = document.createElement("h2");
   title.textContent = "Posts";

   let errorContainer = document.createElement("div");
   errorContainer.id = "error-container";

   let url = "/api/posts/";
   let header = {
      Authorization: `token ${getCookie("token")}`,
   };

   container.appendChild(title);
   container.appendChild(createPostForm());

   let postListContainer = document.createElement("div");
   postListContainer.classList.add(
      "col-10",
      "shadow",
      "my-5",
      "pb-5",
      "bg-body",
      "rounded"
   );
   postListContainer.id = "post-list-container";
   container.appendChild(postListContainer);

   makeRequest(url, header)
      .then(function (data) {
         for (let i = 0; i < data.length; i++) {
            let postData = data[i];

            post(postData);
         }
      })
      .catch(function (error) {
         console.error(error);
      });

   return container;
}

/**
 * A function to get a single post and add a div with the post title and
 * caption to the DOM
 * @param {Object} postData Post details
 */
function post(postData) {
   let title = document.createElement("button");
   title.classList.add("btn", "btn-link", "ps-0");
   title.textContent = postData.title;
   title.setAttribute("data-pk", postData.pk);

   title.onclick = function () {
      changePageContent(postDetails(title.dataset.pk));
   };

   let caption = document.createElement("p");
   caption.classList.add("my-1", "text-muted");
   caption.textContent = postData.caption;

   let container = document.createElement("div");
   container.classList.add(
      "my-4",
      "border",
      "border-secondary",
      "text-start",
      "rounded-end",
      "p-3",
      "pb-1"
   );
   container.appendChild(title);
   container.appendChild(caption);

   document.querySelector("#post-list-container").appendChild(container);
}

/**
 * Creates a form for adding a new post and addes it to the DOM
 * @returns object representing a HTML div element
 */
function createPostForm() {
   let form = document.createElement("form");
   form.enctype = "multipart/form-data";
   form.onsubmit = createPost;

   form.appendChild(formInput("title", "title"));
   form.appendChild(formInput("caption", "Caption"));

   let bodyLabel = document.createElement("label");
   bodyLabel.textContent = "Body";
   let body = document.createElement("textarea");
   body.rows = 4;
   body.name = "body";
   body.classList.add("w-100");

   form.appendChild(bodyLabel);
   form.appendChild(body);

   form.appendChild(formInput("image", "img", "file", "image/png, image/jpeg"));
   form.appendChild(
      buttonElement("Submit", null, "submit", "dark", true, 0, 2, 0, 2)
   );

   let containerDiv = document.createElement("div");
   containerDiv.classList.add(
      "d-flex",
      "col-10",
      "justify-content-center",
      "flex-column",
      "shadow",
      "mt-5",
      "bg-body",
      "rounded",
      "text-start"
   );

   let subTitle = document.createElement("h5");
   subTitle.classList.add("text-center", "mt-5", "mb-3");
   subTitle.textContent = "New post";

   let errorContainer = document.createElement("div");
   errorContainer.id = "error-container";

   containerDiv.appendChild(subTitle);
   containerDiv.appendChild(errorContainer);
   containerDiv.appendChild(form);

   return containerDiv;
}

/**
 * Function used to make a post request to the api to create a new post
 * @param {event} event Event passed to the function when form submits
 */
function createPost(event) {
   event.preventDefault();

   let formData = new FormData();
   formData.append("title", event.target[0].value);
   event.target[1].value != "" &&
      formData.append("caption", event.target[1].value);
   event.target[2].value != "" &&
      formData.append("body", event.target[2].value);
   event.target[3].files[0] != undefined &&
      formData.append("img", event.target[3].files[0]);

   let tokenStr = `token ${getCookie("token")}`;
   let header = { Authorization: tokenStr };
   let url = "/api/posts/";

   makeRequest(url, header, "POST", formData)
      .then(function (data) {
         console.log(data);
         // changePageContent(posts());
      })
      .catch(function (error) {
         console.error(error);
         document.querySelector("#error-container").textContent = error;
      });
}

function postDetails(pk) {
   let url = `/api/posts/${pk}/`;
   let header = { Authorization: `token ${getCookie("token")}` };

   makeRequest(url, header, "GET")
      .then(data => {
         let postContainer = document.createElement("div");
         postContainer.classList.add(
            "shadow",
            "rounded",
            "bg-body",
            "py-5",
            "col-10"
         );

         let postTitle = document.createElement("h3");
         postTitle.textContent = data.title;

         postContainer.appendChild(postTitle);
         postContainer.appendChild(postProfile(data.profile.id));

         if ("caption" in data && data["caption"] != null) {
            let postCaption = document.createElement("p");
            postCaption.classList.add("text-muted");
            postCaption.textContent = data.caption;
            postContainer.appendChild(postCaption);
         }

         if ("img" in data && data["img"] != null) {
            let postImage = document.createElement("img");
            postImage.src = data.img;
            postContainer.appendChild(postImage);
         }

         if ("body" in data && data["body"] != null) {
            let postBody = document.createElement("p");
            postBody.textContent = data.body;
            postContainer.appendChild(postBody);
         }
         container.appendChild(postContainer);
      })
      .catch(function (error) {
         console.error(error);
      });

   let container = document.createElement("div");
   container.classList.add(
      "text-center",
      "d-flex",
      "justify-content-center",
      "align-items-center",
      "flex-column"
   );

   let title = document.createElement("h3");
   title.classList.add("my-3");
   title.textContent = "Post details";
   container.appendChild(title);

   return container;
}

/**
 * Fetchs the profile details and returns a DOM element containing the user avatar and the user
 * @param {int} pk The primary key or id of the profile
 * @returns HTML div element
 */
function postProfile(pk) {
   let container = document.createElement("div");
   container.classList.add("d-flex", "justify-content-center", "flex-column");

   makeRequest(`/api/profile/${pk}`, {
      Authorization: `token ${getCookie("token")}`,
   })
      .then(function (data) {
         if (data.avatar != null) {
            let avatar = document.createElement("img");
            avatar.style.width = "120px";
            avatar.style.height = "120px";
            avatar.src = data.avatar;
            container.appendChild(avatar);
         } else {
            let avatar = document.createElement("div");
            avatar.classList.add("rounded-circle", "bg-dark", "mx-auto");
            avatar.style.width = "120px";
            avatar.style.height = "120px";
            container.appendChild(avatar);
         }

         let username = document.createElement("button");
         username.textContent = data.user.username;
         username.classList.add("my-3", "btn", "btn-link");

         username.onclick = function () {
            changePageContent(profileDetails(data.id));
         };

         container.appendChild(username);
      })
      .catch(function (error) {
         console.error(error);
      });
   return container;
}
