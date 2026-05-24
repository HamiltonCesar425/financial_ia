import { useState } from "react"

import { sendContact } from "../../../services/api"

const initialForm = {
  name: "",
  email: "",
  message: "",
}

export default function Contact() {
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

    if (formData.name.trim().length < 2) {
      setError("Informe um nome válido.")
      return
    }

    if (!formData.email.includes("@")) {
      setError("Informe um email válido.")
      return
    }

    if (formData.message.trim().length < 3) {
      setError("Escreva uma mensagem um pouco mais completa.")
      return
    }

    setStatus("sending")
    setError("")

    try {
      await sendContact({
        name: formData.name,
        email: formData.email,
        message: formData.message,
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
        <span className="product-tag">Contato</span>

        <h1>Entre em contato com o Financial IA</h1>

        <p>
          Para dúvidas, sugestões, parcerias ou assuntos institucionais, utilize
          o formulário abaixo. As mensagens são analisadas manualmente.
        </p>
      </header>

      <form className="feedback-form" onSubmit={handleSubmit}>
        <label>
          <span>Nome</span>

          <input
            autoComplete="name"
            name="name"
            placeholder="Seu nome"
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
            placeholder="Seu melhor email"
            type="email"
            value={formData.email}
            onChange={(event) => handleChange("email", event.target.value)}
          />
        </label>

        <label>
          <span>Mensagem</span>

          <textarea
            name="message"
            placeholder="Escreva sua mensagem."
            rows="7"
            value={formData.message}
            onChange={(event) => handleChange("message", event.target.value)}
          />
        </label>

        {error && <p className="feedback-error">{error}</p>}

        {status === "success" && (
          <p className="feedback-success">Mensagem enviada com sucesso.</p>
        )}

        <button
          className="primary-link"
          disabled={status === "sending"}
          type="submit"
        >
          {status === "sending" ? "Enviando..." : "Enviar mensagem"}
        </button>
      </form>
    </main>
  )
}
