function posts() {
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

   makeRequest(url, header).then(function (data) {
      for (let i = 0; i < data.length; i++) {
         let post = data[i];

         createPost(post);
      }
   });

   container.appendChild(title);
   container.appendChild(createPostForm());

   return container;
}

function createPost(post) {
   console.log(post);
   let title = document.createElement("h5");
   title.textContent = post.title;

   let caption = document.createElement("p");
   caption.classList.add("my-1", "text-muted");
   caption.textContent = post.caption;

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

   console.log(document.querySelector("#root").firstChild);
}

function createPostForm() {
   let form = document.createElement("form");
   form.enctype = "multipart/form-data";
   form.onsubmit = post;

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
      "my-5",
      "pb-5",
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
function post(event) {
   event.preventDefault();

   let formData = new FormData();
   formData.append("title", event.target[0].value);
   event.target[1].value != "" &&
      formData.append("caption", event.target[1].value);
   event.target[2].value != "" &&
      formData.append("body", event.target[2].value);
   event.target[3].files[0] != undefined &&
      formData.append("img", event.target[3].files[0]);

   let token = getCookie("token");

   fetch("/api/posts/", {
      headers: {
         Authorization: `token ${token}`,
      },
      method: "POST",
      body: formData,
   })
      .then(function (response) {
         return response.json();
      })
      .then(function (responseData) {
         console.log(responseData);
      });
}
