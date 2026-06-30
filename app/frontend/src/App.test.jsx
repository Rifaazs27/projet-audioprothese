import { render, screen, waitFor } from '@testing-library/react'
import { afterEach, beforeEach, expect, test, vi } from 'vitest'
import App from './App.jsx'

beforeEach(() => {
  globalThis.fetch = vi.fn(async () => ({
    ok: true,
    status: 200,
    json: async () => [
      { id: 1, nom: 'Martin', prenom: 'Claire', email: 'c@m.fr', appareils: [{ id: 1 }] },
    ],
  }))
})

afterEach(() => {
  vi.restoreAllMocks()
})

test('affiche le titre et la liste des patients', async () => {
  render(<App />)
  expect(screen.getByText(/Gestion des patients/i)).toBeDefined()
  await waitFor(() => expect(screen.getByText('Martin')).toBeDefined())
})
