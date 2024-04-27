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

  const loginResponse = await makeRequest('/login', 'POST', {
    username: userLogin,
    password: userPassword
  })

  if (loginResponse.status === 404) {
    alert('Invalid username or password')
    return
  }

  const {token} = await loginResponse.json()
  localStorage.setItem('authorization_token', token)
  location.href = location.origin + '/profile'
}

function loginScript() {
  const submitButton = getAuthSubmitButton()
  submitButton.onclick = onSubmit

  const registerButton = document.getElementById('action-button')
  registerButton.onclick = () => {
    window.location.href = window.location.origin + '/register'
  }
}

loginScript()
