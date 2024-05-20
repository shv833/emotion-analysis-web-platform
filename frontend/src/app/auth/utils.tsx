import wretch from 'wretch'
import Cookies from 'js-cookie'
import { getApiBaseUrl, getBaseUrl } from '@/api/utils'

const base_url = getBaseUrl()
const api_url = getApiBaseUrl()

const base = wretch(base_url).accept('application/json')
const base_api = wretch(api_url).accept('application/json')

const storeToken = (token: string, type: 'access' | 'refresh') => {
  Cookies.set(type + 'Token', token)
}
const getToken = (type: string) => {
  return Cookies.get(type + 'Token')
}

const removeTokens = () => {
  Cookies.remove('accessToken')
  Cookies.remove('refreshToken')
}

// const register = (email: string, username: string, password: string) => {
//   return base_api.post({ email, username, password }, '/users/register/')
// }

const login = (username: string, password: string) => {
  return base_api.post({ username: username, password }, '/users/token/')
}

const logout = () => {
  const refreshToken = getToken('refresh')
  return base_api.post({ refresh: refreshToken }, '/users/logout/')
}

const handleJWTRefresh = () => {
  const refreshToken = getToken('refresh')
  return base_api.post({ refresh: refreshToken }, '/users/token/refresh/')
}

// const resetPassword = (email: string) => {
//   return base_api.post({ email }, '/auth/users/reset_password/')
// }

// const resetPasswordConfirm = (
//   new_password: string,
//   re_new_password: string,
//   token: string,
//   uid: string
// ) => {
//   return base_api.post(
//     { uid, token, new_password, re_new_password },
//     '/auth/users/reset_password_confirm/'
//   )
// }

export const AuthActions = () => {
  return {
    base_url,
    api_url,
    login,
    //   resetPasswordConfirm,
    handleJWTRefresh,
    //   register,
    //   resetPassword,
    storeToken,
    getToken,
    logout,
    removeTokens,
  }
}
