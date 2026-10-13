import { useMemo } from "react";
import { TERRITORY_PATHS } from "./brazilTerritoryPaths.js";

const REGION_COLORS = {
  Norte: "#6dba8a",
  Nordeste: "#f0a090",
  "Centro-Oeste": "#9fcfdb",
  Sudeste: "#f0a080",
  Sul: "#a0b0e0",
};

const DEFAULT_PARTY_COLORS = {
  PR: "#DA3A3C",
  PA: "#28A3E0",
  PV: "#30C067",
  PD: "#E0A12A",
};

const LABEL_POSITIONS = {
  AC: { x: 67.3, y: 279.6 }, RO: { x: 209.2, y: 310.2 }, AM: { x: 182.2, y: 166.7 },
  PA: { x: 393.9, y: 167.1 }, MA: { x: 537.1, y: 198.6 }, PI: { x: 580.2, y: 243 },
  CE: { x: 657.4, y: 203.3 }, PE: { x: 680.5, y: 252.5 }, AL: { x: 691.8, y: 292.5 },
  BA: { x: 603.5, y: 340 }, TO: { x: 480.1, y: 295.7 }, MT: { x: 338.6, y: 349 },
  GO: { x: 456, y: 407.9 }, DF: { x: 512, y: 394.3 }, MS: { x: 358.5, y: 489.7 },
  MG: { x: 548.4, y: 454 }, SP: { x: 472.7, y: 526.6 }, RJ: { x: 603.5, y: 500.8 },
  PR: { x: 418.8, y: 571.8 }, SC: { x: 402.7, y: 657.3 },
};

const TERRITORY_IDS = [
  "RO", "AC", "AM", "TO", "MT", "GO", "MS", "MG", "PR", "BA",
  "PI", "AL", "DF", "MA", "PA", "SP", "RJ", "SC", "CE", "PE",
];

const TERRITORY_FRONTIERS = {
  AC: ["AM", "RO", "SC"], AM: ["AC", "RO", "MT", "PA"],
  PA: ["AM", "MT", "TO", "MA"], RO: ["AC", "AM", "MT"],
  TO: ["PA", "MA", "PI", "BA", "GO", "MT"], AL: ["PE", "BA"],
  BA: ["AL", "PE", "PI", "TO", "GO", "MG", "RJ"], CE: ["PI", "PE", "RJ"],
  MA: ["PA", "TO", "PI"], PE: ["CE", "PI", "BA", "AL"],
  PI: ["MA", "CE", "PE", "BA", "TO"], DF: ["GO", "MG"],
  GO: ["TO", "BA", "MG", "MS", "MT", "DF"], MT: ["RO", "AM", "PA", "TO", "GO", "MS"],
  MS: ["MT", "GO", "MG", "SP", "PR"], MG: ["BA", "GO", "DF", "MS", "SP", "RJ"],
  RJ: ["MG", "SP", "BA", "CE"], SP: ["MG", "RJ", "MS", "PR"],
  PR: ["SP", "MS", "SC"], SC: ["PR", "AC"],
};

function darkenColor(color) {
  const hex = color.replace("#", "");
  if (!/^[0-9a-f]{6}$/i.test(hex)) return color;
  const channels = [0, 2, 4].map((index) =>
    Math.round(parseInt(hex.slice(index, index + 2), 16) * 0.35)
  );
  return `#${channels.map((channel) => channel.toString(16).padStart(2, "0")).join("")}`;
}

