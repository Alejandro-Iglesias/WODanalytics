import { useState } from 'react'
import { Routes, Route, Navigate } from 'react-router-dom'
import LoginForm from './components/LoginForm'
import RegisterForm from './components/RegisterForm'
import Dashboard from './components/Dashboard'
import WodDetail from './components/WodDetail'

function App() {
  const [token, setToken] = useState(localStorage.getItem('access_token'))
  const [showRegister, setShowRegister] = useState(false)

  const handleLogin = (accessToken) => {
    setToken(accessToken)
    setShowRegister(false)
  }

  const handleLogout = () => {
    localStorage.removeItem('access_token')
    setToken(null)
  }

  if (!token) {
    if (showRegister) {
      return <RegisterForm onLogin={handleLogin} onBack={() => setShowRegister(false)} />
    }
    return <LoginForm onLogin={handleLogin} onShowRegister={() => setShowRegister(true)} />
  }

  return (
    <Routes>
      <Route path="/" element={<Dashboard token={token} onLogout={handleLogout} />} />
      <Route path="/wods/:id" element={<WodDetail token={token} onLogout={handleLogout} />} />
      <Route path="*" element={<Navigate to="/" />} />
    </Routes>
  )
}

export default App