import { API_URL, DOMAIN, PORT, SCHEMA } from '@/constants'

function getApiBaseUrl() {
  const portPart = PORT ? `:${PORT}` : ''
  return `${SCHEMA}${DOMAIN}${portPart}${API_URL}`
}

function getBaseUrl() {
  const portPart = PORT ? `:${PORT}` : ''
  return `${SCHEMA}${DOMAIN}${portPart}`
}

export { getApiBaseUrl, getBaseUrl }
