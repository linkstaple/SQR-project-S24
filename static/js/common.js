function makeRequest(url, method, body) {
  const authToken = localStorage.getItem('authorization_token')
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
