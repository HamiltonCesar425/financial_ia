export default function Privacy() {
  return (
    <main className="privacy-page">
      <header className="privacy-hero">
        <span className="product-tag">Privacidade</span>
        <h1>Privacidade e Uso de Dados</h1>
        <p>
          O Financial IA foi desenhado para usar apenas as informações
          necessárias ao diagnóstico financeiro e apresentar os resultados de
          forma clara, informativa e educacional.
        </p>
      </header>

      <section className="privacy-content">
        <article>
          <h2>Informações utilizadas</h2>
          <p>
            A análise considera os dados financeiros informados manualmente,
            como receita, despesas, dívidas e reserva financeira. Essas
            informações são usadas para calcular score, classificação, alertas,
            recomendações e projeções.
          </p>
        </article>

        <article>
          <h2>Histórico local</h2>
          <p>
            Quando disponível, o histórico de análises é usado para exibir
            evolução, variação e tendência financeira. Esse histórico fica salvo
            no navegador utilizado, com o objetivo de melhorar a leitura do seu
            próprio progresso.
          </p>
        </article>

        <article>
          <h2>Finalidade do uso</h2>
          <p>
            Os dados são tratados para gerar uma leitura automatizada da sua
            situação financeira. O resultado não substitui consultoria
            financeira, contábil, jurídica ou qualquer orientação profissional
            personalizada.
          </p>
        </article>

        <article>
          <h2>Limites e responsabilidade</h2>
          <p>
            As recomendações têm caráter informativo. Decisões financeiras devem
            considerar seu contexto completo, riscos pessoais e, quando
            necessário, apoio de profissionais qualificados.
          </p>
        </article>
      </section>

      <aside className="privacy-note">
        <strong>Compromisso de clareza</strong>
        <p>
          A plataforma está em evolução contínua. Mudanças relevantes na forma
          de uso dos dados devem ser refletidas nesta página.
        </p>
      </aside>
    </main>
  )
}
