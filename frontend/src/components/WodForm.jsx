import { useState } from 'react'

const API = 'http://localhost:8000/api/v1'

function WodForm({ headers, onSuccess }) {
  const [form, setForm] = useState({
    nombre_ejercicio: '',
    tipo: 'for_time',
    resultado_tiempo: '',
    resultado_repeticiones: '',
    peso: '',
    notas: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    // Limpiamos los campos vacíos para no mandar null innecesario
    const body = { ...form }
    if (!body.resultado_tiempo) delete body.resultado_tiempo
    if (!body.resultado_repeticiones) delete body.resultado_repeticiones
    if (!body.peso) delete body.peso
    if (!body.notas) delete body.notas

    try {
      const res = await fetch(`${API}/wods/`, {
        method: 'POST',
        headers,
        body: JSON.stringify(body),
      })

      const data = await res.json()

      if (!res.ok) {
        setError(JSON.stringify(data))
        return
      }

      onSuccess()

    } catch {
      setError('Error de conexión con el servidor')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-lg mx-auto bg-gray-800 rounded-xl p-6 border border-gray-700">
      <h2 className="text-lg font-semibold text-white mb-6">Registrar nuevo WOD</h2>

      <form onSubmit={handleSubmit} className="space-y-4">

        <div>
          <label className="block text-sm text-gray-400 mb-1">Nombre del ejercicio</label>
          <input
            type="text"
            name="nombre_ejercicio"
            value={form.nombre_ejercicio}
            onChange={handleChange}
            className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-400"
            placeholder="Fran, Murph, Back Squat..."
            required
          />
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-1">Tipo de WOD</label>
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
        </div>

        <div className="grid grid-cols-2 gap-4">
          <div>
            <label className="block text-sm text-gray-400 mb-1">Tiempo (minutos)</label>
            <input
              type="number"
              name="resultado_tiempo"
              value={form.resultado_tiempo}
              onChange={handleChange}
              className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-400"
              placeholder="12.5"
              step="0.1"
            />
          </div>
          <div>
            <label className="block text-sm text-gray-400 mb-1">Repeticiones</label>
            <input
              type="number"
              name="resultado_repeticiones"
              value={form.resultado_repeticiones}
              onChange={handleChange}
              className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-400"
              placeholder="150"
            />
          </div>
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-1">Peso (kg)</label>
          <input
            type="number"
            name="peso"
            value={form.peso}
            onChange={handleChange}
            className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-400"
            placeholder="80"
            step="0.5"
          />
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-1">Notas</label>
          <textarea
            name="notas"
            value={form.notas}
            onChange={handleChange}
            className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-400"
            placeholder="Sensaciones, PR, observaciones..."
            rows={3}
          />
        </div>

        {error && (
          <p className="text-red-400 text-sm">{error}</p>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-emerald-500 hover:bg-emerald-600 disabled:bg-gray-600 text-white font-semibold py-3 rounded-lg transition-colors"
        >
          {loading ? 'Registrando...' : 'Registrar WOD'}
        </button>

      </form>
    </div>
  )
}

export default WodForm