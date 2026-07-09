import { useState } from 'react'

interface Message {
  // the question the user asked
  question: string
  // the answer returned by the backend
  answer: string
}

function App() {
  // holds the full conversation history shown on screen
  const [messages, setMessages] = useState<Message[]>([])
  // holds whatever the user is currently typing
  const [input, setInput] = useState('')
  // true while waiting for the backend to respond, so we can disable the button/show a spinner
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    // don't send empty questions
    if (!input.trim()) return

    // disables the button/shows loading state while waiting
    setLoading(true)

    // sends the question to the backend, matching the ChatRequest shape it expects
    const response = await fetch('http://localhost:8000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question: input }),
    })

    // parses the JSON response body, matching the ChatResponse shape
    const data = await response.json()

    // adds this question/answer pair to the conversation history
    setMessages([...messages, { question: input, answer: data.answer }])

    // clears the input box for the next question
    setInput('')

    // re-enables the button now that we have a response
    setLoading(false)
  }

  return (
    <div>
      <h1>LocalMind</h1>

      <div>
        {/* renders one block per question/answer pair in the conversation history */}
        {messages.map((message, index) => (
          <div key={index}>
            <p><strong>You:</strong> {message.question}</p>
            <p><strong>LocalMind:</strong> {message.answer}</p>
          </div>
        ))}
      </div>

      {/* two-way binding: typing updates `input`, and `input` controls what's shown */}
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Ask a question..."
      />
      {/* disabled while waiting for a response, so you can't send twice at once */}
      <button onClick={sendMessage} disabled={loading}>
        {loading ? 'Thinking...' : 'Send'}
      </button>
    </div>
  )
}

export default App
