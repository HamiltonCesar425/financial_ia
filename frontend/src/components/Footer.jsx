import { Link } from "react-router-dom";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-main">
        <div>
          <h3>Financial IA</h3>
          <p>Diagnóstico financeiro automatizado para decisões mais conscientes.</p>
        </div>

        <nav>
          <a href="/privacy">Privacidade</a>
          <a href="/feedback">Feedback</a>
          <a href="/contact">Contato</a>
        </nav>
      </div>

      <div className="footer-meta">
        <small>Financial IA • Uso informativo e educacional.</small>
        <small>Plataforma em evolução contínua.</small>
      </div>

      <Link to="/privacy">Privacidade</Link>

    </footer>
  )
}
