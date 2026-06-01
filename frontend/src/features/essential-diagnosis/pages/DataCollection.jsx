import { Link } from "react-router-dom"

import ScoreForm from "../../../components/ScoreForm"
import ErrorNotice from "../../../components/ErrorNotice"

export default function DataCollection({ onSubmit, loading, error }) {
  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-4 py-8 sm:px-6">
      <div className="w-full max-w-3xl bg-white rounded-2xl shadow-lg p-6 space-y-7 sm:p-10 sm:space-y-8">
        <Link className="page-return-link" to="/">
          Voltar para início
        </Link>

        <div className="text-center space-y-3">
          <h1 className="text-3xl font-bold text-slate-900 sm:text-4xl">
            Vamos analisar sua estrutura financeira
          </h1>

          <p className="text-lg text-slate-600">
            Preencha os indicadores essenciais para iniciar sua análise.
          </p>
        </div>

        <ScoreForm onSubmit={onSubmit} loading={loading} />

        {error ? <ErrorNotice message={error} /> : null}
      </div>
    </div>
  )
}
