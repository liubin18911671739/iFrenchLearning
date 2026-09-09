import { create } from 'zustand'

interface LearnerState {
  id: string | null
  name: string
  level: string
  knowledgeState: Record<string, number>
  overallMastery: number
  isLoading: boolean
  setLearner: (id: string, name: string, level: string) => void
  updateKnowledgeState: (kpId: string, mastery: number) => void
  setLoading: (loading: boolean) => void
}

export const useLearnerStore = create<LearnerState>((set) => ({
  id: null,
  name: '',
  level: 'A1',
  knowledgeState: {},
  overallMastery: 0,
  isLoading: false,

  setLearner: (id, name, level) =>
    set({ id, name, level }),

  updateKnowledgeState: (kpId, mastery) =>
    set((state) => {
      const newKnowledgeState = { ...state.knowledgeState, [kpId]: mastery }
      const values = Object.values(newKnowledgeState)
      const overallMastery = values.length > 0
        ? values.reduce((a, b) => a + b, 0) / values.length
        : 0
      return {
        knowledgeState: newKnowledgeState,
        overallMastery,
      }
    }),

  setLoading: (isLoading) => set({ isLoading }),
}))

interface AppState {
  sidebarCollapsed: boolean
  toggleSidebar: () => void
}

export const useAppStore = create<AppState>((set) => ({
  sidebarCollapsed: false,
  toggleSidebar: () => set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
}))
