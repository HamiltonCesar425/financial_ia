import { useState } from "react";

export default function ScoreForm({ onSubmit, loading }) {
  const [formData, setFormData] = useState({
    receita: "",
    despesas: "",
    divida: "",
  });
  const [errors, setErrors] = useState({});

  const fields = [
    {
      id: "receita",
      label: "Receita mensal",
      placeholder: "5000",
      helper: "A receita deve ser maior que zero.",
    },
    {
      id: "despesas",
      label: "Despesas mensais",
      placeholder: "3000",
      helper: "Despesas podem ser zero, mas nao negativas.",
    },
    {
      id: "divida",
      label: "Divida atual",
      placeholder: "1000",
      helper: "Informe o total atual da sua divida.",
    },
  ];

  const validate = () => {
    const nextErrors = {};
    const receita = Number(formData.receita);
    const despesas = Number(formData.despesas);
    const divida = Number(formData.divida);

    if (formData.receita === "" || Number.isNaN(receita) || receita <= 0) {
      nextErrors.receita = "Informe sua receita. Ela deve ser maior que zero.";
    }

    if (formData.despesas === "" || Number.isNaN(despesas) || despesas < 0) {
      nextErrors.despesas = "Informe despesas validas. Elas nao podem ser negativas.";
    }

    if (formData.divida === "" || Number.isNaN(divida) || divida < 0) {
      nextErrors.divida = "Informe a divida atual. Ela nao pode ser negativa.";
    }

    setErrors(nextErrors);
    return Object.keys(nextErrors).length === 0;
  };

  const handleChange = (field, value) => {
    setFormData((current) => ({ ...current, [field]: value }));
    setErrors((current) => ({ ...current, [field]: undefined }));
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
    });
  };

  return (
    <form id="formulario-score" className="score-form" onSubmit={handleSubmit}>
      {fields.map((field) => (
        <label key={field.id} className="field-group">
          <span>{field.label}</span>
          <input
            inputMode="decimal"
            min="0"
            name={field.id}
            placeholder={field.placeholder}
            step="any"
            type="number"
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
        {loading ? "Analisando seus dados..." : "Calcular meu score"}
      </button>
    </form>
  );
}
