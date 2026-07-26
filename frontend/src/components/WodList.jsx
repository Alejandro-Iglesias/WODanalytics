import { useNavigate } from 'react-router-dom'

function WodList({ wods }) {
  const navigate = useNavigate()

  if (wods.length === 0) {
    return (
      <div className="bg-gray-800 rounded-xl p-6 border border-gray-700 text-center">
        <p className="text-gray-400">No hay entrenamientos registrados todavía.</p>
      </div>
    )
  }

  return (
    <div className="bg-gray-800 rounded-xl border border-gray-700">
      <div className="p-4 border-b border-gray-700">
        <h2 className="text-lg font-semibold text-white">Historial de entrenamientos</h2>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-700">
              <th className="text-left text-gray-400 text-sm font-medium px-4 py-3">Ejercicio</th>
              <th className="text-left text-gray-400 text-sm font-medium px-4 py-3">Tipo</th>
              <th className="text-left text-gray-400 text-sm font-medium px-4 py-3">Tiempo (min)</th>
              <th className="text-left text-gray-400 text-sm font-medium px-4 py-3">Repeticiones</th>
              <th className="text-left text-gray-400 text-sm font-medium px-4 py-3">Fecha</th>
            </tr>
          </thead>
          <tbody>
            {wods.map((wod) => (
              <tr
                key={wod.id}
                onClick={() => navigate(`/wods/${wod.id}`)}
                className="border-b border-gray-700 hover:bg-gray-700 transition-colors cursor-pointer"
              >
                <td className="px-4 py-3 text-white font-medium">{wod.nombre_ejercicio}</td>
                <td className="px-4 py-3">
                  <span className="bg-emerald-900 text-emerald-300 text-xs px-2 py-1 rounded-full">
                    {wod.tipo}
                  </span>
                </td>
                <td className="px-4 py-3 text-gray-300">{wod.resultado_tiempo ?? '—'}</td>
                <td className="px-4 py-3 text-gray-300">{wod.resultado_repeticiones ?? '—'}</td>
                <td className="px-4 py-3 text-gray-400 text-sm">{wod.fecha_entrenamiento}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default WodList