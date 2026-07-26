import { useState } from 'react'

const API = 'http://localhost:8000/api/v1'

function RegisterForm({ onLogin, onBack }) {
  const [form, setForm] = useState({
    email: '',
    username: '',
    password: '',
    fecha_nacimiento: '',
    peso_kg: '',
    altura_cm: '',
  })
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value })
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    // Limpiamos campos opcionales vacíos
    const body = { ...form }
    if (!body.fecha_nacimiento) delete body.fecha_nacimiento
    if (!body.peso_kg) delete body.peso_kg
    if (!body.altura_cm) delete body.altura_cm

    try {
      // Registro
      const res = await fetch(`${API}/auth/register/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })

      const data = await res.json()

      if (!res.ok) {
        const firstError = Object.values(data)[0]
        setError(Array.isArray(firstError) ? firstError[0] : firstError)
        return
      }

      // Login automático tras registro exitoso
      const loginRes = await fetch(`${API}/auth/token/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email: form.email, password: form.password }),
      })

      const loginData = await loginRes.json()
      localStorage.setItem('access_token', loginData.access)
      onLogin(loginData.access)

    } catch {
      setError('Error de conexión con el servidor')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-900 flex items-center justify-center px-4">
      <div className="bg-gray-800 rounded-2xl p-8 w-full max-w-md border border-gray-700">

        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-emerald-400">WODAnalytics AI</h1>
          <p className="text-gray-400 mt-2">Crea tu cuenta de atleta</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">

          <div>
            <label className="block text-sm text-gray-400 mb-1">Email</label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-400"
              placeholder="atleta@gmail.com"
              required
            />
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-1">Nombre de usuario</label>
            <input
              type="text"
              name="username"
              value={form.username}
              onChange={handleChange}
              className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-400"
              placeholder="alejandro"
              required
            />
          </div>

          <div>
            <label className="block text-sm text-gray-400 mb-1">Contraseña</label>
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              className="w-full bg-gray-700 border border-gray-600 rounded-lg px-4 py-3 text-white focus:outline-none focus:border-emerald-400"
              placeholder="Min. 8 caracteres, mayúscula, número y especial"
              required
            />
          </div>

          <div className="grid grid-cols-3 gap-3">
            <div>
              <label className="block text-sm text-gray-400 mb-1">Nacimiento</label>
              <input
                type="date"
                name="fecha_nacimiento"
                value={form.fecha_nacimiento}
                onChange={handleChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-3 text-white focus:outline-none focus:border-emerald-400"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Peso (kg)</label>
              <input
                type="number"
                name="peso_kg"
                value={form.peso_kg}
                onChange={handleChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-3 text-white focus:outline-none focus:border-emerald-400"
                placeholder="75"
                step="0.1"
              />
            </div>
            <div>
              <label className="block text-sm text-gray-400 mb-1">Altura (cm)</label>
              <input
                type="number"
                name="altura_cm"
                value={form.altura_cm}
                onChange={handleChange}
                className="w-full bg-gray-700 border border-gray-600 rounded-lg px-3 py-3 text-white focus:outline-none focus:border-emerald-400"
                placeholder="175"
              />
            </div>
          </div>

          {error && (
            <p className="text-red-400 text-sm text-center">{error}</p>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-emerald-500 hover:bg-emerald-600 disabled:bg-gray-600 text-white font-semibold py-3 rounded-lg transition-colors"
          >
            {loading ? 'Creando cuenta...' : 'Crear cuenta'}
          </button>

          <button
            type="button"
            onClick={onBack}
            className="w-full text-gray-400 hover:text-white text-sm py-2 transition-colors"
          >
            Ya tengo cuenta. Iniciar sesión
          </button>

        </form>
      </div>
    </div>
  )
}

export default RegisterForm