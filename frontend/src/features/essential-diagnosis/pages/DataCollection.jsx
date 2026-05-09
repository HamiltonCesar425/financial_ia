import ScoreForm from "../../../components/ScoreForm";
import ErrorNotice from "../../../components/ErrorNotice";

export default function DataCollection({ onSubmit, loading, error }) {
  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-6">
      <div className="w-full max-w-3xl bg-white rounded-2xl shadow-lg p-10 space-y-8">

        <div className="text-center space-y-3">
          <p className="text-sm font-medium text-slate-500">
            Etapa 1 de 3
          </p>

          <h1 className="text-4xl font-bold text-slate-900">
            Vamos analisar sua estrutura financeira
          </h1>

          <p className="text-lg text-slate-600">
            Preencha os indicadores essenciais para iniciar sua análise.
          </p>
        </div>

        <ScoreForm onSubmit={onSubmit} loading={loading} />

        {error && <ErrorNotice message={error} />}

      </div>
    </div>
  );
}
