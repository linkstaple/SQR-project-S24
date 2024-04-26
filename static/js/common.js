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