export default function BrazilMapSvg({
  territories = [],
  players = [],
  partyColors = DEFAULT_PARTY_COLORS,
  selectedTerritoryId = null,
  onSelectTerritory = () => {},
  isActionable = true,
  currentPlayerId = null,
  className = "",
}) {
  const territoryById = useMemo(
    () => Object.fromEntries(territories.map((territory) => [territory.territory_id, territory])),
    [territories]
  );

  function isTerritorySelectable(territoryId) {
    if (!currentPlayerId) return true;

    const territory = territoryById[territoryId];
    if (!territory) return false;
    if (territory.owner_id === currentPlayerId) return true;

    const frontiers = TERRITORY_FRONTIERS[territoryId] ?? [];
    return territories.some(
      (ownedTerritory) =>
        ownedTerritory.owner_id === currentPlayerId &&
        frontiers.includes(ownedTerritory.territory_id)
    );
  }

  function getFill(territoryId) {
    const territory = territoryById[territoryId];
    let fill = "#2a2624";

    if (territory) {
      const owner = players.find((player) => player.player_id === territory.owner_id);
      fill = owner?.party_id
        ? partyColors[owner.party_id] ?? "#c9963a"
        : REGION_COLORS[territory.region] ?? "#c9963a";
    }

    return isActionable && isTerritorySelectable(territoryId)
      ? fill
      : darkenColor(fill);
  }

  function getAriaLabel(territoryId) {
    const territory = territoryById[territoryId];
    if (!territory) return `Território ${territoryId}`;
    return `${territory.name}, influência ${territory.current_influence}`;
  }

  function handleTerritoryClick(territoryId) {
    const territory = territoryById[territoryId];
    if (territory && isTerritorySelectable(territoryId)) {
      onSelectTerritory(territory);
    }
  }

  function handleTerritoryKeyDown(event, territoryId) {
    if (event.key !== "Enter" && event.key !== " ") return;
    event.preventDefault();
    handleTerritoryClick(territoryId);
  }

  return (
    <svg
      width="746"
      height="750"
      viewBox="0 0 746 750"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
      role="img"
      aria-label="Mapa do Brasil do Polis"
    >
      <defs>
        <mask
          id="mask-df-neighbors"
          maskUnits="userSpaceOnUse"
          x="0"
          y="0"
          width="746"
          height="750"
        >
          <rect x="0" y="0" width="746" height="750" fill="#ffffff" />
          <path d={TERRITORY_PATHS.DF} fill="#000000" fillRule="evenodd" />
        </mask>
      </defs>

      {TERRITORY_IDS.map((territoryId) => (
        <path
          key={`fill-${territoryId}`}
          id={territoryId}
          d={TERRITORY_PATHS[territoryId]}
          fill={getFill(territoryId)}
          fillRule="evenodd"
          clipRule="evenodd"
          mask={
            ["GO", "BA", "MG"].includes(territoryId)
              ? "url(#mask-df-neighbors)"
              : undefined
          }
          className="polis-territory"
          style={{
            cursor: isTerritorySelectable(territoryId) ? "pointer" : "not-allowed",
            transition: "fill 0.15s ease",
          }}
          onClick={() => handleTerritoryClick(territoryId)}
          onKeyDown={(event) => handleTerritoryKeyDown(event, territoryId)}
          tabIndex={isTerritorySelectable(territoryId) ? 0 : -1}
          role="button"
          aria-disabled={!isTerritorySelectable(territoryId)}
          aria-label={getAriaLabel(territoryId)}
        />
      ))}

      {TERRITORY_IDS.filter((territoryId) => territoryId !== selectedTerritoryId).map((territoryId) => (
        <path
          key={`border-${territoryId}`}
          d={TERRITORY_PATHS[territoryId]}
          fill="none"
          stroke="#000000"
          strokeWidth="1.4"
          mask={
            ["GO", "BA", "MG"].includes(territoryId)
              ? "url(#mask-df-neighbors)"
              : undefined
          }
          pointerEvents="none"
        />
      ))}

      {selectedTerritoryId && TERRITORY_PATHS[selectedTerritoryId] && (
        <path
          d={TERRITORY_PATHS[selectedTerritoryId]}
          fill="none"
          stroke="#ffffff"
          strokeWidth="1.4"
          mask={
            ["GO", "BA", "MG"].includes(selectedTerritoryId)
              ? "url(#mask-df-neighbors)"
              : undefined
          }
          pointerEvents="none"
        />
      )}

      <g className="polis-territory-labels" aria-hidden="true">
        {TERRITORY_IDS.map((territoryId) => {
          const position = LABEL_POSITIONS[territoryId];
          const territory = territoryById[territoryId];
          if (!position || !territory) return null;
          const x = position.x;
          const y = position.y;
          return (
            <g key={`label-${territoryId}`}>
              <text
                x={x}
                y={y - 6}
                textAnchor="middle"
                dominantBaseline="middle"
                className="polis-territory-label"
                style={{
                  pointerEvents: "none",
                  userSelect: "none",
                  fontSize: "18px",
                  fontWeight: 800,
                  fill: isActionable && isTerritorySelectable(territoryId) ? "#ffffff" : "#808080",
                  stroke: isActionable && isTerritorySelectable(territoryId) ? "#1a1816" : "#111111",
                  strokeWidth: 2.8,
                  paintOrder: "stroke",
                }}
              >
                {territoryId}
              </text>
              <text
                x={x}
                y={y + 9}
                textAnchor="middle"
                dominantBaseline="middle"
                className="polis-territory-label"
                style={{
                  pointerEvents: "none",
                  userSelect: "none",
                  fontSize: "14px",
                  fontWeight: 800,
                  fill: isActionable && isTerritorySelectable(territoryId) ? "#ffffff" : "#808080",
                  stroke: isActionable && isTerritorySelectable(territoryId) ? "#1a1816" : "#111111",
                  strokeWidth: 2.8,
                  paintOrder: "stroke",
                }}
              >
                {territory.current_influence ?? 0}
              </text>
            </g>
          );
        })}
      </g>

      <g className="polis-transport-markers" aria-hidden="true">
        <path
          d="M 34 282 C -8 390 122 654 330 684"
          fill="none"
          stroke="#ffffff"
          strokeWidth="2.5"
          strokeDasharray="8 8"
          strokeLinecap="round"
          pointerEvents="none"
        />
        <path
          d="M 610 535 C 770 470 780 225 700 188"
          fill="none"
          stroke="#ffffff"
          strokeWidth="2.5"
          strokeDasharray="8 8"
          strokeLinecap="round"
          pointerEvents="none"
        />
        <image href="/ONIBUS.png" x="14" y="262" width="40" height="40" pointerEvents="none" />
        <image href="/ONIBUS.png" x="310" y="664" width="40" height="40" pointerEvents="none" />
        <image href="/NAVIO.png" x="590" y="515" width="40" height="40" pointerEvents="none" />
        <image href="/NAVIO.png" x="680" y="168" width="40" height="40" pointerEvents="none" />
      </g>
    </svg>
  );
}
