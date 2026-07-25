import { useState } from 'react'

const API = 'http://localhost:8000/api/v1'

function PredictForm({ headers }) {
  const [form, setForm] = useState({
    fatiga_muscular: 5,
    nivel_estres: 5,
    horas_sueno: 7,
    tipo_wod: 'for_time',
  })
  const [resultado, setResultado] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)
    setResultado(null)

    try {
      const res = await fetch(`${API}/predict/`, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          fatiga_muscular: parseInt(form.fatiga_muscular),
          nivel_estres: parseInt(form.nivel_estres),
          horas_sueno: parseFloat(form.horas_sueno),
          tipo_wod: form.tipo_wod,
        }),
      })

      const data = await res.json()

      if (!res.ok) {
        setError(JSON.stringify(data))
        return
      }

      setResultado(data)

    } catch {
      setError('Error de conexión con el servidor')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-lg mx-auto bg-gray-800 rounded-xl p-6 border border-gray-700">
      <h2 className="text-lg font-semibold text-white mb-2">Predicción de rendimiento</h2>
      <p className="text-gray-400 text-sm mb-6">
        Introduce tu estado físico de hoy y el modelo de ML estimará tu rendimiento.
      </p>

      <form onSubmit={handleSubmit} className="space-y-4">

        <div>
          <label className="block text-sm text-gray-400 mb-1">
            Fatiga muscular: <span className="text-white font-medium">{form.fatiga_muscular}/10</span>
          </label>
          <input
            type="range"
            name="fatiga_muscular"
            min="1"
            max="10"
            value={form.fatiga_muscular}
            onChange={handleChange}
            className="w-full accent-emerald-400"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>Sin fatiga</span>
            <span>Agotado</span>
          </div>
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-1">
            Nivel de estrés: <span className="text-white font-medium">{form.nivel_estres}/10</span>
          </label>
          <input
            type="range"
            name="nivel_estres"
            min="1"
            max="10"
            value={form.nivel_estres}
            onChange={handleChange}
            className="w-full accent-emerald-400"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>Sin estres</span>
            <span>Muy estresado</span>
          </div>
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-1">
            Horas de sueño: <span className="text-white font-medium">{form.horas_sueno}h</span>
          </label>
          <input
            type="range"
            name="horas_sueno"
            min="4"
            max="10"
            step="0.5"
            value={form.horas_sueno}
            onChange={handleChange}
            className="w-full accent-emerald-400"
          />
          <div className="flex justify-between text-xs text-gray-500 mt-1">
            <span>4h</span>
            <span>10h</span>
          </div>
        </div>

        <div>
          <label className="block text-sm text-gray-400 mb-1">Tipo de WOD</label>
          <select
            name="tipo_wod"
            value={form.tipo_wod}
            onChange={handleChange}
            className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-400"
          >
            <option value="for_time">For Time</option>
            <option value="amrap">AMRAP</option>
            <option value="emom">EMOM</option>
            <option value="tabata">Tabata</option>
          </select>
        </div>

        {error && (
          <p className="text-red-400 text-sm">{error}</p>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full bg-emerald-500 hover:bg-emerald-600 disabled:bg-gray-600 text-white font-semibold py-3 rounded-lg transition-colors"
        >
          {loading ? 'Calculando...' : 'Predecir rendimiento'}
        </button>

      </form>

      {resultado && (
        <div className="mt-6 bg-gray-700 rounded-xl p-5 border border-emerald-700">
          <p className="text-gray-400 text-sm mb-1">Tiempo estimado</p>
          <p className="text-4xl font-bold text-emerald-400">
            {resultado.tiempo_estimado_minutos}
            <span className="text-lg text-gray-400 ml-1">minutos</span>
          </p>
          <p className="text-gray-400 text-sm mt-2">{resultado.mensaje}</p>
        </div>
      )}

    </div>
  )
}

export default PredictForm