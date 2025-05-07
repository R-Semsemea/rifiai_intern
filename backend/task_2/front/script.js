let form = document.querySelector("form");
let submitButton = document.getElementById("submit-btn");

$(document).ready(function () {
  form.addEventListener("submit", handleSubmit);
});

function handleSubmit(event) {
  event.preventDefault();
  submitButton.disabled = true;
  submitButton.value = "...";

  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());
  const jsonData = JSON.stringify(data);

  console.log("Form Data Submitted: ", jsonData);
  signUp(jsonData);
}

function signUp(jsonData) {
  localStorage.setItem("refresh", "true");

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 30000);

  fetch("http://127.0.0.1:5000/register", {
    method: "POST",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
    },
    body: jsonData,
    signal: controller.signal,
  })
    .then(async (response) => {
      clearTimeout(timeout);
      const result = await response.json();

      if (!response.ok) {
        throw new Error(result.message || "Registration failed");
      }

      return result;
    })
    .then((result) => {
      console.log("Server Response:", result);

      showResponse("Success", result.message);
      if (result.email_sent) {
        console.log("Welcome email was sent");
      } else {
        console.log("Welcome email was not sent");
      }
      location.reload();
    })
    .catch((error) => {
      console.error("Error:", error);

      showResponse("Error", error.message);
    })
    .finally(() => {
      submitButton.disabled = false;
      submitButton.value = "Register";
    });
}

function showResponse(status, message) {
  alert(`${status}: ${message}`);
}
