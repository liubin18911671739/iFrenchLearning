import { useState, useEffect } from 'react'
import { Typography, Card, Row, Col, Button, Space, Tag, Progress, Statistic } from 'antd'
import {
  BookOutlined,
  TrophyOutlined,
  ClockCircleOutlined,
  RiseOutlined,
  ArrowRightOutlined,
} from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import { useLearnerStore } from '../../stores'

const { Title, Paragraph } = Typography

const HomePage: React.FC = () => {
  const navigate = useNavigate()
  const { name, level, overallMastery } = useLearnerStore()
  const [stats, setStats] = useState({
    learnedPoints: 0,
    masteredPoints: 0,
    studyHours: 0,
    streakDays: 0,
  })

  useEffect(() => {
    // 模拟统计数据
    setStats({
      learnedPoints: 12,
      masteredPoints: 5,
      studyHours: 8.5,
      streakDays: 3,
    })
  }, [])

  return (
    <div>
      <Title level={2}>欢迎回来，{name || '学习者'}！</Title>
      <Paragraph>继续你的法语学习之旅</Paragraph>

      {/* 统计卡片 */}
      <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
        <Col xs={24} sm={12} lg={6}>
          <Card hoverable onClick={() => navigate('/learning')}>
            <Statistic
              title="已学知识点"
              value={stats.learnedPoints}
              prefix={<BookOutlined />}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card hoverable>
            <Statistic
              title="掌握率"
              value={Math.round(overallMastery * 100)}
              suffix="%"
              prefix={<TrophyOutlined />}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card hoverable>
            <Statistic
              title="学习时长"
              value={stats.studyHours}
              suffix="小时"
              prefix={<ClockCircleOutlined />}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
        <Col xs={24} sm={12} lg={6}>
          <Card hoverable>
            <Statistic
              title="连续学习"
              value={stats.streakDays}
              suffix="天"
              prefix={<RiseOutlined />}
              valueStyle={{ color: '#faad14' }}
            />
          </Card>
        </Col>
      </Row>

      {/* 学习进度 */}
      <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
        <Col xs={24} lg={16}>
          <Card title="今日推荐" style={{ height: '100%' }}>
            <Paragraph>
              根据你的学习状态，我们为你推荐以下内容：
            </Paragraph>
            <Space direction="vertical" style={{ width: '100%' }}>
              <Card type="inner" size="small">
                <Space>
                  <Tag color="blue">语法</Tag>
                  <span>直陈式现在时 - 动词变位练习</span>
                </Space>
                <Progress percent={65} size="small" style={{ marginTop: 8 }} />
              </Card>
              <Card type="inner" size="small">
                <Space>
                  <Tag color="green">词汇</Tag>
                  <span>食物与饮料 - 词汇学习</span>
                </Space>
                <Progress percent={40} size="small" style={{ marginTop: 8 }} />
              </Card>
              <Card type="inner" size="small">
                <Space>
                  <Tag color="orange">复习</Tag>
                  <span>定冠词与不定冠词 - 复习</span>
                </Space>
                <Progress percent={80} size="small" style={{ marginTop: 8 }} />
              </Card>
            </Space>
            <Button
              type="primary"
              style={{ marginTop: 16 }}
              onClick={() => navigate('/exercises')}
            >
              开始学习 <ArrowRightOutlined />
            </Button>
          </Card>
        </Col>
        <Col xs={24} lg={8}>
          <Card title="学习目标" style={{ height: '100%' }}>
            <div style={{ textAlign: 'center', padding: '20px 0' }}>
              <div style={{ marginBottom: 16 }}>
                <Tag color="blue" style={{ fontSize: 16, padding: '4px 12px' }}>
                  当前等级：{level || 'A1'}
                </Tag>
              </div>
              <div style={{ fontSize: 24, marginBottom: 16 }}>↓</div>
              <div>
                <Tag color="green" style={{ fontSize: 16, padding: '4px 12px' }}>
                  目标等级：B1
                </Tag>
              </div>
            </div>
            <Progress
              percent={25}
              strokeColor="#52c41a"
              style={{ marginTop: 16 }}
            />
            <Paragraph type="secondary" style={{ textAlign: 'center', marginTop: 8 }}>
              完成度 25%
            </Paragraph>
          </Card>
        </Col>
      </Row>

      {/* 快捷入口 */}
      <Row gutter={[16, 16]} style={{ marginTop: 24 }}>
        <Col xs={24} sm={8}>
          <Card
            hoverable
            onClick={() => navigate('/knowledge-graph')}
            style={{ textAlign: 'center' }}
          >
            <BookOutlined style={{ fontSize: 32, color: '#1890ff' }} />
            <Title level={4} style={{ marginTop: 16 }}>知识图谱</Title>
            <Paragraph type="secondary">浏览完整知识体系</Paragraph>
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card
            hoverable
            onClick={() => navigate('/diagnostics')}
            style={{ textAlign: 'center' }}
          >
            <TrophyOutlined style={{ fontSize: 32, color: '#52c41a' }} />
            <Title level={4} style={{ marginTop: 16 }}>诊断报告</Title>
            <Paragraph type="secondary">查看薄弱点分析</Paragraph>
          </Card>
        </Col>
        <Col xs={24} sm={8}>
          <Card
            hoverable
            onClick={() => navigate('/profile')}
            style={{ textAlign: 'center' }}
          >
            <ClockCircleOutlined style={{ fontSize: 32, color: '#722ed1' }} />
            <Title level={4} style={{ marginTop: 16 }}>学习档案</Title>
            <Paragraph type="secondary">查看学习历史</Paragraph>
          </Card>
        </Col>
      </Row>
    </div>
  )
}

export default HomePage
