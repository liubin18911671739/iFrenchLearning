import { useState } from 'react'
import { Card, Radio, Button, Typography, Tag, Alert, Space } from 'antd'
import { CheckCircleOutlined, CloseCircleOutlined, ArrowRightOutlined } from '@ant-design/icons'

const { Title, Text } = Typography

interface ExerciseOption {
  id: string
  text: string
}

interface Exercise {
  id: string
  type: 'vocabulary' | 'grammar' | 'translation' | 'reading'
  difficulty: number
  content: string
  question: string
  options?: ExerciseOption[]
  correctAnswer: string
  explanation: string
  knowledgePoints: string[]
  level: string
}

interface ExerciseCardProps {
  exercise: Exercise
  onSubmit: (exerciseId: string, answer: string, correct: boolean) => void
  onNext?: () => void
}

const ExerciseCard: React.FC<ExerciseCardProps> = ({
  exercise,
  onSubmit,
  onNext,
}) => {
  const [selectedAnswer, setSelectedAnswer] = useState<string | null>(null)
  const [isSubmitted, setIsSubmitted] = useState(false)
  const [isCorrect, setIsCorrect] = useState(false)

  const handleSubmit = () => {
    if (!selectedAnswer) return

    const correct = selectedAnswer === exercise.correctAnswer
    setIsCorrect(correct)
    setIsSubmitted(true)
    onSubmit(exercise.id, selectedAnswer, correct)
  }

  const handleNext = () => {
    setSelectedAnswer(null)
    setIsSubmitted(false)
    setIsCorrect(false)
    onNext?.()
  }

  const getDifficultyColor = (difficulty: number) => {
    if (difficulty < 0.3) return 'green'
    if (difficulty < 0.6) return 'orange'
    return 'red'
  }

  const getTypeLabel = (type: string) => {
    const labels: Record<string, string> = {
      vocabulary: '词汇',
      grammar: '语法',
      translation: '翻译',
      reading: '阅读',
    }
    return labels[type] || type
  }

  return (
    <Card
      style={{ maxWidth: 700, margin: '0 auto' }}
      title={
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <span>练习题</span>
          <Space>
            <Tag color="blue">{getTypeLabel(exercise.type)}</Tag>
            <Tag color={getDifficultyColor(exercise.difficulty)}>
              难度: {Math.round(exercise.difficulty * 100)}%
            </Tag>
            <Tag>{exercise.level}</Tag>
          </Space>
        </div>
      }
    >
      <div style={{ marginBottom: 24 }}>
        {exercise.content && (
          <div style={{
            background: '#f5f5f5',
            padding: 16,
            borderRadius: 8,
            marginBottom: 16,
            fontStyle: 'italic',
          }}>
            {exercise.content}
          </div>
        )}
        <Title level={4}>{exercise.question}</Title>
      </div>

      {exercise.options && (
        <Radio.Group
          value={selectedAnswer}
          onChange={(e) => !isSubmitted && setSelectedAnswer(e.target.value)}
          disabled={isSubmitted}
          style={{ width: '100%' }}
        >
          <Space direction="vertical" style={{ width: '100%' }}>
            {exercise.options.map((option) => (
              <Radio
                key={option.id}
                value={option.id}
                style={{
                  width: '100%',
                  padding: '12px 16px',
                  border: '1px solid #d9d9d9',
                  borderRadius: 8,
                  marginLeft: 0,
                  ...(isSubmitted && option.id === exercise.correctAnswer
                    ? { borderColor: '#52c41a', background: '#f6ffed' }
                    : {}),
                  ...(isSubmitted && option.id === selectedAnswer && !isCorrect
                    ? { borderColor: '#f5222d', background: '#fff2f0' }
                    : {}),
                }}
              >
                {option.text}
                {isSubmitted && option.id === exercise.correctAnswer && (
                  <CheckCircleOutlined style={{ color: '#52c41a', marginLeft: 8 }} />
                )}
                {isSubmitted && option.id === selectedAnswer && !isCorrect && (
                  <CloseCircleOutlined style={{ color: '#f5222d', marginLeft: 8 }} />
                )}
              </Radio>
            ))}
          </Space>
        </Radio.Group>
      )}

      {isSubmitted && (
        <div style={{ marginTop: 24 }}>
          {isCorrect ? (
            <Alert
              type="success"
              message="回答正确！"
              description={exercise.explanation}
              showIcon
              style={{ marginBottom: 16 }}
            />
          ) : (
            <Alert
              type="error"
              message="回答错误"
              description={
                <div>
                  <div style={{ marginBottom: 8 }}>
                    <Text strong>正确答案：</Text>
                    <Text type="danger">
                      {exercise.options?.find(o => o.id === exercise.correctAnswer)?.text}
                    </Text>
                  </div>
                  <div>{exercise.explanation}</div>
                </div>
              }
              showIcon
              style={{ marginBottom: 16 }}
            />
          )}

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
            <Space>
              <Text type="secondary">涉及知识点：</Text>
              {exercise.knowledgePoints.map((kp) => (
                <Tag key={kp}>{kp}</Tag>
              ))}
            </Space>
            {onNext && (
              <Button type="primary" onClick={handleNext}>
                下一题 <ArrowRightOutlined />
              </Button>
            )}
          </div>
        </div>
      )}

      {!isSubmitted && (
        <div style={{ marginTop: 24, textAlign: 'center' }}>
          <Button
            type="primary"
            size="large"
            onClick={handleSubmit}
            disabled={!selectedAnswer}
          >
            提交答案
          </Button>
        </div>
      )}
    </Card>
  )
}

export default ExerciseCard
