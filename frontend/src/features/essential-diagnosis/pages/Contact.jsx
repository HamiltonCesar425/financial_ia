import { useState } from "react"

import { sendContact } from "../../../services/api"

const initialForm = {
  name: "",
  email: "",
  message: "",
}

const isValidEmail = (email) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.trim())

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

    if (status === "sending") {
      return
    }

    if (formData.name.trim().length < 2) {
      setError("Informe um nome válido.")
      return
    }

    if (!isValidEmail(formData.email)) {
      setError("Informe um email válido.")
      return
    }

    if (formData.message.trim().length < 10) {
      setError("Escreva uma mensagem um pouco mais completa.")
      return
    }

    setStatus("sending")
    setError("")

    try {
      await sendContact({
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
        <span className="product-tag">Contato</span>

        <h1>Entre em contato com o Financial IA</h1>

        <p>
          Para dúvidas, sugestões, parcerias ou assuntos institucionais, utilize
          o formulário abaixo. As mensagens são analisadas manualmente.
        </p>
      </header>

      <form className="feedback-form" noValidate onSubmit={handleSubmit}>
        <label>
          <span>Nome</span>

          <input
            aria-invalid={error.includes("nome") ? "true" : "false"}
            autoComplete="name"
            disabled={status === "sending"}
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
            aria-invalid={error.includes("email") ? "true" : "false"}
            autoComplete="email"
            disabled={status === "sending"}
            name="email"
            placeholder="Seu email"
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
            placeholder="Escreva sua mensagem."
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
            Mensagem enviada com sucesso.
          </p>
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
