import { Typography } from 'antd'

const { Title, Paragraph } = Typography

const ProfilePage: React.FC = () => {
  return (
    <div>
      <Title level={2}>个人中心</Title>
      <Paragraph>管理你的学习档案和设置</Paragraph>
    </div>
  )
}

export default ProfilePage
