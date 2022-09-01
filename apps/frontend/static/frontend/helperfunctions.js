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

   const form = new FormData(event.target);
   const formData = Object.fromEntries(form);

   fetch("/api/profile/authenticate/", {
      headers: { "Content-Type": "application/json" },
      method: "POST",
      body: JSON.stringify(formData),
   })
      .then(async function (response) {
         if (response.status !== 200) {
            let errorRes = await response.json();
            document.querySelector(
               "#error"
            ).textContent = `An error occurred - ${
               errorRes.error != undefined ? errorRes.error : ""
            }`;
            return;
         }
         return response.json();
      })
      .then(function (responseData) {
         if (responseData) {
            console.log(responseData.token);
            document.cookie = `token=${responseData.token}`;
            console.log(document.cookie);
            refreshNavBar();
            changePageContent(posts());
         }
      });
}

function register(event) {
   event.preventDefault();
   const formData = new FormData();

   formData.append("username", event.target[0].value);
   formData.append("email", event.target[1].value);
   formData.append("first_name", event.target[2].value);
   formData.append("last_name", event.target[3].value);
   formData.append("password", event.target[4].value);
   formData.append("avatar", event.target[5].files[0]);

   fetch("/api/profile/register/", {
      method: "POST",
      body: formData,
   })
      .then(function (response) {
         return response.json();
      })
      .then(function (responseData) {
         document.querySelector("#error").textContent = `An error occurred - ${
            responseData.error != undefined ? errorRes.error : ""
         }`;

         changePageContent(Home());
      })
      .catch(function (error) {
         console.error(error);
      });
}

async function makeRequest(url, header = null, method = "GET", data = null) {
   let response = await fetch(url, {
      headers: header == null ? {} : header,
      method,
      body: data,
   });

   return await response.json();
}
