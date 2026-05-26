import { useState } from "react"

import { sendFeedback } from "../../../services/api"

const initialForm = {
  name: "",
  email: "",
  message: "",
}

const isValidEmail = (email) =>
  email.trim() === "" || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())

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

    if (status === "sending") {
      return
    }

    if (!isValidEmail(formData.email)) {
      setError("Informe um email válido ou deixe o campo em branco.")
      return
    }

    if (formData.message.trim().length < 10) {
      setError("Escreva uma mensagem um pouco mais completa.")
      return
    }

    setStatus("sending")
    setError("")

    try {
      await sendFeedback({
        name: formData.name.trim(),
        email: formData.email.trim(),
        message: formData.message.trim(),
      })

      setFormData(initialForm)
      setStatus("success")
    } catch (error) {
      console.error(error)
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
          Esta plataforma está em evolução contínua, e seu feedback ajuda
          diretamente na melhoria da experiência e das análises oferecidas.
        </p>
      </header>

      <form className="feedback-form" noValidate onSubmit={handleSubmit}>
        <label>
          <span>Nome</span>
          <input
            autoComplete="name"
            disabled={status === "sending"}
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
            aria-invalid={error.includes("email") ? "true" : "false"}
            autoComplete="email"
            disabled={status === "sending"}
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
            aria-invalid={error.includes("mensagem") ? "true" : "false"}
            disabled={status === "sending"}
            name="message"
            placeholder="Conte o que na sua opinião funcionou, o que confundiu você ou o que esperava encontrar."
            rows="7"
            value={formData.message}
            onChange={(event) => handleChange("message", event.target.value)}
          />
        </label>

        {error && (
          <p className="feedback-error" role="alert">
            {error}
          </p>
        )}
        {status === "success" && (
          <p className="feedback-success" role="status">
            Feedback enviado com sucesso.
          </p>
        )}

        <button
          className="primary-link"
          disabled={status === "sending"}
          type="submit"
        >
          {status === "sending" ? "Enviando..." : "Enviar feedback"}
        </button>
      </form>
    </main>
  )
}
