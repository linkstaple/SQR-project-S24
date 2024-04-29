export const users = {
  michael: {
    name: 'michael',
    password: '1'
  },
  andrew: {
    name: 'andrew',
    password: '2'
  },
  timur: {
    name: 'timur',
    password: '3'
  }
}

const APP_PORT = process.env.BIND_PORT
const BASE_URL = `http://127.0.0.1:${APP_PORT}`

export const pages = {
  root: BASE_URL + '/',
  login: BASE_URL + '/login',
  register: BASE_URL + '/register',
  profile: BASE_URL + '/profile'
}
