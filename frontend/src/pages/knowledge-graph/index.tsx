import { useState, useEffect } from 'react'
import { Typography, Card, Tabs } from 'antd'
import KnowledgeGraph from '../../components/common/KnowledgeGraph'

const { Title, Paragraph } = Typography

interface GraphNode {
  id: string
  name: string
  level: string
  category: string
  mastery?: number
}

interface GraphEdge {
  source: string
  target: string
  type: string
}

const KnowledgeGraphPage: React.FC = () => {
  const [loading, setLoading] = useState(false)
  const [nodes] = useState<GraphNode[]>([])
  const [edges] = useState<GraphEdge[]>([])
  const [selectedLevel, setSelectedLevel] = useState<string | undefined>(undefined)

  const fetchGraphData = async (_level?: string) => {
    setLoading(true)
    setTimeout(() => {
      setLoading(false)
    }, 500)
  }

  useEffect(() => {
    fetchGraphData(selectedLevel)
  }, [selectedLevel])

  const tabItems = [
    { key: 'all', label: '全部' },
    { key: 'A1', label: 'A1' },
    { key: 'A2', label: 'A2' },
    { key: 'B1', label: 'B1' },
    { key: 'B2', label: 'B2' },
  ]

  return (
    <div>
      <Title level={2}>知识图谱</Title>
      <Paragraph>
        探索法语知识体系，了解知识点之间的依赖关系
      </Paragraph>

      <Card style={{ marginTop: 24 }}>
        <Tabs
          items={tabItems}
          onChange={(key) => setSelectedLevel(key === 'all' ? undefined : key)}
        />
      </Card>

      <div style={{ marginTop: 24 }}>
        <KnowledgeGraph
          nodes={nodes}
          edges={edges}
          loading={loading}
          width={1100}
          height={650}
        />
      </div>
    </div>
  )
}

export default KnowledgeGraphPage
