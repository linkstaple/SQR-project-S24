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
    body: JSON.stringify({
      username: userLogin,
      password: userPassword,
    }),
    headers: {
      "Content-Type": "application/json",
    },
  });

  if (registerResponse.status === 409) {
    alert(`Username "${userLogin}" is already taken`);
    return;
  }
  if (!registerResponse.ok) {
    alert("Unknown error");
    return;
  }

  //   location.href = window.location.origin + "/login";
}

function registerScript() {
  const submitButton = getAuthSubmitButton();
  submitButton.onclick = onSubmit;
}

registerScript();