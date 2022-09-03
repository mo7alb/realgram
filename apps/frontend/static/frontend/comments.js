/**
 * Function to create a form that creates a new comment
 */
function commentForm(postId) {
   let form = document.createElement("form");
   form.onsubmit = function (event) {
      submitComment(event, postId);
   };
   form.appendChild(formInput("Comment", "comment"));
   form.appendChild(
      buttonElement("Submit", null, "submit", "secondary", true, 0, 2)
   );

   let formContainer = document.createElement("div");
   formContainer.classList.add("mb-5", "shadow", "p-3", "rounded", "col-10");

   let errorContainer = document.createElement("div");
   errorContainer.id = "error";

   formContainer.appendChild(errorContainer);
   formContainer.appendChild(form);

   return formContainer;
}

/**
 * Funtion to submit a comment to the api
 * @param {Event Object} event Form submit event
 * @param {int} postId Post to which the comment is created
 * @returns undefined
 */
function submitComment(event, postId) {
   event.preventDefault();
   if (event.target[0].value == "") {
      document.querySelector("#error").textContent = "Comment is required";
      return;
   }

   let formData = new FormData();
   formData.append("message", event.target[0].value);
   formData.append("post", postId);

   makeRequest("/api/comments/", getHeader(), "POST", formData)
      .then(function () {
         changePageContent(postDetails(postId));
      })
      .catch(function (error) {
         console.error(error);
      });
}

/**
 * Fetchs a list of comments and adds them to a div and returns the div
 * @param {int} postId id of the post for which the comments are to be fetched
 * @returns Object representing the HTML div element
 */
function comments(postId) {
   let container = document.createElement("div");
   container.classList.add("mb-5", "shadow", "p-3", "rounded", "col-10");

   makeRequest(`/api/comments/${postId}`, getHeader())
      .then(function (data) {
         if (data.length == 0) {
            container.textContent = "No comments yet";
            return;
         }
         for (let i = 0; i < data.length; i++) {
            let comment = document.createElement("h6");
            comment.textContent = data[i].message;
            let commentDiv = document.createElement("div");
            commentDiv.classList.add(
               "border-bottom",
               "border-bottom",
               "border-2",
               "mb-4"
            );
            commentDiv.appendChild(comment);
            container.appendChild(commentDiv);
         }
      })
      .catch(function (error) {
         console.error(error);
      });

   return container;
}
