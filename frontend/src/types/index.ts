export interface Learner {
  id: string
  name: string
  level: 'A1' | 'A2' | 'B1' | 'B2'
  createdAt?: string
}

export interface KnowledgeState {
  knowledgePointId: string
  mastery: number
  lastPracticed?: string
}

export interface KnowledgePoint {
  id: string
  name: string
  level: string
  category: 'vocabulary' | 'grammar' | 'verb_conjugation' | 'accord'
  description?: string
  prerequisites: string[]
}

export interface KnowledgeGraph {
  nodes: KnowledgePoint[]
  edges: Array<{
    source: string
    target: string
    type: string
  }>
}

export interface Exercise {
  id: string
  type: 'vocabulary' | 'grammar' | 'translation' | 'reading' | 'listening'
  difficulty: number
  content: string
  options?: string[]
  correctAnswer: string
  knowledgePoints: string[]
  cognitiveLevel: string
}

export interface ExerciseResult {
  exerciseId: string
  correct: boolean
  score: number
  feedback: string
  masteryChanges: Record<string, number>
}

export interface DiagnosticReport {
  learnerId: string
  weakPoints: Array<{
    knowledgePointId: string
    name: string
    mastery: number
    rootCause?: string
  }>
  errorTrends: Array<{
    date: string
    vocabulary: number
    grammar: number
    conjugation: number
  }>
  recommendations: string[]
}

export interface LearningPath {
  current: string
  target: string
  path: string[]
  recommendations: Array<{
    knowledgePointId: string
    name: string
    reason: string
  }>
}
