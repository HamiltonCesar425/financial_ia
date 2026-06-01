import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"

function normalizeChartData(data) {
  return data
    .map((item, index) => ({
      ...item,
      chartKey: `${index}-${item?.label || "analise"}`,
      chartLabel: item?.label || `Análise ${index + 1}`,
      score: Number(item?.score),
    }))
    .filter((item) => Number.isFinite(item.score))
}

function ScoreHistoryChart({ data }) {
  const chartData = normalizeChartData(data || [])

  if (!chartData.length) {
    return null
  }

  if (chartData.length < 2) {
    return (
      <section className="score-history-empty bg-white rounded-2xl shadow-md p-6 mt-8">
        <h2 className="text-xl font-semibold mb-2">
          Evolução do Score Financeiro
        </h2>

        <p>
          Sua primeira análise foi registrada. O gráfico evolutivo aparecerá
          quando houver pelo menos duas análises para comparação.
        </p>
      </section>
    )
  }

  return (
    <section className="score-history-chart bg-white rounded-2xl shadow-md p-6 mt-8">
      <h2 className="text-xl font-semibold mb-4">
        Evolução do Score Financeiro
      </h2>

      <div className="score-history-plot">
        <ResponsiveContainer width="100%" height="100%">
          <LineChart
            data={chartData}
            margin={{ top: 12, right: 16, bottom: 8, left: 0 }}
          >
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis
              dataKey="chartKey"
              tickFormatter={(_, index) => chartData[index]?.chartLabel || ""}
            />
            <YAxis domain={[0, 100]} />

            <Tooltip
              formatter={(value) => [value, "Score"]}
              labelFormatter={(_, payload) =>
                payload?.[0]?.payload?.chartLabel || ""
              }
            />

            <Line type="monotone" dataKey="score" strokeWidth={2} dot />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </section>
  )
}

export default ScoreHistoryChart
