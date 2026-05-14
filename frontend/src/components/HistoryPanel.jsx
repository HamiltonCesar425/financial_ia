import { getHistory } from "../utils/historyStorage"

export default function HistoryPanel() {
  const history = getHistory()

  const formatCurrency = (value) =>
    new Intl.NumberFormat("pt-BR", {
      style: "currency",
      currency: "BRL",
    }).format(Number(value || 0))

  const formatDate = (date) => new Date(date).toLocaleDateString("pt-BR")

  if (!history.length) {
    return null
  }

  return (
    <section className="card history-card">
      <div className="section-heading">
        <span className="eyebrow">Histórico</span>
        <h2>Evolução financeira</h2>
      </div>

      <div className="history-list">
        {[...history].reverse().map((entry) => (
          <div key={entry.id} className="history-item">
            <div>
              <strong>Score {entry.score}</strong>
              <span>. {entry.classification}</span>
            </div>

            <small>{formatDate(entry.timestamp)}</small>

            <p>
              Receita: {formatCurrency(entry.receita)} | Despesas: {formatCurrency(entry.despesas)}
            </p>
          </div>
        ))}
      </div>

      <button
        className="secondary-button"
        onClick={() => {
          cleanHistory()
          window.location.reload()
        }}
      >
        Limpar histórico
      </button>
    </section>
  )
}
