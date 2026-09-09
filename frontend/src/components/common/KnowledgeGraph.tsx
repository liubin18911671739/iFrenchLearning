import { useEffect, useRef, useState, useCallback } from 'react'
import * as d3 from 'd3'
import { Card, Spin, Empty, Tag, Tooltip } from 'antd'
import { ZoomInOutlined, ZoomOutOutlined, ReloadOutlined } from '@ant-design/icons'

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
  weight?: number
}

interface KnowledgeGraphProps {
  nodes: GraphNode[]
  edges: GraphEdge[]
  width?: number
  height?: number
  onNodeClick?: (node: GraphNode) => void
  loading?: boolean
}

const categoryColors: Record<string, string> = {
  grammar: '#1890ff',
  vocabulary: '#52c41a',
  verb_conjugation: '#faad14',
  accord: '#f5222d',
}

const KnowledgeGraph: React.FC<KnowledgeGraphProps> = ({
  nodes,
  edges,
  width = 900,
  height = 600,
  onNodeClick,
  loading = false,
}) => {
  const svgRef = useRef<SVGSVGElement>(null)
  const [selectedNode, setSelectedNode] = useState<GraphNode | null>(null)

  const getNodeColor = useCallback((node: GraphNode) => {
    if (node.mastery !== undefined) {
      if (node.mastery >= 0.8) return '#52c41a'
      if (node.mastery >= 0.5) return '#faad14'
      return '#f5222d'
    }
    return categoryColors[node.category] || '#999'
  }, [])

  useEffect(() => {
    if (!svgRef.current || nodes.length === 0) return

    const svg = d3.select(svgRef.current)
    svg.selectAll('*').remove()

    const g = svg.append('g')
    
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.3, 3])
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      .on('zoom', (event: any) => {
        g.attr('transform', event.transform)
      })

    svg.call(zoom)

    const simulation = d3.forceSimulation(nodes as any)
      .force('link', d3.forceLink(edges as any).id((d: any) => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(30))

    const link = g.append('g')
      .selectAll('line')
      .data(edges)
      .join('line')
      .attr('stroke', '#999')
      .attr('stroke-opacity', 0.6)
      .attr('stroke-width', 2)

    const node = g.append('g')
      .selectAll('g')
      .data(nodes)
      .join('g')

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    node.call(d3.drag<any, GraphNode>()
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      .on('start', (event: any, d: any) => {
        if (!event.active) simulation.alphaTarget(0.3).restart()
        d.fx = d.x
        d.fy = d.y
      })
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      .on('drag', (event: any, d: any) => {
        d.fx = event.x
        d.fy = event.y
      })
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      .on('end', (event: any, d: any) => {
        if (!event.active) simulation.alphaTarget(0)
        d.fx = null
        d.fy = null
      }))

    node.append('circle')
      .attr('r', 18)
      .attr('fill', (d) => getNodeColor(d))
      .attr('stroke', '#fff')
      .attr('stroke-width', 2)
      .style('cursor', 'pointer')
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      .on('click', (event: any, d: any) => {
        event.stopPropagation()
        setSelectedNode(d)
        onNodeClick?.(d)
      })

    node.append('text')
      .text((d) => d.name.length > 6 ? d.name.slice(0, 6) + '...' : d.name)
      .attr('text-anchor', 'middle')
      .attr('dy', 30)
      .style('font-size', '11px')
      .style('fill', '#333')

    // eslint-disable-next-line @typescript-eslint/no-explicit-any
    simulation.on('tick', () => {
      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      link.attr('x1', (d: any) => d.source.x)
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .attr('y1', (d: any) => d.source.y)
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .attr('x2', (d: any) => d.target.x)
        // eslint-disable-next-line @typescript-eslint/no-explicit-any
        .attr('y2', (d: any) => d.target.y)

      // eslint-disable-next-line @typescript-eslint/no-explicit-any
      node.attr('transform', (d: any) => `translate(${d.x},${d.y})`)
    })

    return () => {
      simulation.stop()
    }
  }, [nodes, edges, width, height, getNodeColor, onNodeClick])

  if (loading) {
    return (
      <Card>
        <div style={{ textAlign: 'center', padding: '100px 0' }}>
          <Spin size="large" tip="加载知识图谱..." />
        </div>
      </Card>
    )
  }

  if (nodes.length === 0) {
    return (
      <Card>
        <Empty description="暂无知识图谱数据" />
      </Card>
    )
  }

  return (
    <Card
      title="知识图谱"
      extra={
        <div style={{ display: 'flex', gap: 8 }}>
          <Tooltip title="放大">
            <ZoomInOutlined style={{ cursor: 'pointer', fontSize: 16 }} />
          </Tooltip>
          <Tooltip title="缩小">
            <ZoomOutOutlined style={{ cursor: 'pointer', fontSize: 16 }} />
          </Tooltip>
          <Tooltip title="重置">
            <ReloadOutlined style={{ cursor: 'pointer', fontSize: 16 }} />
          </Tooltip>
        </div>
      }
    >
      <div style={{ position: 'relative' }}>
        <svg
          ref={svgRef}
          width={width}
          height={height}
          style={{ border: '1px solid #f0f0f0', borderRadius: 8 }}
        />
        
        <div style={{
          position: 'absolute',
          top: 10,
          left: 10,
          background: 'rgba(255,255,255,0.9)',
          padding: '8px 12px',
          borderRadius: 4,
          fontSize: 12,
        }}>
          <div style={{ marginBottom: 4, fontWeight: 'bold' }}>图例：</div>
          <div><span style={{ color: '#52c41a' }}>●</span> 已掌握 (≥80%)</div>
          <div><span style={{ color: '#faad14' }}>●</span> 学习中 (50-80%)</div>
          <div><span style={{ color: '#f5222d' }}>●</span> 薄弱 (&lt;50%)</div>
        </div>

        {selectedNode && (
          <div style={{
            position: 'absolute',
            bottom: 10,
            right: 10,
            background: 'rgba(255,255,255,0.95)',
            padding: '12px 16px',
            borderRadius: 8,
            boxShadow: '0 2px 8px rgba(0,0,0,0.15)',
            minWidth: 200,
          }}>
            <div style={{ fontWeight: 'bold', marginBottom: 8 }}>{selectedNode.name}</div>
            <div style={{ marginBottom: 4 }}>
              <Tag>{selectedNode.level}</Tag>
              <Tag>{selectedNode.category}</Tag>
            </div>
            {selectedNode.mastery !== undefined && (
              <div>掌握度：{Math.round(selectedNode.mastery * 100)}%</div>
            )}
          </div>
        )}
      </div>
    </Card>
  )
}

export default KnowledgeGraph
