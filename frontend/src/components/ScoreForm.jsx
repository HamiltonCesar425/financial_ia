import { useState } from "react"

const fields = [
  {
    id: "receita",
    label: "Receita mensal",
    placeholder: "5000",
    helper: "Informe sua entrada financeira mensal principal.",
  },
  {
    id: "despesas",
    label: "Despesas mensais",
    placeholder: "3000",
    helper: "Some seus custos fixos e recorrentes.",
  },
  {
    id: "divida",
    label: "Dívida atual",
    placeholder: "1000",
    helper: "Inclua financiamentos, empréstimos e parcelamentos.",
  },
  {
    id: "reserva",
    label: "Reserva financeira",
    placeholder: "2000",
    helper: "Valor disponível para emergências ou liquidez imediata.",
  },
]

const parseCurrencyValue = (value) => {
  const sanitizedValue = value
    .trim()
    .replace(/^R\$\s?/i, "")
    .replace(/\s/g, "")

  if (!sanitizedValue) {
    return Number.NaN
  }

  const normalizedValue = sanitizedValue.includes(",")
    ? sanitizedValue.replace(/\./g, "").replace(",", ".")
    : sanitizedValue.replace(/^(\d{1,3})(\.\d{3})+$/, (value) =>
        value.replace(/\./g, ""),
      )

  return Number(normalizedValue)
}

export default function ScoreForm({ onSubmit, loading }) {
  const [formData, setFormData] = useState({
    receita: "",
    despesas: "",
    divida: "",
    reserva: "",
  })

  const [errors, setErrors] = useState({})

  const validate = () => {
    const nextErrors = {}
    const parsedData = {
      receita: parseCurrencyValue(formData.receita),
      despesas: parseCurrencyValue(formData.despesas),
      divida: parseCurrencyValue(formData.divida),
      reserva: parseCurrencyValue(formData.reserva),
    }

    if (
      formData.receita.trim() === "" ||
      !Number.isFinite(parsedData.receita) ||
      parsedData.receita <= 0
    ) {
      nextErrors.receita = "Informe uma receita válida."
    }

    if (
      formData.despesas.trim() === "" ||
      !Number.isFinite(parsedData.despesas) ||
      parsedData.despesas < 0
    ) {
      nextErrors.despesas = "Informe despesas válidas."
    }

    if (
      formData.divida.trim() === "" ||
      !Number.isFinite(parsedData.divida) ||
      parsedData.divida < 0
    ) {
      nextErrors.divida = "Informe uma dívida válida."
    }

    if (
      formData.reserva.trim() === "" ||
      !Number.isFinite(parsedData.reserva) ||
      parsedData.reserva < 0
    ) {
      nextErrors.reserva = "Informe uma reserva válida."
    }

    if (
      !nextErrors.receita &&
      !nextErrors.despesas &&
      parsedData.despesas > parsedData.receita
    ) {
      nextErrors.despesas =
        "As despesas não podem ultrapassar sua receita mensal."
    }

    setErrors(nextErrors)

    if (Object.keys(nextErrors).length > 0) {
      return null
    }

    return parsedData
  }

  const handleChange = (field, value) => {
    setFormData((current) => ({
      ...current,
      [field]: value,
    }))

    setErrors((current) => {
      const nextErrors = { ...current }
      delete nextErrors[field]
      return nextErrors
    })
  }

  const handleSubmit = (event) => {
    event.preventDefault()

    if (loading) {
      return
    }

    const parsedData = validate()

    if (!parsedData) {
      return
    }

    onSubmit(parsedData)
  }

  return (
    <form id="formulario-score" className="score-form" onSubmit={handleSubmit}>
      {fields.map((field) => (
        <label key={field.id} className="field-group">
          <span>{field.label}</span>

          <input
            aria-describedby={`${field.id}-helper ${
              errors[field.id] ? `${field.id}-error` : ""
            }`.trim()}
            aria-invalid={errors[field.id] ? "true" : "false"}
            disabled={loading}
            id={field.id}
            inputMode="decimal"
            name={field.id}
            placeholder={field.placeholder}
            type="text"
            value={formData[field.id]}
            onChange={(event) => handleChange(field.id, event.target.value)}
          />

          <small id={`${field.id}-helper`}>{field.helper}</small>

          {errors[field.id] ? (
            <p className="field-error" id={`${field.id}-error`}>
              {errors[field.id]}
            </p>
          ) : null}
        </label>
      ))}

      <button className="primary-button" disabled={loading} type="submit">
        {loading ? "Analisando..." : "Calcular meu diagnóstico"}
      </button>
    </form>
  )
}
