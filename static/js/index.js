document.addEventListener("DOMContentLoaded", function () {
  const roomNameElement = document.getElementById("room-name");

  if (roomNameElement) {
    const roomName = JSON.parse(roomNameElement.textContent);

    if (roomName) {
      // WebSocket setup
      const notificationSocket = new WebSocket(
        "ws://" + window.location.host + "/ws/notification/" + roomName + "/"
      );

      notificationSocket.onmessage = function (e) {
        const data = JSON.parse(e.data);
        console.log(data);

        // Update HTML with WebSocket data
        updateNotification(data);
      };

      // AJAX function to fetch data
      // function fetchData() {
      //   fetch("/notifications/broadcast_notification/")
      //     .then(response => response.json())
      //     .then(data => updateNotification(data))
      //     .catch(error => console.error("Error fetching data:", error));
      // }

      // Update HTML function
      function updateNotification(data) {
        console.log(data)
        document.getElementById("notification_data").innerHTML += (`
          <div class="d-flex align-items-center mb-6"> 
            <div class="symbol symbol-40 symbol-light-primary mr-5">
              <span class="symbol-label"> 
                <i class="${data.message.icon ? data.message.icon : 'fas fa-bell fa-lg'}"></i> 
              </span> 
            </div>  
            <div class="d-flex flex-column font-weight-bold" > 
              <a href="#" class="text-dark text-hover-primary mb-1 font-size-lg">${data.message.title ? data.message.title : data.message.user}</a>  
              <span class="text-muted">${data.message.message}</span>  
            </div> 
          </div>
        `);
        document.getElementById("notification-badge").innerHTML =
          parseInt(document.getElementById("notification-badge").innerHTML) + 1;
      }

      // Fetch data initially
      // fetchData();

      // Set up an interval to fetch data periodically (every 5 seconds in this example)
      // setInterval(fetchData, 5000);

      notificationSocket.onclose = function (e) {
        console.error("WebSocket closed unexpectedly");
      };
    } else {
      console.error("Invalid roomName:", roomName);
    }
  } else {
    console.error("Element with ID 'room-name' not found.");
  }
});


