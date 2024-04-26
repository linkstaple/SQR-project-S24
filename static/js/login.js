async function onSubmit() {
  const userLogin = getLoginValue();
  if (!userLogin) {
    alert("User login is not specified");
    return;
  }

  const userPassword = getPasswordValue();
  if (!userPassword) {
    alert("Password is not specified");
    return;
  }

  const loginResponse = await fetch("/api/login", {
    method: "POST",
    body: JSON.stringify({
      username: userLogin,
      password: userPassword,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (loginResponse.status === 404) {
    alert("Invalid username or password");
    return;
  }
}

function loginScript() {
  const submitButton = getAuthSubmitButton();
  submitButton.onclick = onSubmit;

  const registerButton = document.getElementById("auth-register-button");
  registerButton.onclick = () => {
    window.location.href = window.location.origin + "/register";
  };
}

loginScript();
