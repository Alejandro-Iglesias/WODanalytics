import { useState, useEffect } from 'react'
import WodList from './WodList'
import WodForm from './WodForm'
import PredictForm from './PredictForm'

const API = 'http://localhost:8000/api/v1'

function Dashboard({ token, onLogout }) {
  const [wodsData, setWodsData] = useState(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState('dashboard')

  const headers = {
    'Content-Type': 'application/json',
    Authorization: `Bearer ${token}`,
  }

  const fetchWods = async () => {
    try {
      const res = await fetch(`${API}/wods/`, { headers })
      const data = await res.json()
      setWodsData(data)
    } catch (err) {
      console.error('Error cargando WODs:', err)
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchWods()
  }, [])

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-900 flex items-center justify-center">
        <p className="text-emerald-400 text-xl">Cargando dashboard...</p>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-900 text-white">

      {/* Navbar */}
      <nav className="bg-gray-800 border-b border-gray-700 px-6 py-4">
        <div className="flex justify-between items-center">
          <h1 className="text-xl font-bold text-emerald-400">WODAnalytics AI</h1>
          <div className="flex gap-4">
            <button
              onClick={() => setActiveTab('dashboard')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'dashboard' ? 'bg-emerald-500 text-white' : 'text-gray-400 hover:text-white'}`}
            >
              Dashboard
            </button>
            <button
              onClick={() => setActiveTab('register')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'register' ? 'bg-emerald-500 text-white' : 'text-gray-400 hover:text-white'}`}
            >
              Registrar WOD
            </button>
            <button
              onClick={() => setActiveTab('predict')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${activeTab === 'predict' ? 'bg-emerald-500 text-white' : 'text-gray-400 hover:text-white'}`}
            >
              Predicción ML
            </button>
            <button
              onClick={onLogout}
              className="bg-red-600 hover:bg-red-700 text-white px-4 py-2 rounded-lg text-sm transition-colors"
            >
              Cerrar sesión
            </button>
          </div>
        </div>
      </nav>

      {/* Contenido */}
      <main className="p-6">

        {/* Métricas */}
        {activeTab === 'dashboard' && (
          <div>
            {/* Cards de métricas */}
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
              <div className="bg-gray-800 rounded-xl p-5 border border-gray-700">
                <p className="text-gray-400 text-sm">Racha actual</p>
                <p className="text-4xl font-bold text-emerald-400 mt-1">
                  {wodsData?.racha_dias ?? 0}
                  <span className="text-lg text-gray-400 ml-1">días</span>
                </p>
              </div>
              <div className="bg-gray-800 rounded-xl p-5 border border-gray-700">
                <p className="text-gray-400 text-sm">Media semanal</p>
                <p className="text-4xl font-bold text-blue-400 mt-1">
                  {wodsData?.media_semanal ?? 0}
                  <span className="text-lg text-gray-400 ml-1">WODs/día</span>
                </p>
              </div>
              <div className={`rounded-xl p-5 border ${wodsData?.alerta_fatiga ? 'bg-red-900 border-red-700' : 'bg-gray-800 border-gray-700'}`}>
                <p className="text-gray-400 text-sm">Estado</p>
                {wodsData?.alerta_fatiga ? (
                  <p className="text-red-400 font-semibold mt-1 text-sm">{wodsData.alerta_fatiga}</p>
                ) : (
                  <p className="text-emerald-400 font-bold text-xl mt-1">Sin alertas</p>
                )}
              </div>
            </div>

            {/* Lista de WODs */}
            <WodList wods={wodsData?.wods ?? []} />
          </div>
        )}

        {activeTab === 'register' && (
          <WodForm token={token} headers={headers} onSuccess={() => { fetchWods(); setActiveTab('dashboard') }} />
        )}

        {activeTab === 'predict' && (
          <PredictForm token={token} headers={headers} />
        )}

      </main>
    </div>
  )
}

export default Dashboard