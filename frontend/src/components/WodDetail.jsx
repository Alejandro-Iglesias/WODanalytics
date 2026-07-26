import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'

const API = 'http://localhost:8000/api/v1'

function WodDetail({ token }) {
  const { id } = useParams()
  const navigate = useNavigate()

  const [wod, setWod] = useState(null)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const [form, setForm] = useState({})
  const [error, setError] = useState(null)
  const [saving, setSaving] = useState(false)

  const headers = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  }

  useEffect(() => {
    fetchWod()
  }, [id])

  const fetchWod = async () => {
    try {
      const res = await fetch(`${API}/wods/${id}/`, { headers })
      const data = await res.json()
      setWod(data)
      setForm(data)
    } catch {
      setError('Error cargando el WOD')
    } finally {
      setLoading(false)
    }
  }

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSave = async () => {
    setSaving(true)
    setError(null)

    try {
      const res = await fetch(`${API}/wods/${id}/`, {
        method: 'PUT',
        headers,
        body: JSON.stringify(form),
      })

      if (!res.ok) {
        const data = await res.json()
        setError(JSON.stringify(data))
        return
      }

      const data = await res.json()
      setWod(data)
      setEditing(false)

    } catch {
      setError('Error guardando los cambios')
    } finally {
      setSaving(false)
    }
  }

  const handleDelete = async () => {
    if (!confirm('¿Seguro que quieres eliminar este WOD?')) return

    try {
      await fetch(`${API}/wods/${id}/`, {
        method: 'DELETE',
        headers,
      })
      navigate('/')
    } catch {
      setError('Error eliminando el WOD')
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <p className="text-emerald-400 text-xl">Cargando...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">

      {/* Navbar */}
      <nav className="bg-gray-800 border-b border-gray-700 px-6 py-4">
        <div className="flex justify-between items-center">
          <button
            onClick={() => navigate('/')}
            className="text-emerald-400 hover:text-emerald-300 font-medium transition-colors"
          >
            Volver al dashboard
          </button>
          <div className="flex gap-3">
            {!editing ? (
              <>
                <button
                  onClick={() => setEditing(true)}
                  className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg text-sm transition-colors"
                >
                  Editar
                </button>
                <button
                  onClick={handleDelete}
                  className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm transition-colors"
                >
                  Eliminar
                </button>
              </>
            ) : (
              <>
                <button
                  onClick={() => setEditing(false)}
                  className="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded-lg text-sm transition-colors"
                >
                  Cancelar
                </button>
                <button
                  onClick={handleSave}
                  disabled={saving}
                  className="bg-emerald-500 hover:bg-emerald-600 disabled:bg-gray-600 text-white px-4 py-2 rounded-lg text-sm transition-colors"
                >
                  {saving ? 'Guardando...' : 'Guardar cambios'}
                </button>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Contenido */}
      <main className="max-w-2xl mx-auto p-6">
        <h1 className="text-2xl font-bold text-white mb-6">
          {editing ? 'Editando WOD' : 'Detalle del WOD'}
        </h1>

        {error && (
          <p className="text-red-400 text-sm mb-4">{error}</p>
        )}

        <div className="bg-gray-800 rounded-xl border border-gray-700 p-6 space-y-4">

          <div>
            <label className="block text-sm text-gray-400 mb-1">Ejercicio</label>
            {editing ? (
              <input
                type="text"
                name="nombre_ejercicio"
                value={form.nombre_ejercicio}
                onChange={handleChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-400"
              />
            ) : (
              <p className="text-white font-semibold text-lg">{wod.nombre_ejercicio}</p>
            )}
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-1">Tipo</label>
            {editing ? (
              <select
                name="tipo"
                value={form.tipo}
                onChange={handleChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-400"
              >
                <option value="for_time">For Time</option>
                <option value="amrap">AMRAP</option>
                <option value="emom">EMOM</option>
                <option value="tabata">Tabata</option>
              </select>
            ) : (
              <span className="bg-emerald-900 text-emerald-300 text-sm px-3 py-1 rounded-full">
                {wod.tipo}
              </span>
            )}
          </div>

          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Tiempo (min)</label>
              {editing ? (
                <input
                  type="number"
                  name="resultado_tiempo"
                  value={form.resultado_tiempo ?? ''}
                  onChange={handleChange}
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-400"
                  step="0.1"
                />
              ) : (
                <p className="text-white">{wod.resultado_tiempo ?? '—'}</p>
              )}
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Repeticiones</label>
              {editing ? (
                <input
                  type="number"
                  name="resultado_repeticiones"
                  value={form.resultado_repeticiones ?? ''}
                  onChange={handleChange}
                  className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-400"
                />
              ) : (
                <p className="text-white">{wod.resultado_repeticiones ?? '—'}</p>
              )}
            </div>
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-1">Peso (kg)</label>
            {editing ? (
              <input
                type="number"
                name="peso"
                value={form.peso ?? ''}
                onChange={handleChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-400"
                step="0.5"
              />
            ) : (
              <p className="text-white">{wod.peso ?? '—'}</p>
            )}
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-1">Notas</label>
            {editing ? (
              <textarea
                name="notas"
                value={form.notas ?? ''}
                onChange={handleChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-400"
                rows={4}
              />
            ) : (
              <p className="text-gray-300">{wod.notas ?? 'Sin notas'}</p>
            )}
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-1">Fecha</label>
            <p className="text-gray-300">{wod.fecha_entrenamiento}</p>
          </div>

        </div>
      </main>
    </div>
  )
}

export default WodDetail