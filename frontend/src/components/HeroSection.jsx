export default function HeroSection({ onStart }) {
  return (
    <section className="hero card">
      <span className="product-tag">Versão Fundadora</span>

      <h1>Diagnóstico Financeiro Automatizado com Score, Alertas e Projeções Explicáveis.
      </h1>

      <h2>Entenda sua saúde financeira através de indicadores estruturais e análises automatizadas.
      </h2>

      <p>
        O Financial IA analisa informações financeiras informadas manualmente para
        gerar score, classificação de risco, alertas financeiros,
        recomendações iniciais e projeções de evolução.
      </p>

      <button className="primary-link" type="button" onClick={onStart}>
        Testar Diagnóstico
      </button>

      <small className="hero-disclaimer">
        Plataforma em evolução contínua • Uso informativo e educacional.
      </small>
    </section>
  );
}

