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

window.onload = function () {
   // get the root element from the html file
   let head = document.querySelector("#head");

   // create a nav bar
   head.appendChild(createNavbar());

   changePageContent(Home());
};

function changePageContent(content) {
   let root = document.querySelector("#root");
   root.innerHTML = "";
   root.appendChild(content);
}

function createNavbar() {
   // create a nav element
   let navElement = document.createElement("nav");
   // add bootstrap5 classes to the nav element
   navElement.classList.add(
      "navbar",
      "navbar-expand-md",
      "bg-dark",
      "navbar-dark"
   );

   // create a fluid container to contain the content of the navbar
   let container = document.createElement("div");
   container.classList.add("container-fluid");

   // create an anchor tag for the logo
   let realgramAnchor = document.createElement("button");
   realgramAnchor.classList.add(
      "navbar-brand",
      "ms-5",
      "nav-link",
      "btn",
      "btn-link"
   );
   realgramAnchor.style.cursor = "pointer";
   realgramAnchor.addEventListener("click", function () {
      changePageContent(Home());
   });

   realgramAnchor.textContent = "Realgram";

   // add logo anchor tag to the navbar container
   container.appendChild(realgramAnchor);

   // insert collapse button
   container.insertAdjacentHTML(
      "beforeend",
      `
         <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
         </button>
      `
   );

   let navListContainer = document.createElement("div");
   navListContainer.classList.add("collapse", "navbar-collapse");
   navListContainer.id = "navbarSupportedContent";

   let navUnorderedList = document.createElement("ul");
   navUnorderedList.classList.add("navbar-nav", "ms-auto", "mb-2", "mb-lg-0");

   navUnorderedList.appendChild(navItem("Home"));
   navUnorderedList.appendChild(navItem("Register"));
   navUnorderedList.appendChild(navItem("Login"));

   navListContainer.appendChild(navUnorderedList);

   container.appendChild(navListContainer);
   // add the fulid container to the navbar
   navElement.appendChild(container);
   // return the nav element to be added to the root element
   return navElement;
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

function Home() {
   let token = getCookie("token");
   if (token != undefined) {
      return posts();
   }

   let containerDiv = document.createElement("div");
   containerDiv.classList.add(
      "container-fluid",
      "d-flex",
      "justify-content-between",
      "align-items-center",
      "vh-100",
      "row"
   );

   // add hero section to the home screen
   containerDiv.appendChild(heroSection());

   // add the login form
   containerDiv.appendChild(LoginForm());

   return containerDiv;
}

function heroSection() {
   let heroSection = document.createElement("div");
   heroSection.classList.add(
      "col-md-7",
      "col-12",
      "d-flex",
      "justify-content-center"
   );

   let title = document.createElement("h3");
   title.classList.add(
      "text-nowrap",
      "text-uppercase",
      "fs-2",
      "fw-bold",
      "font-monospace",
      "text-center"
   );
   title.textContent = "Welcome to realgram";
   let caption = document.createElement("p");
   caption.classList.add(
      "text-nowrap",
      "text-uppercase",
      "fs-5",
      "fw-bold",
      "font-monospace",
      "text-muted",
      "text-center"
   );
   caption.textContent = "A place where families grow";

   let textContainer = document.createElement("div");

   textContainer.appendChild(title);
   textContainer.appendChild(caption);

   heroSection.appendChild(textContainer);
   return heroSection;
}

function LoginForm() {
   let form = document.createElement("form");
   form.classList.add("w-100");
   form.onsubmit = login;

   form.appendChild(formInput("Username", "username"));
   form.appendChild(formInput("Password", "password", "password"));

   form.appendChild(
      buttonElement("Submit", null, "submit", "secondary", true, 0, 2, 0, 2)
   );

   let formContainer = document.createElement("div");
   formContainer.classList.add(
      "col-12",
      "col-md-4",
      "d-flex",
      "flex-column",
      "align-items-center",
      "shadow",
      "p-3",
      "mb-5",
      "bg-body",
      "rounded"
   );
   let errorDiv = document.createElement("div");
   errorDiv.id = "error";

   formContainer.appendChild(errorDiv);
   formContainer.appendChild(form);

   formContainer.appendChild(
      buttonElement(
         "Create new account",
         function () {
            changePageContent(registerPage());
         },
         "button",
         "secondary",
         true,
         0,
         2
      )
   );
   return formContainer;
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
            changePageContent(posts());
         }
      });
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

function registerPage() {
   let containerDiv = document.createElement("div");
   containerDiv.classList.add(
      "container-fluid",
      "d-flex",
      "justify-content-between",
      "align-items-center",
      "vh-100",
      "row"
   );

   // add hero section to the home screen
   containerDiv.appendChild(heroSection());

   // add the login form
   containerDiv.appendChild(RegisterForm());

   return containerDiv;
}

function RegisterForm() {
   let form = document.createElement("form");
   form.id = "register-form";
   form.classList.add("w-100");
   form.enctype = "multipart/form-data";
   form.onsubmit = register;

   form.appendChild(formInput("Username", "username"));
   form.appendChild(formInput("Email address", "email", "email"));
   form.appendChild(formInput("First Name", "first_name"));
   form.appendChild(formInput("Last Name", "last_name"));
   form.appendChild(formInput("Password", "password", "password"));
   form.appendChild(
      formInput("Avatar", "avatar", "file", "image/png, image/jpeg")
   );
   // let hiddenFild = `<input type="hidden" name="_csrf" value="${}" />`;
   form.appendChild(
      buttonElement("Register", null, "submit", "dark", true, 0, 2, 0, 2)
   );

   let formContainer = document.createElement("div");
   formContainer.classList.add(
      "col-12",
      "col-md-4",
      "d-flex",
      "flex-column",
      "align-items-center",
      "shadow",
      "p-3",
      "mb-5",
      "bg-body",
      "rounded"
   );
   let errorDiv = document.createElement("div");
   errorDiv.id = "error";
   formContainer.appendChild(errorDiv);
   formContainer.appendChild(form);
   formContainer.appendChild(
      buttonElement(
         "Have an account, Login",
         function () {
            changePageContent(Home());
         },
         "button",
         "dark",
         true,
         0,
         2
      )
   );
   return formContainer;
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

   let csrfToken = getCookie("csrftoken");

   fetch("/api/profile/register/", {
      headers: {
         "X-CSRFToken": csrfToken,
      },
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

function posts() {
   let container = document.createElement("div");
   container.classList.add("container-fluid", "text-center");

   let title = document.createElement("h2");
   title.textContent = "Post List";

   container.appendChild(title);
   return container;
}
