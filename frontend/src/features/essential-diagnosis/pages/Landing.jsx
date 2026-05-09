export default function Landing({ onStart }) {
  return (
    <div className="min-h-screen bg-slate-50 flex items-center justify-center px-6">
      <div className="max-w-4xl text-center space-y-12">

        <div className="space-y-1">
          <h1 className="text-3xl font-bold text-slate-900">
            financial_ia
          </h1>

          <p className="text-base text-slate-500">
            Diagnóstico Essencial
          </p>
        </div>

        <div className="space-y-5">
          <h2 className="text-5xl font-bold text-slate-900 leading-tight">
            Descubra sua saúde financeira em poucos minutos
          </h2>

          <p className="text-lg text-slate-600 max-w-2xl mx-auto">
            Receba um diagnóstico automatizado com score financeiro,
            alertas prioritários e recomendações iniciais.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-5">
          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 hover:shadow-md transition">
            Diagnóstico rápido
          </div>

          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 hover:shadow-md transition">
            Análise objetiva
          </div>

          <div className="bg-white p-6 rounded-xl shadow-sm border border-slate-200 hover:shadow-md transition">
            Resultado imediato
          </div>
        </div>

        <button
          onClick={onStart}
          className="bg-slate-900 text-white px-10 py-5 rounded-xl text-lg font-medium hover:bg-slate-800 transition"
        >
          Iniciar Diagnóstico
        </button>

        <p className="text-sm text-slate-500">
          Sem complexidade. Resultado em instantes.
        </p>

      </div>
    </div>
  );
}