import { useState, useEffect } from 'react'
import { Typography, Card, Button, Spin } from 'antd'
import { ReloadOutlined } from '@ant-design/icons'
import DiagnosticReport from '../../components/common/DiagnosticReport'

const { Title, Paragraph } = Typography

const mockReport = {
  weak_points: [
    {
      knowledge_point_id: 'grammar_prt_passe_compose',
      name: '复合过去时',
      level: 'A1',
      category: 'verb_conjugation',
      mastery: 0.25,
      confidence: 0.75,
      root_cause: true,
    },
    {
      knowledge_point_id: 'grammar_auxiliaire',
      name: '助动词 avoir/être',
      level: 'A1',
      category: 'grammar',
      mastery: 0.35,
      confidence: 0.65,
      root_cause: true,
    },
  ],
  overall_mastery: 0.45,
  recommendations: [
    '优先学习根本原因知识点: 复合过去时',
    '加强 verb_conjugation 类知识的学习',
  ],
  category_mastery: {
    grammar: 0.55,
    vocabulary: 0.65,
    verb_conjugation: 0.35,
  },
}

const DiagnosticsPage: React.FC = () => {
  const [report] = useState(mockReport)
  const [loading, setLoading] = useState(false)

  const fetchReport = async () => {
    setLoading(true)
    setTimeout(() => {
      setLoading(false)
    }, 500)
  }

  useEffect(() => {
    fetchReport()
  }, [])

  return (
    <div>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 24 }}>
        <div>
          <Title level={2}>诊断报告</Title>
          <Paragraph>查看你的学习诊断和薄弱点分析</Paragraph>
        </div>
        <Button onClick={fetchReport} loading={loading}>
          <ReloadOutlined /> 刷新
        </Button>
      </div>

      {loading ? (
        <Card>
          <div style={{ textAlign: 'center', padding: '100px 0' }}>
            <Spin size="large" tip="加载诊断报告..." />
          </div>
        </Card>
      ) : (
        <DiagnosticReport report={report} />
      )}
    </div>
  )
}

export default DiagnosticsPage
