import { useState } from "react"

import { sendFeedback } from "../../../services/api"

const initialForm = {
  name: "",
  email: "",
  message: "",
}

export default function Feedback() {
  const [formData, setFormData] = useState(initialForm)
  const [status, setStatus] = useState("idle")
  const [error, setError] = useState("")

  const handleChange = (field, value) => {
    setFormData((current) => ({
      ...current,
      [field]: value,
    }))

    setError("")
    if (status === "success") {
      setStatus("idle")
    }
  }

  const handleSubmit = async (event) => {
    event.preventDefault()

    if (formData.message.trim().length < 3) {
      setError("Escreva uma mensagem um pouco mais completa.")
      return
    }

    setStatus("sending")
    setError("")

    try {
      await sendFeedback({
        name: formData.name,
        email: formData.email,
        message: formData.message,
      })

      setFormData(initialForm)
      setStatus("success")
    } catch (err) {
      setStatus("idle")
      setError("Não foi possível enviar agora. Tente novamente em instantes.")
    }
  }

  return (
    <main className="feedback-page">
      <header className="feedback-hero">
        <span className="product-tag">Feedback</span>
        <h1>Ajude a evoluir o Financial IA</h1>
        <p>
          Este é um produto fundador em evolução contínua. Seu feedback ajuda a priorizar melhorias
          reais, reduzir atrito e tornar o diagnóstico mais útil.
        </p>
      </header>

      <form className="feedback-form" onSubmit={handleSubmit}>
        <label>
          <span>Nome</span>
          <input
            autoComplete="name"
            name="name"
            placeholder="Opcional"
            type="text"
            value={formData.name}
            onChange={(event) => handleChange("name", event.target.value)}
          />
        </label>

        <label>
          <span>Email</span>
          <input
            autoComplete="email"
            name="email"
            placeholder="Opcional"
            type="email"
            value={formData.email}
            onChange={(event) => handleChange("email", event.target.value)}
          />
        </label>

        <label>
          <span>Mensagem</span>
          <textarea
            name="message"
            placeholder="Conte o que funcionou, o que confundiu ou o que você esperava encontrar."
            rows="7"
            value={formData.message}
            onChange={(event) => handleChange("message", event.target.value)}
          />
        </label>

        {error && <p className="feedback-error">{error}</p>}
        {status === "success" && <p className="feedback-success">Feedback enviado com sucesso.</p>}

        <button className="primary-link" disabled={status === "sending"} type="submit">
          {status === "sending" ? "Enviando..." : "Enviar feedback"}
        </button>
      </form>
    </main>
  )
}
