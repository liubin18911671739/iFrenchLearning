import { useState } from 'react'
import { Typography, Card, Button } from 'antd'
import { ReloadOutlined } from '@ant-design/icons'
import ExerciseCard from '../../components/common/ExerciseCard'

const { Title, Paragraph } = Typography

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

const mockExercises: Exercise[] = [
  {
    id: 'ex1',
    type: 'grammar',
    difficulty: 0.3,
    content: '',
    question: '选择正确的定冠词填空：___ livre est sur la table.',
    options: [
      { id: 'a', text: 'Le' },
      { id: 'b', text: 'La' },
      { id: 'c', text: 'Les' },
      { id: 'd', text: 'Un' },
    ],
    correctAnswer: 'a',
    explanation: 'livre是阳性名词，所以使用阳性定冠词le。',
    knowledgePoints: ['grammar_article_def', 'grammar_noun_gender'],
    level: 'A1',
  },
  {
    id: 'ex2',
    type: 'vocabulary',
    difficulty: 0.2,
    content: '',
    question: '"Bonjour"的中文意思是？',
    options: [
      { id: 'a', text: '再见' },
      { id: 'b', text: '你好' },
      { id: 'c', text: '谢谢' },
      { id: 'd', text: '对不起' },
    ],
    correctAnswer: 'b',
    explanation: 'Bonjour是法语中最常用的问候语，意思是"你好"或"白天好"。',
    knowledgePoints: ['vocab_bonjour'],
    level: 'A1',
  },
]

const ExercisesPage: React.FC = () => {
  const [exercises] = useState<Exercise[]>(mockExercises)
  const [currentExerciseIndex, setCurrentExerciseIndex] = useState(0)
  const [completedCount, setCompletedCount] = useState(0)
  const [correctCount, setCorrectCount] = useState(0)

  const currentExercise = exercises[currentExerciseIndex]

  const handleSubmit = (_exerciseId: string, _answer: string, correct: boolean) => {
    setCompletedCount((prev) => prev + 1)
    if (correct) {
      setCorrectCount((prev) => prev + 1)
    }
  }

  const handleNext = () => {
    if (currentExerciseIndex < exercises.length - 1) {
      setCurrentExerciseIndex((prev) => prev + 1)
    }
  }

  const handleRestart = () => {
    setCurrentExerciseIndex(0)
    setCompletedCount(0)
    setCorrectCount(0)
  }

  return (
    <div>
      <Title level={2}>练习</Title>
      <Paragraph>通过练习巩固所学知识</Paragraph>

      <Card style={{ marginBottom: 24 }}>
        <div style={{ display: 'flex', gap: 24 }}>
          <span>进度：{completedCount}/{exercises.length}</span>
          <span>正确率：{completedCount > 0 ? Math.round((correctCount / completedCount) * 100) : 0}%</span>
        </div>
      </Card>

      {currentExercise ? (
        <ExerciseCard
          exercise={currentExercise}
          onSubmit={handleSubmit}
          onNext={handleNext}
        />
      ) : (
        <Card>
          <div style={{ textAlign: 'center', padding: '40px 0' }}>
            <Title level={3}>练习完成！</Title>
            <Paragraph>
              你完成了 {completedCount} 道题，正确率 {completedCount > 0 ? Math.round((correctCount / completedCount) * 100) : 0}%
            </Paragraph>
            <Button type="primary" onClick={handleRestart}>
              <ReloadOutlined /> 重新开始
            </Button>
          </div>
        </Card>
      )}
    </div>
  )
}

export default ExercisesPage
