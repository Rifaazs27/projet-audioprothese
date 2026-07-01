import { useEffect, useState } from 'react'
import { api } from './api'

const patientVide = { nom: '', prenom: '', email: '', telephone: '' }
const appareilVide = { marque: '', modele: '', numero_serie: '', oreille: 'gauche', date_pose: '' }
const rdvVide = { date_heure: '', motif: '' }

export default function App() {
  const [patients, setPatients] = useState([])
  const [rendezVous, setRendezVous] = useState([])
  const [form, setForm] = useState(patientVide)
  const [selectionId, setSelectionId] = useState(null)
  const [appareilForm, setAppareilForm] = useState(appareilVide)
  const [rdvForm, setRdvForm] = useState(rdvVide)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  async function charger() {
    setLoading(true)
    try {
      const [ps, rdvs] = await Promise.all([api.listPatients(), api.listRendezVous()])
      setPatients(ps)
      setRendezVous(rdvs)
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

  const selection = patients.find((p) => p.id === selectionId) || null
  const nomPatient = (id) => {
    const p = patients.find((x) => x.id === id)
    return p ? `${p.prenom} ${p.nom}` : `#${id}`
  }
  const formatDate = (v) => {
    const d = new Date(v)
    return isNaN(d) ? String(v ?? '—') : d.toLocaleString('fr-FR', { dateStyle: 'short', timeStyle: 'short' })
  }

  async function ajouterPatient(e) {
    e.preventDefault()
    try {
      const payload = { ...form, email: form.email || null, telephone: form.telephone || null }
      await api.createPatient(payload)
      setForm(patientVide)
      await charger()
    } catch (e) {
      setError(e.message)
    }
  }

  async function supprimer(id) {
    try {
      await api.deletePatient(id)
      if (id === selectionId) setSelectionId(null)
      await charger()
    } catch (e) {
      setError(e.message)
    }
  }

  async function enregistrerAppareil(e) {
    e.preventDefault()
    try {
      const payload = {
        ...appareilForm,
        numero_serie: appareilForm.numero_serie || null,
        date_pose: appareilForm.date_pose || null,
      }
      await api.addAppareil(selectionId, payload)
      setAppareilForm(appareilVide)
      await charger()
    } catch (e) {
      setError(e.message)
    }
  }

  async function prendreRendezVous(e) {
    e.preventDefault()
    try {
      await api.addRendezVous(selectionId, { ...rdvForm })
      setRdvForm(rdvVide)
      await charger()
    } catch (e) {
      setError(e.message)
    }
  }

  return (
    <>
      <header>
        <h1>Cabinet d'audioprothèse — Gestion des patients, appareils &amp; rendez-vous</h1>
        <p>MVP DevOps · API FastAPI · supervision Prometheus/Grafana</p>
      </header>
      <main>
        {error && <p className="error">{error}</p>}

        <section className="card">
          <h2>Nouveau patient</h2>
          <form onSubmit={ajouterPatient}>
            <label>
              Nom
              <input required value={form.nom} onChange={(e) => setForm({ ...form, nom: e.target.value })} />
            </label>
            <label>
              Prénom
              <input required value={form.prenom} onChange={(e) => setForm({ ...form, prenom: e.target.value })} />
            </label>
            <label>
              Email
              <input type="email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
            </label>
            <label>
              Téléphone
              <input value={form.telephone} onChange={(e) => setForm({ ...form, telephone: e.target.value })} />
            </label>
            <button type="submit">Ajouter</button>
          </form>
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
                <th>RDV</th>
                <th></th>
              </tr>
            </thead>
            <tbody>
              {patients.map((p) => (
                <tr key={p.id} className={p.id === selectionId ? 'ligne-active' : undefined}>
                  <td>{p.id}</td>
                  <td>{p.nom}</td>
                  <td>{p.prenom}</td>
                  <td>{p.email || p.telephone || '—'}</td>
                  <td><span className="badge">{p.appareils?.length ?? 0}</span></td>
                  <td><span className="badge">{p.rendez_vous?.length ?? 0}</span></td>
                  <td className="actions">
                    <button onClick={() => setSelectionId(p.id === selectionId ? null : p.id)}>
                      {p.id === selectionId ? 'Fermer' : 'Gérer'}
                    </button>
                    <button className="danger" onClick={() => supprimer(p.id)}>Supprimer</button>
                  </td>
                </tr>
              ))}
              {patients.length === 0 && !loading && (
                <tr>
                  <td colSpan="7" style={{ color: 'var(--muted)' }}>Aucun patient enregistré.</td>
                </tr>
              )}
            </tbody>
          </table>
        </section>

        {selection && (
          <section className="card">
            <h2>Dossier de {selection.prenom} {selection.nom}</h2>

            {/* -------- Rubrique : enregistrement d'appareil -------- */}
            <h3>Enregistrer un appareil auditif</h3>
            <form onSubmit={enregistrerAppareil}>
              <label>
                Marque
                <input required value={appareilForm.marque}
                  onChange={(e) => setAppareilForm({ ...appareilForm, marque: e.target.value })} />
              </label>
              <label>
                Modèle
                <input required value={appareilForm.modele}
                  onChange={(e) => setAppareilForm({ ...appareilForm, modele: e.target.value })} />
              </label>
              <label>
                N° de série
                <input value={appareilForm.numero_serie}
                  onChange={(e) => setAppareilForm({ ...appareilForm, numero_serie: e.target.value })} />
              </label>
              <label>
                Oreille
                <select value={appareilForm.oreille}
                  onChange={(e) => setAppareilForm({ ...appareilForm, oreille: e.target.value })}>
                  <option value="gauche">Gauche</option>
                  <option value="droite">Droite</option>
                  <option value="bilateral">Bilatéral</option>
                </select>
              </label>
              <label>
                Date de pose
                <input type="date" value={appareilForm.date_pose}
                  onChange={(e) => setAppareilForm({ ...appareilForm, date_pose: e.target.value })} />
              </label>
              <button type="submit">Enregistrer l'appareil</button>
            </form>

            <table>
              <thead>
                <tr><th>Marque</th><th>Modèle</th><th>N° série</th><th>Oreille</th><th>Date de pose</th></tr>
              </thead>
              <tbody>
                {selection.appareils?.map((a) => (
                  <tr key={a.id}>
                    <td>{a.marque}</td>
                    <td>{a.modele}</td>
                    <td>{a.numero_serie || '—'}</td>
                    <td>{a.oreille}</td>
                    <td>{a.date_pose || '—'}</td>
                  </tr>
                ))}
                {(selection.appareils?.length ?? 0) === 0 && (
                  <tr><td colSpan="5" style={{ color: 'var(--muted)' }}>Aucun appareil enregistré.</td></tr>
                )}
              </tbody>
            </table>

            {/* -------- Rubrique : prise de rendez-vous -------- */}
            <h3 style={{ marginTop: '1.5rem' }}>Prendre un rendez-vous</h3>
            <form onSubmit={prendreRendezVous}>
              <label>
                Date &amp; heure
                <input type="datetime-local" required value={rdvForm.date_heure}
                  onChange={(e) => setRdvForm({ ...rdvForm, date_heure: e.target.value })} />
              </label>
              <label>
                Motif
                <input required placeholder="Contrôle, réglage…" value={rdvForm.motif}
                  onChange={(e) => setRdvForm({ ...rdvForm, motif: e.target.value })} />
              </label>
              <button type="submit">Planifier le rendez-vous</button>
            </form>

            <table>
              <thead>
                <tr><th>Date &amp; heure</th><th>Motif</th><th>Statut</th></tr>
              </thead>
              <tbody>
                {selection.rendez_vous?.map((r) => (
                  <tr key={r.id}>
                    <td>{formatDate(r.date_heure)}</td>
                    <td>{r.motif}</td>
                    <td><span className="badge">{r.statut}</span></td>
                  </tr>
                ))}
                {(selection.rendez_vous?.length ?? 0) === 0 && (
                  <tr><td colSpan="3" style={{ color: 'var(--muted)' }}>Aucun rendez-vous planifié.</td></tr>
                )}
              </tbody>
            </table>
          </section>
        )}

        <section className="card">
          <h2>Rendez-vous à venir {loading ? '…' : `(${rendezVous.length})`}</h2>
          <table>
            <thead>
              <tr><th>Date &amp; heure</th><th>Patient</th><th>Motif</th><th>Statut</th></tr>
            </thead>
            <tbody>
              {rendezVous.map((r) => (
                <tr key={r.id}>
                  <td>{formatDate(r.date_heure)}</td>
                  <td>{nomPatient(r.patient_id)}</td>
                  <td>{r.motif}</td>
                  <td><span className="badge">{r.statut}</span></td>
                </tr>
              ))}
              {rendezVous.length === 0 && !loading && (
                <tr><td colSpan="4" style={{ color: 'var(--muted)' }}>Aucun rendez-vous.</td></tr>
              )}
            </tbody>
          </table>
        </section>
      </main>
    </>
  )
}
