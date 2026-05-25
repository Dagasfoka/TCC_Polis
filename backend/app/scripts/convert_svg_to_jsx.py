import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

SVG_PATH = PROJECT_ROOT / "static" / "Estados.svg"
OUTPUT_PATH = (
    PROJECT_ROOT
    / "static"
    / "BrazilMapSvg.jsx"
)

TERRITORY_IDS = {
    "AC", "AM", "PA", "RO", "TO",
    "AL", "BA", "CE", "MA", "PE", "PI",
    "DF", "GO", "MT", "MS",
    "MG", "RJ", "SP",
    "PR", "SC",
}

REGION_COLORS = """
const REGION_COLORS = {
  Norte: "#6dba8a",
  Nordeste: "#f0a090",
  "Centro-Oeste": "#9fcfdb",
  Sudeste: "#f0a080",
  Sul: "#a0b0e0",
};
"""

def convert_svg_attrs(svg: str) -> str:
    svg = svg.replace("fill-rule", "fillRule")
    svg = svg.replace("clip-rule", "clipRule")
    svg = svg.replace("stroke-width", "strokeWidth")
    svg = svg.replace("stroke-linecap", "strokeLinecap")
    svg = svg.replace("stroke-linejoin", "strokeLinejoin")
    svg = svg.replace("class=", "className=")

    # Corrige possível id errado do Rio Grande/Rio de Janeiro se seu SVG tiver RG
    svg = svg.replace('id="RG"', 'id="RJ"')

    return svg


def enhance_path(match: re.Match) -> str:
    tag = match.group(0)
    territory_id_match = re.search(r'id="([^"]+)"', tag)

    if not territory_id_match:
        return tag

    territory_id = territory_id_match.group(1)

    if territory_id not in TERRITORY_IDS:
        return tag

    # Remove fill fixo para React controlar
    tag = re.sub(r'\sfill="[^"]*"', "", tag)

    # Remove stroke fixo se quiser React controlar
    tag = re.sub(r'\sstroke="[^"]*"', "", tag)
    tag = re.sub(r'\sstrokeWidth="[^"]*"', "", tag)

    insert = f'''
      fill={{getFill("{territory_id}")}}
      stroke={{getStroke("{territory_id}")}}
      strokeWidth={{selectedTerritoryId === "{territory_id}" ? 2.5 : 1}}
      className="polis-territory"
      style={{{{ cursor: "pointer", transition: "fill 0.15s ease, stroke 0.15s ease" }}}}
      onClick={{() => handleTerritoryClick("{territory_id}")}}
      onKeyDown={{(event) => handleTerritoryKeyDown(event, "{territory_id}")}}
      tabIndex={{0}}
      role="button"
      aria-label={{getAriaLabel("{territory_id}")}}'''

    # Insere depois de <path
    tag = tag.replace("<path", "<path" + insert, 1)

    return tag


def main() -> None:
    svg = SVG_PATH.read_text(encoding="utf-8")
    svg = convert_svg_attrs(svg)

    # Remove XML/header se houver
    svg = re.sub(r"<\?xml.*?\?>", "", svg, flags=re.DOTALL)
    svg = re.sub(r"<!DOCTYPE.*?>", "", svg, flags=re.DOTALL)

    # Adiciona props no <svg>
    svg = re.sub(
        r"<svg([^>]*)>",
        r'<svg\1 className={className} role="img" aria-label="Mapa do Brasil do Polis">',
        svg,
        count=1,
    )

    # Melhora só paths com id de território
    svg = re.sub(r"<path\b[^>]*\/?>", enhance_path, svg)

    component = f'''import {{ useMemo }} from "react";

{REGION_COLORS}

const PLAYER_COLORS = ["#c9963a", "#d07060", "#6dba8a", "#9fcfdb"];

function normalizeOwnerId(ownerId) {{
  if (ownerId === null || ownerId === undefined) return null;

  const numericOwnerId = Number(ownerId);

  if (Number.isNaN(numericOwnerId)) return null;

  return numericOwnerId;
}}

export default function BrazilMapSvg({{
  territories = [],
  selectedTerritoryId = null,
  onSelectTerritory = () => {{}},
  className = "",
}}) {{
  const territoryById = useMemo(() => {{
    return Object.fromEntries(
      territories.map((territory) => [territory.territory_id, territory])
    );
  }}, [territories]);

  function getFill(territoryId) {{
    const territory = territoryById[territoryId];

    if (!territory) return "#2a2624";
    if (selectedTerritoryId === territoryId) return "#e8c070";

    const ownerId = normalizeOwnerId(territory.owner_id);

    if (ownerId !== null) {{
      return PLAYER_COLORS[ownerId % PLAYER_COLORS.length];
    }}

    return REGION_COLORS[territory.region] ?? "#c9963a";
  }}

  function getStroke(territoryId) {{
    if (selectedTerritoryId === territoryId) return "#ffffff";
    return "#1a1816";
  }}

  function getAriaLabel(territoryId) {{
    const territory = territoryById[territoryId];

    if (!territory) return `Território ${{territoryId}}`;

    return `${{territory.name}}, influência ${{territory.current_influence}}`;
  }}

  function handleTerritoryClick(territoryId) {{
    const territory = territoryById[territoryId];

    if (!territory) return;

    onSelectTerritory(territory);
  }}

  function handleTerritoryKeyDown(event, territoryId) {{
    if (event.key !== "Enter" && event.key !== " ") return;

    event.preventDefault();
    handleTerritoryClick(territoryId);
  }}

  return (
    {svg}
  );
}}
'''

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(component, encoding="utf-8")

    print(f"Componente criado em: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()