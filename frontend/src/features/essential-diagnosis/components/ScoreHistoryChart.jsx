import {
  CartesianGrid,
  Line,
  LineChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts"

function ScoreHistoryChart({ data }) {
  if (!data.length) {
    return null
  }

  return (
    <section className="bg-white rounded-2xl shadow-md p-6 mt-8">
      <h2 className="text-xl font-semibold mb-4">
        Evolução do Score Financeiro
      </h2>

      <ResponsiveContainer width="100%" height={320}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="label" />
          <YAxis domain={[0, 100]} />

          <Tooltip />

          <Line type="monotone" dataKey="score" strokeWidth={2} dot />
        </LineChart>
      </ResponsiveContainer>
    </section>
  )
}

export default ScoreHistoryChart
