import { Routes, Route } from 'react-router-dom'
import MainLayout from './components/layout/MainLayout'
import HomePage from './pages/home'
import LearningPage from './pages/learning'
import ExercisesPage from './pages/exercises'
import DiagnosticsPage from './pages/diagnostics'
import KnowledgeGraphPage from './pages/knowledge-graph'
import ProfilePage from './pages/profile'

function App() {
  return (
    <Routes>
      <Route path="/" element={<MainLayout />}>
        <Route index element={<HomePage />} />
        <Route path="learning" element={<LearningPage />} />
        <Route path="exercises" element={<ExercisesPage />} />
        <Route path="diagnostics" element={<DiagnosticsPage />} />
        <Route path="knowledge-graph" element={<KnowledgeGraphPage />} />
        <Route path="profile" element={<ProfilePage />} />
      </Route>
    </Routes>
  )
}

export default App
