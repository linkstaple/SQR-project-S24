function makeRequest(url, method, body) {
  const authToken = authManager.getToken()
  return fetch(`/api${url}`, {
    method,
    body: body ? JSON.stringify(body) : undefined,
    headers: {
      ...(authToken && {Authorization: `Bearer ${authToken}`}),
      ...(body && {'Content-Type': 'application/json'})
    }
  })
}

function fetchUsers() {
  return makeRequest('/users', 'GET')
}

const routeManager = {
  goToLogin() {
    location.href = location.origin + '/login'
  },
  goToRegister() {
    location.href = location.origin + '/register'
  },
  goToProfile() {
    location.href = location.origin + '/profile'
  },
  goToGroup(groupId) {
    location.href = location.origin + `/group/${groupId}`
  }
}

const AUTH_TOKEN_STORAGE_KEY = 'authorization_jwt_token'

const authManager = {
  getToken() {
    return localStorage.getItem(AUTH_TOKEN_STORAGE_KEY)
  },
  saveToken(token) {
    if (!token) {
      return
    }
    localStorage.setItem(AUTH_TOKEN_STORAGE_KEY, token)
  },
  clearToken() {
    localStorage.removeItem(AUTH_TOKEN_STORAGE_KEY)
  },
  logout() {
    this.clearToken()
    routeManager.goToLogin()
  }
}
