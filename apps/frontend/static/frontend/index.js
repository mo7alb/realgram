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

   let token = getCookie("token");
   if (token == undefined) {
      navUnorderedList.appendChild(navItem("Register"));
      navUnorderedList.appendChild(navItem("Login"));
   } else {
      navUnorderedList.appendChild(
         navItem("Logout", function () {
            let token = getCookie("token");
            let authString = `token ${token}`;
            console.log(authString);
            fetch("/api/profile/logout/", {
               headers: {
                  Authorization: authString,
               },
               method: "POST",
            }).then(function (response) {
               if (response.status == 200) {
                  deleteCookie("token");
                  refreshNavBar();
                  changePageContent(Home());
               }
            });
         })
      );
   }

   navListContainer.appendChild(navUnorderedList);

   container.appendChild(navListContainer);
   // add the fulid container to the navbar
   navElement.appendChild(container);
   // return the nav element to be added to the root element
   return navElement;
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
