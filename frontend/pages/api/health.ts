import type { NextApiRequest, NextApiResponse } from 'next'

type HealthResponse = {
  status: string
  service: string
  timestamp: string
  version: string
}

export default function handler(
  req: NextApiRequest,
  res: NextApiResponse<HealthResponse>
) {
  res.status(200).json({
    status: 'healthy',
    service: 'rehumanizer-serverless',
    timestamp: new Date().toISOString(),
    version: '2.0.0'
  })
} 