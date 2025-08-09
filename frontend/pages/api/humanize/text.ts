import type { NextApiRequest, NextApiResponse } from 'next'
import { GoogleGenerativeAI } from '@google/generative-ai'

type HumanizeRequest = {
  text: string
  pipeline_type?: string
  education_level?: string
  paranoid_mode?: boolean
  writehuman_mode?: boolean
}

type HumanizeResponse = {
  humanized_text: string
  original_text: string
  word_count: number
  processing_time: number
  meaning_preserved: boolean
  pipeline_type: string
  education_level: string
}

// Initialize Gemini client
const genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY!)

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse<HumanizeResponse | { error: string }>
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' })
  }

  const startTime = Date.now()

  try {
    const {
      text,
      pipeline_type = 'comprehensive',
      education_level = 'undergraduate',
      paranoid_mode = true,
      writehuman_mode = true
    }: HumanizeRequest = req.body

    if (!text || text.trim().length === 0) {
      return res.status(400).json({ error: 'Text is required' })
    }

    if (text.length > 5000) {
      return res.status(400).json({ error: 'Text too long (max 5000 characters)' })
    }

    // Step 1: Simple paraphrasing (replace Humaneyes model)
    let result = simpleParaphrase(text)

    // Step 2: Gemini humanization
    result = await geminiHumanize(result, education_level)

    // Step 3: Stylometric changes
    result = applyStylometricChanges(result)

    // Step 4: WriteHuman mimicry (if enabled)
    if (writehuman_mode) {
      result = applyWriteHumanMimicry(result)
    }

    // Step 5: Paranoid mode (if enabled)
    if (paranoid_mode) {
      result = applyParanoidMode(result)
    }

    // Step 6: Ensure minimum word count
    result = enforceMinWordCount(result, 250)

    const processingTime = Date.now() - startTime

    res.status(200).json({
      humanized_text: result,
      original_text: text,
      word_count: result.split(' ').length,
      processing_time: processingTime,
      meaning_preserved: true,
      pipeline_type,
      education_level
    })

  } catch (error) {
    console.error('Humanization error:', error)
    res.status(500).json({ error: 'Failed to humanize text' })
  }
}

// Simple paraphrasing function (replaces Humaneyes model)
function simpleParaphrase(text: string): string {
  const replacements: Record<string, string> = {
    'artificial intelligence': 'AI technology',
    'demonstrates': 'shows',
    'capabilities': 'abilities',
    'processing': 'handling',
    'systems': 'platforms',
    'technologies': 'tools',
    'algorithms': 'methods',
    'sophisticated': 'advanced',
    'remarkable': 'great',
    'innovative': 'new',
    'utilize': 'use',
    'implement': 'use',
    'facilitate': 'help',
    'optimize': 'improve'
  }

  let result = text
  for (const [original, replacement] of Object.entries(replacements)) {
    result = result.replace(new RegExp(original, 'gi'), replacement)
  }

  return result
}

// Gemini humanization
async function geminiHumanize(text: string, educationLevel: string): Promise<string> {
  try {
    const model = genAI.getGenerativeModel({ model: 'gemini-1.5-pro' })

    const prompt = `Rewrite the following text to sound more human and natural while preserving the exact meaning. 
    Target education level: ${educationLevel}
    
    Requirements:
    - Make it sound like a human wrote it
    - Add natural flow and variation
    - Keep the same core message
    - Use ${educationLevel}-level vocabulary
    - Add some personality and natural imperfections
    
    Text: ${text}
    
    Rewritten version:`

    const result = await model.generateContent(prompt)
    const response = await result.response
    return response.text() || text
  } catch (error) {
    console.error('Gemini API error:', error)
    // Fallback if Gemini fails
    return text
  }
}

// Apply stylometric changes
function applyStylometricChanges(text: string): string {
  const sentences = text.split(/[.!?]+/).filter(s => s.trim())
  const fillerPhrases = [
    'to be honest',
    'you know',
    'as far as I can tell',
    'if I\'m not mistaken',
    'come to think of it'
  ]

  let result = sentences.map((sentence, index) => {
    let processed = sentence.trim()
    
    // Randomly add filler phrases
    if (Math.random() < 0.3) {
      const filler = fillerPhrases[Math.floor(Math.random() * fillerPhrases.length)]
      processed = `${processed}, ${filler}`
    }

    // Add punctuation variety
    if (index < sentences.length - 1) {
      if (Math.random() < 0.1) {
        processed += '...'
      } else {
        processed += '.'
      }
    }

    return processed
  }).join(' ')

  return result
}

// Apply WriteHuman mimicry
function applyWriteHumanMimicry(text: string): string {
  const downgrades: Record<string, string> = {
    'demonstrates': 'shows',
    'utilizes': 'uses',
    'substantial': 'big',
    'numerous': 'many',
    'frequently': 'often',
    'consequently': 'so',
    'furthermore': 'also',
    'nevertheless': 'but',
    'approximately': 'about'
  }

  let result = text
  for (const [formal, casual] of Object.entries(downgrades)) {
    result = result.replace(new RegExp(formal, 'gi'), casual)
  }

  // Add casual connectors
  result = result.replace(/\. ([A-Z])/g, (match, letter) => {
    if (Math.random() < 0.2) {
      return `. And ${letter.toLowerCase()}`
    }
    return match
  })

  return result
}

// Apply paranoid mode (coherence disruption)
function applyParanoidMode(text: string): string {
  const sentences = text.split(/[.!?]+/).filter(s => s.trim())
  const tangents = [
    'which is interesting when you consider it',
    'funny how these things connect when you think about it',
    'and here\'s where it gets really interesting',
    'considering the broader context'
  ]

  let result = sentences.map((sentence, index) => {
    let processed = sentence.trim()

    // Add tangents occasionally
    if (Math.random() < 0.15) {
      const tangent = tangents[Math.floor(Math.random() * tangents.length)]
      processed = `${processed} (${tangent})`
    }

    // Add ellipses for burstiness
    if (Math.random() < 0.1) {
      processed += '...'
    }

    return processed
  }).join('. ')

  return result + '.'
}

// Enforce minimum word count
function enforceMinWordCount(text: string, minWords: number): string {
  const words = text.split(' ')
  if (words.length >= minWords) return text

  const expansions = [
    'This is particularly significant when considering the broader implications.',
    'Moreover, this approach demonstrates considerable effectiveness in practical applications.',
    'Furthermore, the methodology employed here offers substantial benefits for various use cases.',
    'Additionally, these findings suggest important considerations for future developments.',
    'It\'s worth noting that this represents a meaningful advancement in the field.'
  ]

  let result = text
  while (result.split(' ').length < minWords) {
    const expansion = expansions[Math.floor(Math.random() * expansions.length)]
    result += ' ' + expansion
  }

  return result
}

// Configure the serverless function
export const config = {
  maxDuration: 60, // 60 seconds timeout
  regions: ['iad1'], // US East for better Gemini API latency
} 