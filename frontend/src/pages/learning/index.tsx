import { useState } from 'react'
import { Typography, Card, Row, Col, Button, Tabs, List, Tag, Space } from 'antd'
import {
  BookOutlined,
  ReadOutlined,
  AudioOutlined,
  EditOutlined,
  ArrowRightOutlined,
} from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'

const { Title, Paragraph } = Typography

interface LearningModule {
  id: string
  title: string
  description: string
  icon: React.ReactNode
  color: string
  level: string
  progress: number
}

const modules: LearningModule[] = [
  {
    id: 'vocabulary',
    title: '词汇学习',
    description: '学习法语核心词汇，按主题分类',
    icon: <BookOutlined />,
    color: '#52c41a',
    level: 'A1-B2',
    progress: 35,
  },
  {
    id: 'grammar',
    title: '语法学习',
    description: '系统学习法语语法规则',
    icon: <EditOutlined />,
    color: '#1890ff',
    level: 'A1-B2',
    progress: 28,
  },
  {
    id: 'reading',
    title: '阅读理解',
    description: '通过阅读文章提高理解能力',
    icon: <ReadOutlined />,
    color: '#722ed1',
    level: 'A2-B2',
    progress: 15,
  },
  {
    id: 'listening',
    title: '听力训练',
    description: '通过听力材料提高听力水平',
    icon: <AudioOutlined />,
    color: '#faad14',
    level: 'A1-B2',
    progress: 20,
  },
]

const topics = [
  { id: 'topic_salutation', name: '问候与告别', level: 'A1', count: 15 },
  { id: 'topic_famille', name: '家庭', level: 'A1', count: 25 },
  { id: 'topic_nourriture', name: '食物与饮料', level: 'A1', count: 30 },
  { id: 'topic_couleur', name: '颜色', level: 'A1', count: 12 },
  { id: 'topic_nombre', name: '数字', level: 'A1', count: 20 },
  { id: 'topic_temps', name: '时间', level: 'A1', count: 18 },
]

const grammarTopics = [
  { id: 'grammar_noun_gender', name: '名词的性', level: 'A1', prerequisites: [] },
  { id: 'grammar_article_def', name: '定冠词', level: 'A1', prerequisites: ['名词的性'] },
  { id: 'grammar_article_indef', name: '不定冠词', level: 'A1', prerequisites: ['名词的性'] },
  { id: 'grammar_prt_now', name: '直陈式现在时', level: 'A1', prerequisites: ['名词的性'] },
  { id: 'grammar_negation', name: '否定结构', level: 'A1', prerequisites: ['直陈式现在时'] },
  { id: 'grammar_question', name: '疑问句', level: 'A1', prerequisites: ['直陈式现在时'] },
]

const LearningPage: React.FC = () => {
  const navigate = useNavigate()
  const [activeTab, setActiveTab] = useState('modules')

  return (
    <div>
      <Title level={2}>学习</Title>
      <Paragraph>选择学习内容开始你的法语学习之旅</Paragraph>

      <Tabs
        activeKey={activeTab}
        onChange={setActiveTab}
        items={[
          {
            key: 'modules',
            label: '学习模块',
            children: (
              <Row gutter={[16, 16]}>
                {modules.map((module) => (
                  <Col xs={24} sm={12} lg={6} key={module.id}>
                    <Card
                      hoverable
                      onClick={() => navigate('/exercises')}
                      style={{ height: '100%' }}
                    >
                      <div style={{ textAlign: 'center', marginBottom: 16 }}>
                        <div
                          style={{
                            width: 60,
                            height: 60,
                            borderRadius: '50%',
                            background: module.color,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                            margin: '0 auto',
                            fontSize: 24,
                            color: '#fff',
                          }}
                        >
                          {module.icon}
                        </div>
                      </div>
                      <Title level={4} style={{ textAlign: 'center' }}>
                        {module.title}
                      </Title>
                      <Paragraph type="secondary" style={{ textAlign: 'center' }}>
                        {module.description}
                      </Paragraph>
                      <div style={{ textAlign: 'center' }}>
                        <Tag>{module.level}</Tag>
                      </div>
                      <div style={{ marginTop: 16 }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: 4 }}>
                          <span>进度</span>
                          <span>{module.progress}%</span>
                        </div>
                        <div
                          style={{
                            height: 6,
                            background: '#f0f0f0',
                            borderRadius: 3,
                          }}
                        >
                          <div
                            style={{
                              width: `${module.progress}%`,
                              height: '100%',
                              background: module.color,
                              borderRadius: 3,
                            }}
                          />
                        </div>
                      </div>
                    </Card>
                  </Col>
                ))}
              </Row>
            ),
          },
          {
            key: 'vocabulary',
            label: '词汇主题',
            children: (
              <Card>
                <List
                  dataSource={topics}
                  renderItem={(topic) => (
                    <List.Item
                      actions={[
                        <Button type="link" onClick={() => navigate('/exercises')}>
                          开始学习 <ArrowRightOutlined />
                        </Button>,
                      ]}
                    >
                      <List.Item.Meta
                        title={
                          <Space>
                            <span>{topic.name}</span>
                            <Tag>{topic.level}</Tag>
                          </Space>
                        }
                        description={`${topic.count} 个词汇`}
                      />
                    </List.Item>
                  )}
                />
              </Card>
            ),
          },
          {
            key: 'grammar',
            label: '语法专题',
            children: (
              <Card>
                <List
                  dataSource={grammarTopics}
                  renderItem={(topic) => (
                    <List.Item
                      actions={[
                        <Button type="link" onClick={() => navigate('/exercises')}>
                          学习 <ArrowRightOutlined />
                        </Button>,
                      ]}
                    >
                      <List.Item.Meta
                        title={
                          <Space>
                            <span>{topic.name}</span>
                            <Tag>{topic.level}</Tag>
                          </Space>
                        }
                        description={
                          topic.prerequisites.length > 0
                            ? `前置知识: ${topic.prerequisites.join(', ')}`
                            : '无前置知识'
                        }
                      />
                    </List.Item>
                  )}
                />
              </Card>
            ),
          },
        ]}
      />
    </div>
  )
}

export default LearningPage
