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

  const registerResponse = await fetch("/api/register", {
    method: "POST",
    body: {
      username: userLogin,
      password: userPassword,
    },
  });
  if (registerResponse.status === 409) {
    alert("username taken");
    return;
  }

  location.href = window.location.origin + "/login";
}

function registerScript() {
  const submitButton = getAuthSubmitButton();
  submitButton.onclick = onSubmit;
}

registerScript();
