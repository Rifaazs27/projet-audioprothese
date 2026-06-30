import { useEffect, useState } from 'react'
import { api } from './api'

const champsVides = { nom: '', prenom: '', email: '', telephone: '' }

export default function App() {
  const [patients, setPatients] = useState([])
  const [form, setForm] = useState(champsVides)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  async function charger() {
    setLoading(true)
    try {
      setPatients(await api.listPatients())
      setError(null)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    charger()
  }, [])

  async function ajouter(e) {
    e.preventDefault()
    try {
      const payload = { ...form, email: form.email || null, telephone: form.telephone || null }
      await api.createPatient(payload)
      setForm(champsVides)
      await charger()
    } catch (e) {
      setError(e.message)
    }
  }

  async function supprimer(id) {
    try {
      await api.deletePatient(id)
      await charger()
    } catch (e) {
      setError(e.message)
    }
  }

  return (
    <>
      <header>
        <h1>Cabinet d'audioprothèse — Gestion des patients</h1>
        <p>MVP DevOps · API FastAPI · supervision Prometheus/Grafana</p>
      </header>
      <main>
        <section className="card">
          <h2>Nouveau patient</h2>
          <form onSubmit={ajouter}>
            <label>
              Nom
              <input
                required
                value={form.nom}
                onChange={(e) => setForm({ ...form, nom: e.target.value })}
              />
            </label>
            <label>
              Prénom
              <input
                required
                value={form.prenom}
                onChange={(e) => setForm({ ...form, prenom: e.target.value })}
              />
            </label>
            <label>
              Email
              <input
                type="email"
                value={form.email}
                onChange={(e) => setForm({ ...form, email: e.target.value })}
              />
            </label>
            <label>
              Téléphone
              <input
                value={form.telephone}
                onChange={(e) => setForm({ ...form, telephone: e.target.value })}
              />
            </label>
            <button type="submit">Ajouter</button>
          </form>
          {error && <p className="error">{error}</p>}
        </section>

        <section className="card">
          <h2>Patients {loading ? '…' : `(${patients.length})`}</h2>
          <table>
            <thead>
              <tr>
                <th>#</th>
                <th>Nom</th>
                <th>Prénom</th>
                <th>Contact</th>
                <th>Appareils</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {patients.map((p) => (
                <tr key={p.id}>
                  <td>{p.id}</td>
                  <td>{p.nom}</td>
                  <td>{p.prenom}</td>
                  <td>{p.email || p.telephone || '—'}</td>
                  <td>
                    <span className="badge">{p.appareils?.length ?? 0}</span>
                  </td>
                  <td>
                    <button className="danger" onClick={() => supprimer(p.id)}>
                      Supprimer
                    </button>
                  </td>
                </tr>
              ))}
              {patients.length === 0 && !loading && (
                <tr>
                  <td colSpan="6" style={{ color: 'var(--muted)' }}>
                    Aucun patient enregistré.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </section>
      </main>
    </>
  )
}
