import './globals.css'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: 'ReHumanizer - AI Text Humanization',
  description: 'Transform AI-generated text into natural, human-like content that bypasses AI detection.',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  )
} 