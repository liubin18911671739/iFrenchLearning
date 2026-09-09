import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 可以在这里添加token
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    return response.data
  },
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

// 健康检查API
export const healthApi = {
  check: () => api.get('/health'),
  checkNeo4j: () => api.get('/health/neo4j'),
  checkPostgres: () => api.get('/health/postgres'),
}

// 学习者API
export const learnerApi = {
  getAll: (params?: { skip?: number; limit?: number }) =>
    api.get('/learners', { params }),
  create: (data: { name: string; level?: string }) =>
    api.post('/learners', data),
  getState: (id: string) => api.get(`/learners/${id}/state`),
}

// 知识图谱API
export const knowledgeGraphApi = {
  getGraph: () => api.get('/knowledge-graph'),
  getPrerequisites: (nodeId: string) =>
    api.get(`/knowledge-graph/${nodeId}/prerequisites`),
  findPath: (current: string, target: string) =>
    api.get(`/knowledge-graph/path/${current}/${target}`),
}

// 练习API
export const exerciseApi = {
  getAll: () => api.get('/exercises'),
  submit: (data: { exerciseId: string; answer: string }) =>
    api.post('/exercises/submit', data),
  getRecommendations: (learnerId: string, n?: number) =>
    api.get('/exercises/recommend', { params: { learner_id: learnerId, n } }),
}

export default api
