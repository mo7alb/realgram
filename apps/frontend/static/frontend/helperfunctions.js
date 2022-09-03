window.onload = function () {
   // get the root element from the html file
   let head = document.querySelector("#head");

   // create a nav bar
   head.appendChild(createNavbar());

   changePageContent(Home());
};

function getCookie(cname) {
   let name = cname + "=";
   let cookies = document.cookie.split(";");

   for (let i = 0; i < cookies.length; i++) {
      let cookie = cookies[i].trim();

      if (cookie.startsWith(name)) {
         let keyValue = cookie.split("=");
         let returnVal = keyValue[1];
         if (returnVal[returnVal.length - 1] == ";") {
            returnVal = keyValue[1].slice(0, -1);
         }
         return returnVal;
      }
   }
}

function deleteCookie(name) {
   document.cookie = name + "=; Path=/; Expires=Thu, 01 Jan 1970 00:00:01 GMT;";
}

function getHeader() {
   let tokenStr = `token ${getCookie("token")}`;
   return {
      Authorization: tokenStr,
   };
}

function buttonElement(
   content,
   clickEvent,
   type = "button",
   color = "dark",
   outline = true,
   paddingX = 0,
   paddingY = 0,
   marginX = 0,
   marginY = 0
) {
   let btn = document.createElement("button");
   btn.textContent = content;

   if (clickEvent !== null) btn.addEventListener("click", clickEvent);

   let style = `btn${outline == true ? "-outline" : ""}-${color}`;
   btn.classList.add(
      "btn",
      style,
      `mx-${marginX}`,
      `my-${marginY}`,
      `px-${paddingX}`,
      `py-${paddingY}`,
      "w-100"
   );

   btn.type = type;

   return btn;
}

function navItem(content, clickEvent) {
   let listItem = document.createElement("li");
   listItem.classList.add("nav-item", "me-4");

   listItem.appendChild(
      buttonElement(content, clickEvent, "button", "light", true, 5, 2)
   );
   return listItem;
}

function formInput(label, htmlFor, type = "text", accepts = null) {
   let inputDiv = document.createElement("div");
   inputDiv.classList.add("mb-3");

   let inputLabel = document.createElement("label");
   inputLabel.textContent = label;
   inputLabel.classList.add("form-label");
   inputLabel.setAttribute("for", htmlFor);
   inputDiv.appendChild(inputLabel);

   let input = document.createElement("input");
   input.type = type;
   input.classList.add("form-control", "w-100");
   input.id = htmlFor;
   input.name = htmlFor;
   if (accepts !== null) input.accept = accepts;

   inputDiv.appendChild(input);

   return inputDiv;
}

function refreshNavBar() {
   // get the root element from the html file
   let head = document.querySelector("#head");
   head.innerHTML = "";
   // create a nav bar
   head.appendChild(createNavbar());
}

function changePageContent(content) {
   let root = document.querySelector("#root");
   root.innerHTML = "";
   root.appendChild(content);
}

function login(event) {
   event.preventDefault();

   const formData = new FormData(event.target);
   formData.append("username", event.target[0].value);
   formData.append("password", event.target[1].value);

   makeRequest("/api/profile/authenticate/", null, "POST", formData)
      .then(function (data) {
         document.cookie = `token=${data.token};`;
         refreshNavBar();
         changePageContent(postsList());
      })
      .catch(function (error) {
         document.querySelector("#error").textContent = error;
      });
}

function register(event) {
   event.preventDefault();
   const formData = new FormData();

   event.target[0].value && formData.append("username", event.target[0].value);
   event.target[1].value && formData.append("email", event.target[1].value);
   event.target[2].value &&
      formData.append("first_name", event.target[2].value);
   event.target[3].value && formData.append("last_name", event.target[3].value);
   event.target[4].value && formData.append("password", event.target[4].value);
   event.target[5].files[0] &&
      formData.append("avatar", event.target[5].files[0]);

   makeRequest("/api/profile/register/", null, "POST", formData)
      .then(function (data) {
         changePageContent(Home());
      })
      .catch(function (error) {
         console.log(error);
         document.querySelector(
            "#error"
         ).textContent = `An error occurred - ${error.message}`;
      });
}

async function makeRequest(url, header = null, method = "GET", data = null) {
   let response =
      header == null
         ? await fetch(url, {
              method,
              body: data,
           })
         : await fetch(url, {
              headers: header,
              method,
              body: data,
           });
   if (response.status == 201) {
      return response.statusText;
   } else if (!response.headers.get("content-type")) {
      return response;
   } else {
      return await response.json();
   }
}
