import { useEffect, useState } from "react";

const TUTORIAL_PAGES = [
  {
    chapter: "O começo da disputa",
    title: "Sua missão é secreta",
    paragraphs: [
      "Cada jogador recebe um objetivo próprio. Leia sua carta com atenção: ela pode pedir que você controle determinados estados, conquiste territórios de uma região ou elimine um rival.",
      "No início, a carta fica aberta por 15 segundos. Aproveite para memorizar a missão e mantenha seu objetivo em segredo durante a partida.",
    ],
    note: "Vence quem cumprir a própria missão primeiro.",
  },
  {
    chapter: "Preparação",
    title: "Distribua sua influência",
    paragraphs: [
      "Antes das jogadas, seus pontos de influência precisam ser distribuídos pelos territórios que você controla. Selecione um estado no mapa, ajuste a quantidade e salve a distribuição.",
      "Você pode dividir os pontos entre vários estados. Quando tiver usado todos, confirme para concluir esta etapa e entrar na disputa.",
    ],
    note: "A tela mostra quanto ainda falta distribuir.",
  },
  {
    chapter: "Sua vez",
    title: "Escolha um território e uma ação",
    paragraphs: [
      "Quando chegar sua vez, escolha um território no mapa. O painel apresenta as ações disponíveis para aquele estado, com seus riscos, custos e possíveis efeitos.",
      "Compare as opções antes de decidir: uma ação pode aumentar sua influência ou dinheiro, alterar o controle de um território e também trazer consequências.",
    ],
    note: "A indicação “Vez de” mostra quem pode agir agora.",
  },
  {
    chapter: "Perguntas e resultados",
    title: "Conhecimento também conta",
    paragraphs: [
      "Algumas ações apresentam uma pergunta de múltipla escolha. Responda dentro do tempo exibido. Uma resposta correta aumenta em 20% a chance de sucesso da ação.",
      "Depois, o dado é comparado à dificuldade (CD). O resultado mostra se a ação funcionou e como mudaram os recursos ou o controle do território.",
    ],
    note: "A pergunta tem limite de 30 segundos.",
  },
  {
    chapter: "Leia o tabuleiro",
    title: "Acompanhe a disputa",
    paragraphs: [
      "As cartas ao redor do mapa resumem a situação dos jogadores: dinheiro, corrupção e quantidade de estados controlados. O destaque de turno ajuda a acompanhar a ordem das jogadas.",
      "Observe as mudanças depois de cada ação. Um rival pode estar perto de cumprir a missão — às vezes, defender um território é tão importante quanto avançar.",
    ],
    note: "Selecione os estados no mapa para ver suas opções.",
  },
  {
    chapter: "Rumo à vitória",
    title: "Jogue pensando no objetivo",
    paragraphs: [
      "Missões de controle exigem manter os estados indicados; missões regionais pedem uma quantidade de territórios numa região; missões de destruição dependem de tirar um jogador do mapa.",
      "Use suas ações para aproximar-se da sua condição de vitória e fique de olho nos adversários. Quando alguém cumpre o objetivo, a partida termina e o vencedor é revelado.",
    ],
    note: "Sua missão continua sendo só sua: planeje sem revelá-la.",
  },
];

export default function TutorialBook({ onClose }) {
  const [pageIndex, setPageIndex] = useState(0);
  const page = TUTORIAL_PAGES[pageIndex];

  useEffect(() => {
    function handleKeyDown(event) {
      if (event.key === "Escape") onClose();
      if (event.key === "ArrowRight") {
        setPageIndex((current) => Math.min(TUTORIAL_PAGES.length - 1, current + 1));
      }
      if (event.key === "ArrowLeft") {
        setPageIndex((current) => Math.max(0, current - 1));
      }
    }

    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [onClose]);

  return (
    <div className="polis-tutorial-overlay" role="dialog" aria-modal="true" aria-label="Tutorial: como jogar Polis">
      <section className="polis-tutorial-book">
        <button type="button" className="polis-tutorial-close" onClick={onClose} aria-label="Fechar tutorial" title="Fechar">
          ×
        </button>

        <header className="polis-tutorial-header">
          <span className="polis-tutorial-kicker">GUIA DO JOGADOR</span>
          <h1>Como jogar Polis</h1>
          <p>Um guia rápido para entrar na disputa.</p>
        </header>

        <article className="polis-tutorial-page" key={pageIndex}>
          <div className="polis-tutorial-page-top">
            <span className="polis-tutorial-chapter">{page.chapter}</span>
          </div>
          <h2>{page.title}</h2>
          {page.paragraphs.map((paragraph) => <p key={paragraph}>{paragraph}</p>)}
          <aside className="polis-tutorial-note">{page.note}</aside>
        </article>

        <footer className="polis-tutorial-footer">
          <button
            type="button"
            className="polis-tutorial-nav"
            onClick={() => setPageIndex((current) => Math.max(0, current - 1))}
            disabled={pageIndex === 0}
          >
            ← Anterior
          </button>
          <span className="polis-tutorial-page-count">{pageIndex + 1} / {TUTORIAL_PAGES.length}</span>
          {pageIndex < TUTORIAL_PAGES.length - 1 ? (
            <button
              type="button"
              className="polis-tutorial-nav is-next"
              onClick={() => setPageIndex((current) => Math.min(TUTORIAL_PAGES.length - 1, current + 1))}
            >
              Próxima →
            </button>
          ) : (
            <button type="button" className="polis-tutorial-nav is-next" onClick={onClose}>
              Vamos jogar ✦
            </button>
          )}
        </footer>
      </section>
    </div>
  );
}
