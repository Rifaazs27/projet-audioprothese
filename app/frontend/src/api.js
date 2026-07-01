// Couche d'accès à l'API. La base est relative (/api) : en production le
// frontend et l'API sont exposés derrière le même Ingress.
const BASE = import.meta.env.VITE_API_BASE ?? ''

async function request(path, options = {}) {
  const resp = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!resp.ok) {
    const detail = await resp.text()
    throw new Error(`Erreur API ${resp.status} : ${detail}`)
  }
  if (resp.status === 204) return null
  return resp.json()
}

export const api = {
  listPatients: () => request('/api/patients'),
  getPatient: (id) => request(`/api/patients/${id}`),
  createPatient: (data) =>
    request('/api/patients', { method: 'POST', body: JSON.stringify(data) }),
  deletePatient: (id) => request(`/api/patients/${id}`, { method: 'DELETE' }),
  // Enregistrement d'un appareil auditif pour un patient
  addAppareil: (id, data) =>
    request(`/api/patients/${id}/appareils`, { method: 'POST', body: JSON.stringify(data) }),
  // Prise de rendez-vous pour un patient
  addRendezVous: (id, data) =>
    request(`/api/patients/${id}/rendez-vous`, { method: 'POST', body: JSON.stringify(data) }),
  // Liste globale des rendez-vous (triés par date)
  listRendezVous: () => request('/api/rendez-vous'),
}
