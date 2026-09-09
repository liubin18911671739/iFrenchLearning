import { Card, Row, Col, Statistic, List, Tag, Typography, Progress, Empty, Button, Space } from 'antd'
import {
  WarningOutlined,
  CheckCircleOutlined,
  BulbOutlined,
  ArrowRightOutlined,
} from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'

const { Paragraph, Text } = Typography

interface WeakPoint {
  knowledge_point_id: string
  name: string
  level: string
  category: string
  mastery: number
  confidence: number
  root_cause: boolean
}

interface DiagnosticReportProps {
  report: {
    weak_points: WeakPoint[]
    overall_mastery: number
    recommendations: string[]
    category_mastery: Record<string, number>
  } | null
}

const categoryLabels: Record<string, string> = {
  grammar: '语法',
  vocabulary: '词汇',
  verb_conjugation: '动词变位',
  accord: '性数配合',
}

const categoryColors: Record<string, string> = {
  grammar: '#1890ff',
  vocabulary: '#52c41a',
  verb_conjugation: '#faad14',
  accord: '#f5222d',
}

const DiagnosticReport: React.FC<DiagnosticReportProps> = ({ report }) => {
  const navigate = useNavigate()

  if (!report) {
    return (
      <Card>
        <Empty description="暂无诊断数据" />
      </Card>
    )
  }

  const rootCauses = report.weak_points.filter((wp) => wp.root_cause)
  const weakPoints = report.weak_points.filter((wp) => !wp.root_cause)

  return (
    <div>
      <Row gutter={[16, 16]} style={{ marginBottom: 24 }}>
        <Col xs={24} sm={8}>
          <Card>
            <Statistic
              title="总体掌握度"
              value={Math.round(report.overall_mastery * 100)}
              suffix="%"
              valueStyle={{
                color: report.overall_mastery >= 0.7 ? '#52c41a' : '#faad14',
              }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card>
            <Statistic
              title="薄弱知识点"
              value={report.weak_points.length}
              prefix={<WarningOutlined style={{ color: '#f5222d' }} />}
              valueStyle={{ color: '#f5222d' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card>
            <Statistic
              title="根本原因"
              value={rootCauses.length}
              prefix={<BulbOutlined style={{ color: '#faad14' }} />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
      </Row>

      <Card title="各类别掌握度" style={{ marginBottom: 24 }}>
        <Row gutter={[16, 16]}>
          {Object.entries(report.category_mastery).map(([category, mastery]) => (
            <Col xs={12} sm={6} key={category}>
              <div style={{ textAlign: 'center' }}>
                <Progress
                  type="circle"
                  percent={Math.round(mastery * 100)}
                  strokeColor={
                    mastery >= 0.7 ? '#52c41a' : mastery >= 0.5 ? '#faad14' : '#f5222d'
                  }
                  size={100}
                />
                <div style={{ marginTop: 8 }}>
                  <Text strong>{categoryLabels[category] || category}</Text>
                </div>
              </div>
            </Col>
          ))}
        </Row>
      </Card>

      {rootCauses.length > 0 && (
        <Card
          title={
            <Space>
              <BulbOutlined style={{ color: '#faad14' }} />
              <span>根本原因分析</span>
            </Space>
          }
          style={{ marginBottom: 24 }}
          type="inner"
        >
          <Paragraph type="secondary">
            以下知识点是导致其他知识点薄弱的根本原因，建议优先学习：
          </Paragraph>
          <List
            dataSource={rootCauses}
            renderItem={(item) => (
              <List.Item
                actions={[
                  <Button
                    type="link"
                    onClick={() => navigate('/learning')}
                  >
                    去学习 <ArrowRightOutlined />
                  </Button>,
                ]}
              >
                <List.Item.Meta
                  title={
                    <Space>
                      <Text strong>{item.name}</Text>
                      <Tag color={categoryColors[item.category]}>
                        {categoryLabels[item.category]}
                      </Tag>
                      <Tag>{item.level}</Tag>
                    </Space>
                  }
                  description={
                    <Space>
                      <Text type="secondary">
                        掌握度: {Math.round(item.mastery * 100)}%
                      </Text>
                      <Text type="secondary">
                        置信度: {Math.round(item.confidence * 100)}%
                      </Text>
                    </Space>
                  }
                />
              </List.Item>
            )}
          />
        </Card>
      )}

      {weakPoints.length > 0 && (
        <Card
          title={
            <Space>
              <WarningOutlined style={{ color: '#f5222d' }} />
              <span>其他薄弱知识点</span>
            </Space>
          }
          style={{ marginBottom: 24 }}
        >
          <List
            dataSource={weakPoints.slice(0, 10)}
            renderItem={(item) => (
              <List.Item>
                <List.Item.Meta
                  title={
                    <Space>
                      <Text>{item.name}</Text>
                      <Tag color={categoryColors[item.category]}>
                        {categoryLabels[item.category]}
                      </Tag>
                      <Tag>{item.level}</Tag>
                    </Space>
                  }
                  description={
                    <Progress
                      percent={Math.round(item.mastery * 100)}
                      size="small"
                      strokeColor={
                        item.mastery >= 0.5 ? '#faad14' : '#f5222d'
                      }
                      style={{ maxWidth: 300 }}
                    />
                  }
                />
              </List.Item>
            )}
          />
        </Card>
      )}

      <Card
        title={
          <Space>
            <CheckCircleOutlined style={{ color: '#52c41a' }} />
            <span>学习建议</span>
          </Space>
        }
      >
        <List
          dataSource={report.recommendations}
          renderItem={(item) => (
            <List.Item>
              <List.Item.Meta
                avatar={<BulbOutlined style={{ color: '#faad14', fontSize: 16 }} />}
                description={item}
              />
            </List.Item>
          )}
        />
      </Card>
    </div>
  )
}

export default DiagnosticReport
