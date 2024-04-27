const authToken = authManager.getToken()
if (authToken) {
    routeManager.goToProfile()
} else {
    routeManager.goToLogin()
}
