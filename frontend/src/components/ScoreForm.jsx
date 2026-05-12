import { useState } from "react";

export default function ScoreForm({ onSubmit, loading }) {
  const [formData, setFormData] = useState({
    receita: "",
    despesas: "",
    divida: "",
    reserva: "",
  });

  const [errors, setErrors] = useState({});

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
  ];

  const validate = () => {
    const nextErrors = {};

    const receita = Number(formData.receita);
    const despesas = Number(formData.despesas);
    const divida = Number(formData.divida);
    const reserva = Number(formData.reserva);

    if (formData.receita === "" || Number.isNaN(receita) || receita <= 0) {
      nextErrors.receita = "Informe uma receita válida.";
    }

    if (formData.despesas === "" || Number.isNaN(despesas) || despesas < 0) {
      nextErrors.despesas = "Informe despesas válidas.";
    }

    if (formData.divida === "" || Number.isNaN(divida) || divida < 0) {
      nextErrors.divida = "Informe uma dívida válida.";
    }

    if (formData.reserva === "" || Number.isNaN(reserva) || reserva < 0) {
      nextErrors.reserva = "Informe uma reserva válida.";
    }

    if (despesas > receita) {
      nextErrors.despesas =
        "As despesas não podem ultrapassar sua receita mensal.";
    }

    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const handleChange = (field, value) => {
    setFormData((current) => ({
      ...current,
      [field]: value,
    }));

    setErrors((current) => ({
      ...current,
      [field]: undefined,
    }));
  };

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!validate()) {
      return;
    }

    onSubmit({
      receita: Number(formData.receita),
      despesas: Number(formData.despesas),
      divida: Number(formData.divida),
      reserva: Number(formData.reserva),
    });
  };

  return (
    <form id="formulario-score" className="score-form" onSubmit={handleSubmit}>
      {fields.map((field) => (
        <label key={field.id} className="field-group">
          <span>{field.label}</span>

          <input
            inputMode="decimal"
            name={field.id}
            placeholder={field.placeholder}
            type="text"
            value={formData[field.id]}
            onChange={(event) => handleChange(field.id, event.target.value)}
          />

          <small>{field.helper}</small>

          {errors[field.id] ? (
            <p className="field-error">{errors[field.id]}</p>
          ) : null}
        </label>
      ))}

      <button className="primary-button" disabled={loading} type="submit">
        {loading ? "Analisando..." : "Calcular meu diagnóstico"}
      </button>
    </form>
  );
}
