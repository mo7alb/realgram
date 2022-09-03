/**
 * function to retrieve a chat room
 */
function getRoom(profileId) {
   makeRequest(`/api/message/room/${profileId}/`, getHeader(), "GET", null)
      .then(function (data) {
         console.log(data);
         if (data.error == "Room does not exists") {
            createRoom(profileId);
            return;
         }
         changePageContent(messagePage(data.slug, profileId));
      })
      .catch(function (error) {
         console.error(error);
      });
}

/**
 * Create a new room
 */
function createRoom(profileId) {
   const header = getHeader();
   header["Content-Type"] = "application/json";
   makeRequest(
      `/api/message/room/`,
      header,
      "POST",
      JSON.stringify({
         profile: profileId,
      })
   )
      .then(function (data) {
         getRoom(profileId);
      })
      .catch(function (error) {
         console.error(error);
      });
}

/**
 * displays a form to send messages and display all the messages
 */
function messagePage(slug, profileId) {
   const webSocket = new WebSocket(
      "wss://" + window.location.host + "/ws/" + slug + "/"
   );

   webSocket.onmessage = function (e) {
      const data = JSON.parse(e.data);
      displayMessage(data);
   };

   webSocket.onclose = function (e) {
      console.log("Chat socket closed");
   };

   const container = document.createElement("div");
   container.classList.add(
      "vh-100",
      "d-flex",
      "flex-column",
      "justify-content-end",
      "align-items-center"
   );

   const messageContainer = document.createElement("div");
   messageContainer.id = "messages";

   makeRequest("/api/message/" + slug, getHeader())
      .then(function (data) {
         for (let i = 0; i < data.length; i++) {
            displayMessage(data[i]);
         }
      })
      .catch(function (error) {
         console.log(error);
      });

   const form = document.createElement("form");
   form.classList.add("mb-5", "w-75");

   form.onsubmit = function (event) {
      event.preventDefault();
      const message = event.target[0].value;

      if (message == "") return;
      webSocket.send(JSON.stringify({ message: message, slug, profileId }));
      event.target[0].value = "";
   };

   const input = document.createElement("input");
   input.classList.add("col-7", "px-2", "py-2", "rounded");
   input.focus = true;

   const btn = document.createElement("button");
   btn.classList.add("btn", "btn-secondary", "col-4", "py-2");
   btn.type = "submit";
   btn.textContent = "Send";

   form.appendChild(input);
   form.appendChild(btn);

   container.appendChild(form);
   return container;
}

/**
 * adds message to the dom
 */
function displayMessage(data) {
   const messageContainer = document.createElement("div");
   const message = document.createElement("p");
   message.textContent = data.message;

   messageContainer.appendChild(message);
   document.querySelector("#messages").appendChild(messageContainer);
}
