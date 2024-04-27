async function onSubmit() {
  const userLogin = getLoginValue()
  if (!userLogin) {
    alert('User login is not specified')
    return
  }

  const userPassword = getPasswordValue()
  if (!userPassword) {
    alert('Password is not specified')
    return
  }

  const registerResponse = await makeRequest('/register', 'POST', {
    username: userLogin,
    password: userPassword
  })

  if (registerResponse.status === 409) {
    alert(`Username "${userLogin}" is already taken`)
    return
  }
  if (!registerResponse.ok) {
    alert('Unknown error')
    return
  }

  const {token} = await registerResponse.json()
  authManager.saveToken(token)
  routeManager.goToProfile()
}

function registerScript() {
  const submitButton = getAuthSubmitButton()
  submitButton.onclick = onSubmit

  const registerButton = document.getElementById('action-button')
  registerButton.onclick = routeManager.goToLogin
}

registerScript()
