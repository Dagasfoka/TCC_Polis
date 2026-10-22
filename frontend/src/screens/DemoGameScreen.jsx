import { useEffect, useMemo, useRef, useState } from "react";
import { formatMission } from "../utils/missionUtils.js";
import BrazilMapSvg from "../components/BrazilMapSvg.jsx";
import QUESTION_PREVIEW_BANK from "../data/questionPreviewBank.json";
import VictoryScreen from "./VictoryScreen.jsx";
import PlayerCard from "../components/PlayerCard.jsx";
import QuestionPresentation from "../components/QuestionPresentation.jsx";
import InfluenceDistributionScreen from "./InfluenceDistributionScreen.jsx";
import DiceAnimation from "../components/DiceAnimation.jsx";
import TerritoryActions from "../components/TerritoryActions.jsx";
import GameNotice from "../components/GameNotice.jsx";
import MissionModal from "../components/MissionModal.jsx";
import LastActionResult from "../components/LastActionResult.jsx";

const PARTY_COLORS = {
  PR: "#DA3A3C",
  PA: "#28A3E0",
  PV: "#30C067", 
  PD: "#E0A12A",
  1: "#DA3A3C",
  2: "#E0A12A",
  3: "#28A3E0",
  4: "#30C067",
};

const DEMO_ACTION_RESULT = {
  type: "action_result",
  success: true,
  title: "Mapeamento Voluntário de Obras Ociosas",
  description: "Ampliar a presença do partido por meio de uma política pública.",
  territory_name: "São Paulo",
  territory_id: "SP",
  response: "Construí uma base de dados sobre o desperdício estatal.",
  money_generated: 120,
  influence_generated: 45,
  corruption_generated: 10,
  conquered: true,
  question_was_correct: true,
  old_current_influence: 90,
  new_current_influence: 135,
};

export default function DemoGameScreen({
  onReturnRoom,
  initialMatchId,
  initialPlayerId,
  onMatchNotFound,
  onLeaveRoom,
}) {
  const matchId = String(initialMatchId ?? "");
  const playerId = initialPlayerId ?? "";

  const [connected, setConnected] = useState(false);
  const [matchState, setMatchState] = useState(null);

  const [showMission, setShowMission] = useState(false);
  const [showLargeMission, setShowLargeMission] = useState(false);
  const [selectedTerritory, setSelectedTerritory] = useState(null);
  const [showInitialDistribution, setShowInitialDistribution] = useState(false);
  const [distributionConfirmed, setDistributionConfirmed] = useState(false);
  const [distributionTerritoryId, setDistributionTerritoryId] = useState("");
  const [distributionAmount, setDistributionAmount] = useState(0);
  const [showVictoryScreen, setShowVictoryScreen] = useState(false);
  const [showQuestionPreview, setShowQuestionPreview] = useState(false);
  const [showActionResultDemo, setShowActionResultDemo] = useState(false);
  const [previewQuestion, setPreviewQuestion] = useState(null);
  const [availableActions, setAvailableActions] = useState([]);
  const [actionType, setActionType] = useState(null);

  const [pendingQuestion, setPendingQuestion] = useState(null);
  const [pendingActionInfo, setPendingActionInfo] = useState(null);
  const [gameNotice, setGameNotice] = useState(null);
  const [skipTurnMessage, setSkipTurnMessage] = useState(null);
  const [diceAnimation, setDiceAnimation] = useState(null);
  const [questionFeedback, setQuestionFeedback] = useState(null);
  const [lastActionResult, setLastActionResult] = useState(null);
  const [queuedActionResult, setQueuedActionResult] = useState(null);

  const [pendingDistributions, setPendingDistributions] = useState({});

  const wsRef = useRef(null);
  const winnerAlertShownRef = useRef(false);
  const reconnectTimerRef = useRef(null);
  const gameNoticeTimerRef = useRef(null);
  const skipTurnTimerRef = useRef(null);
  const lastSkippedTurnRef = useRef(null);
  const previousRoundRef = useRef(null);
  const lastActionNoticeRef = useRef(null);
  const lastActionResultSignatureRef = useRef(null);
  const gameNoticeIdRef = useRef(0);
  const localActionPendingRef = useRef(false);
  const lastDiceResultRef = useRef(null);
  const answeredQuestionRef = useRef(null);
  const pendingDiceResultRef = useRef(null);
  const pendingCompletionNoticesRef = useRef([]);
  const receivedInitialStateRef = useRef(false);
  const shouldReconnectRef = useRef(true);
  const isUnmountingRef = useRef(false);

  const players = matchState?.players ?? [];
  const territories = matchState?.territories ?? [];

  const myTerritories = territories.filter(
    (territory) => territory.owner_id === matchState?.your_player_id
  );

  const distributionTerritory =
    myTerritories.find(
        (territory) =>
            String(territory.territory_id) ===
            String(distributionTerritoryId)
    ) ?? myTerritories[0] ?? null;

  useEffect(() => {
      if (myTerritories.length === 0) {
          return;
      }

      const selectedTerritoryExists = myTerritories.some(
          (territory) =>
              String(territory.territory_id) ===
              String(distributionTerritoryId)
      );

      if (!selectedTerritoryExists) {
          setDistributionTerritoryId(
              String(myTerritories[0].territory_id)
          );
      }
  }, [myTerritories, distributionTerritoryId]);

  useEffect(() => {
    if (!diceAnimation?.rolling) return undefined;

    const intervalId = window.setInterval(() => {
      setDiceAnimation((current) => {
        if (!current?.rolling) return current;

        if (current.steps >= 18) {
          return {
            ...current,
            roll: current.finalRoll,
            rolling: false,
          };
        }

        return {
          ...current,
          roll: Math.floor(Math.random() * 20) + 1,
          steps: current.steps + 1,
        };
      });
    }, 65);

    return () => window.clearInterval(intervalId);
  }, [diceAnimation?.rolling]);

  useEffect(() => {
    if (
      !diceAnimation ||
      diceAnimation.rolling ||
      diceAnimation.outcomeVisible
    ) {
      return undefined;
    }

    const timeoutId = window.setTimeout(() => {
      setDiceAnimation((current) =>
        current ? { ...current, outcomeVisible: true } : current
      );
    }, 450);

    return () => window.clearTimeout(timeoutId);
  }, [diceAnimation?.rolling, diceAnimation?.outcomeVisible]);

  useEffect(() => {
    if (!diceAnimation || diceAnimation.rolling) return undefined;

    const timeoutId = window.setTimeout(() => {
      setDiceAnimation(null);

      if (pendingCompletionNoticesRef.current.length > 0) {
        showGameNotices(pendingCompletionNoticesRef.current);
        pendingCompletionNoticesRef.current = [];
      }
    }, 1800);

    return () => window.clearTimeout(timeoutId);
  }, [diceAnimation?.rolling]);

  useEffect(() => {
    if (!questionFeedback) return undefined;

    const timeoutId = window.setTimeout(
      () => closeQuestionFeedback(),
      30000
    );

    return () => window.clearTimeout(timeoutId);
  }, [questionFeedback]);

  useEffect(() => {
    if (!queuedActionResult || diceAnimation || questionFeedback) return;

    setLastActionResult(queuedActionResult.result);
    setQueuedActionResult(null);
  }, [queuedActionResult, diceAnimation, questionFeedback]);

  function showGameNotice(kind, message) {
    showGameNotices([{ kind, message }]);
  }

  function handleSelectDistributionTerritory(territoryId) {
    setDistributionTerritoryId(territoryId);

    setDistributionAmount(
      pendingDistributions[territoryId] ?? 0
    );

    setDistributionConfirmed(false);
  }

  function savePendingDistribution() {
    if (!distributionTerritory) {
      showGameNotice("error", "Selecione um território.");
      return;
    }

    if (
      !Number.isInteger(distributionAmountValue) ||
      distributionAmountValue < 0
    ) {
      showGameNotice(
        "error",
        "Informe uma quantidade inteira e positiva."
      );
      return;
    }

    setPendingDistributions((previous) => {
      const updated = { ...previous };
      const territoryId = String(distributionTerritory.territory_id);

      if (distributionAmountValue === 0) {
        delete updated[territoryId];
      } else {
        updated[territoryId] = distributionAmountValue;
      }

      return updated;
    });

    showGameNotice(
      "success",
      "Distribuição do território salva."
    );
  }

  function removePendingDistribution(territoryId) {
    setPendingDistributions((previous) => {
      const updated = { ...previous };
      delete updated[territoryId];
      return updated;
    });

    if (String(distributionTerritoryId) === String(territoryId)) {
      setDistributionAmount(0);
    }
  }

  function showGameNotices(notices) {
    if (!notices.length) return;

    if (gameNoticeTimerRef.current) {
      clearTimeout(gameNoticeTimerRef.current);
    }

    let noticeIndex = 0;

    const showNextNotice = () => {
      setGameNotice({
        ...notices[noticeIndex],
        id: ++gameNoticeIdRef.current,
      });

      gameNoticeTimerRef.current = setTimeout(() => {
        noticeIndex += 1;

        if (noticeIndex < notices.length) {
          showNextNotice();
        } else {
          setGameNotice(null);
          gameNoticeTimerRef.current = null;
        }
      }, 2200);
    };

    showNextNotice();
  }

  function startDiceAnimation(result) {
    if (!Number.isFinite(Number(result?.roll))) return;

    setDiceAnimation({
      roll: Math.floor(Math.random() * 20) + 1,
      finalRoll: Number(result.roll),
      success: Boolean(result.success),
      threshold: Number(
        result.minimum_roll_to_succeed ?? result.success_chance ?? 0
      ),
      rolling: true,
      outcomeVisible: false,
      steps: 0,
    });
  }

  function closeQuestionFeedback() {
    setQuestionFeedback(null);
    setPendingQuestion(null);
    setPendingActionInfo(null);

    const result = pendingDiceResultRef.current;
    pendingDiceResultRef.current = null;

    if (result) startDiceAnimation(result);
  }

  function notifyActionCompleted(result) {
    if (!["attack_result", "attack_no_question"].includes(result?.type)) {
      return;
    }

    const signature = JSON.stringify(result);

    if (
      receivedInitialStateRef.current &&
      signature !== lastActionNoticeRef.current &&
      localActionPendingRef.current
    ) {
      if (
        Number.isFinite(Number(result.roll)) &&
        lastDiceResultRef.current !== signature
      ) {
        lastDiceResultRef.current = signature;

        const answeredQuestion = answeredQuestionRef.current;

        if (
          answeredQuestion &&
          typeof result.question_was_correct === "boolean"
        ) {
          pendingDiceResultRef.current = result;

          setQuestionFeedback({
            question: answeredQuestion.question,
            selectedAnswer: answeredQuestion.selectedAnswer,
            correctAnswer: result.correct_answer,
          });

          answeredQuestionRef.current = null;
        } else {
          startDiceAnimation(result);
        }
      }

      const threshold = Number(
        result.minimum_roll_to_succeed ?? result.success_chance ?? 0
      );

      const actionSucceeded =
        typeof result.success === "boolean"
          ? result.success
          : Number(result.roll) >= threshold;

      pendingCompletionNoticesRef.current = [
        actionSucceeded
          ? { kind: "success", message: "Ação concluída!" }
          : { kind: "error", message: "Ação fracassada!" },
      ];

      localActionPendingRef.current = false;
    }

    lastActionNoticeRef.current = signature;
  }

  function queueActionResult(result) {
    if (!result || typeof result !== "object") return;

    const signature = JSON.stringify(result);
    if (signature === lastActionResultSignatureRef.current) return;

    lastActionResultSignatureRef.current = signature;
    setQueuedActionResult({ result, signature });
  }

  const currentPlayer = useMemo(() => {
    if (!matchState) {
      return null;
    }

    return (
      players.find(
        (player) =>
          player.player_id === matchState.current_turn_player_id
      ) ?? null
    );
  }, [matchState, players]);

  const me = useMemo(() => {
    if (!matchState) {
      return null;
    }

    return (
      players.find(
        (player) => player.player_id === matchState.your_player_id
      ) ?? null
    );
  }, [matchState, players]);

  const totalPendingInfluence = Object.values(pendingDistributions)
    .reduce((total, amount) => total + Number(amount || 0), 0);

  const currentTerritoryPendingInfluence = Number(
      pendingDistributions[
          String(distributionTerritory?.territory_id ?? "")
      ] ?? 0
  );

  const maxDistributionInfluence = Math.max(
    0,
    Number(me?.match_influence ?? 0)
      - totalPendingInfluence
      + currentTerritoryPendingInfluence
  );

  const distributionAmountValue =
    distributionAmount === ""
      ? 0
      : Math.min(
          maxDistributionInfluence,
          Math.max(0, Number(distributionAmount) || 0)
        );

  const isMyTurn =
    Boolean(matchState) &&
    matchState.status === "running" &&
    matchState.current_turn_player_id === matchState.your_player_id;

  const nextPlayer = useMemo(() => {
    if (players.length === 0 || !matchState?.current_turn_player_id) {
      return null;
    }

    const currentIndex = players.findIndex(
      (player) =>
        player.player_id === matchState.current_turn_player_id
    );

    if (currentIndex === -1) {
      return null;
    }

    return players[(currentIndex + 1) % players.length] ?? null;
  }, [players, matchState?.current_turn_player_id]);

  const playerPositions = useMemo(() => {
    // Os cards ficam sempre nas mesmas posições.
    // A troca de turno altera apenas o destaque e o rótulo "Próximo".
    return players.slice(0, 4);
  }, [players]);

  const victoryRanking = useMemo(() => {
    const rankedPlayers = players.map((player) => ({
      ...player,
      controlledTerritories: territories.filter(
        (territory) => territory.owner_id === player.player_id
      ).length,
    }));

    const winnerId = matchState?.winner_id;

    return rankedPlayers.sort((a, b) => {
      if (winnerId && a.player_id === winnerId) return -1;
      if (winnerId && b.player_id === winnerId) return 1;

      return (
        b.controlledTerritories - a.controlledTerritories ||
        (b.match_money ?? 0) - (a.match_money ?? 0) ||
        (b.match_influence ?? 0) - (a.match_influence ?? 0)
      );
    });
  }, [players, territories, matchState?.winner_id]);

  function handleWinnerAlert(newMatchState) {
    if (
      newMatchState?.status === "finished" &&
      newMatchState?.winner_id &&
      !winnerAlertShownRef.current
    ) {
      winnerAlertShownRef.current = true;
      setShowVictoryScreen(true);
    }
  }

  function connect() {
    if (!matchId || !playerId) {
      console.error("matchId ou playerId não disponíveis.");
      return;
    }

    // Não cria outra conexão se já existir uma ativa.
    if (
      wsRef.current &&
      (
        wsRef.current.readyState === WebSocket.OPEN ||
        wsRef.current.readyState === WebSocket.CONNECTING
      )
    ) {
      return;
    }

    const WS =
      import.meta.env.VITE_WS_URL ||
      "wss://tcc-polis-42o9.onrender.com";

    console.log(
      `Conectando na partida ${matchId} como ${playerId}...`
    );

    const ws = new WebSocket(
      `${WS}/ws/match/${matchId}/${playerId}`
    );

    wsRef.current = ws;

    ws.onopen = () => {
  // Ignora conexões antigas
  if (wsRef.current !== ws) {
    ws.close();
    return;
  }

  console.log("WebSocket conectado.");

  setConnected(true);

  if (reconnectTimerRef.current) {
    clearTimeout(reconnectTimerRef.current);
    reconnectTimerRef.current = null;
  }
};

    ws.onmessage = (event) => {
      if (wsRef.current !== ws) {
    return;
  }

  let data;

  try {
    data = JSON.parse(event.data);
  } catch (error) {
    console.error(
      "Erro ao interpretar mensagem WebSocket:",
      error
    );

    return;
  }

      try {
        data = JSON.parse(event.data);
      } catch (error) {
        console.error(
          "Erro ao interpretar mensagem WebSocket:",
          error
        );

        return;
      }

      console.log("Evento recebido:", data);

      if (data.type === "territory_selected") {
        console.log("Território selecionado:", data.payload);

        setSelectedTerritory(data.payload.territory);
        setAvailableActions(data.payload.available_actions);
        setActionType(data.payload.action_type);

        return;
      }

      if (data.type === "attack_question") {
        setPendingQuestion(data.question);

        setPendingActionInfo({
          target_territory_id: data.target_territory_id,
          territory_id: data.territory_id,
          territory_name: data.territory_name,
          option_id: data.option_id,
          title: data.title,
          success_chance: data.success_chance,
        });

        return;
      }

      if (data.type === "match_state") {
        const newMatchState = data.payload;
        if (newMatchState?.must_distribute === false) {
            setShowInitialDistribution(false);
            setDistributionConfirmed(true);
            setPendingDistributions({});
            setDistributionAmount(0);
            setDistributionTerritoryId("");
        }
        const newRound = newMatchState?.round;

        if (newRound != null) {
          if (
            previousRoundRef.current !== null &&
            newRound > previousRoundRef.current
          ) {
            showGameNotice(
              "success",
              "Nova rodada! O dinheiro foi distribuído aos jogadores."
            );
          }

          previousRoundRef.current = newRound;
        }

        const actionResult = newMatchState?.last_action_result;
        const skippedPlayerId =
          newMatchState?.skipped_player_id ?? null;

        if (!skippedPlayerId || !receivedInitialStateRef.current) {
          lastSkippedTurnRef.current = null;
        } else {
          const skippedTurnKey =
            `${skippedPlayerId}:${newMatchState?.current_turn_player_id ?? ""}`;

          if (lastSkippedTurnRef.current !== skippedTurnKey) {
            lastSkippedTurnRef.current = skippedTurnKey;

            const skippedPlayer = newMatchState.players?.find(
              (player) => player.player_id === skippedPlayerId
            );

            setSkipTurnMessage(
              `${skippedPlayer?.username ?? "O jogador"} não possui dinheiro suficiente. A vez foi pulada.`
            );

            if (skipTurnTimerRef.current) {
              clearTimeout(skipTurnTimerRef.current);
            }

            skipTurnTimerRef.current = setTimeout(() => {
              setSkipTurnMessage(null);
              skipTurnTimerRef.current = null;
            }, 5000);
          }
        }

        if (receivedInitialStateRef.current) {
          notifyActionCompleted(actionResult);
          queueActionResult(actionResult);
        } else {
          if (actionResult) {
            lastActionResultSignatureRef.current = JSON.stringify(actionResult);
          }
          if (["attack_result", "attack_no_question"].includes(actionResult?.type)) {
            lastActionNoticeRef.current = JSON.stringify(actionResult);
          }
        }

        receivedInitialStateRef.current = true;
        setMatchState(newMatchState);

        handleWinnerAlert(newMatchState);

        return;
      }

      if (data.result?.type === "attack_result") {
        const newMatchState = data.match;

        notifyActionCompleted(data.result);
        queueActionResult(data.result);
        setMatchState(newMatchState);
        handleWinnerAlert(newMatchState);

        return;
      }

      if (data.match && data.result) {
        const newMatchState = data.match;

        notifyActionCompleted(data.result);
        queueActionResult(data.result);
        setMatchState(newMatchState);
        if (
          !["attack_result", "attack_no_question"].includes(data.result?.type)
        ) {
          setPendingQuestion(null);
          setPendingActionInfo(null);
        }

        handleWinnerAlert(newMatchState);

        return;
      }

      if (data.type === "error") {
        const message =
          data.payload?.message ??
          data.message ??
          "Erro desconhecido.";

        console.error("Erro recebido do servidor:", message);

        const normalizedMessage = message.toLowerCase();

        if (
          (normalizedMessage.includes("partida") &&
            normalizedMessage.includes("encontrada")) ||
          normalizedMessage.includes("match not found")
        ) {
          onMatchNotFound?.(message);
          return;
        }

        if (normalizedMessage.includes("fronteira")) {
          localActionPendingRef.current = false;
          setSelectedTerritory(null);
          setAvailableActions([]);
          return;
        }

        const isTechnicalError =
          normalizedMessage.includes("not supported between instances") ||
          normalizedMessage.includes("nonetype") ||
          normalizedMessage.includes("traceback");

        showGameNotice(
          "error",
          isTechnicalError
            ? "Não foi possível concluir a ação. Tente novamente."
            : message
        );

        localActionPendingRef.current = false;

        return;
      }
    };

    ws.onerror = (error) => {
      console.error("Erro no WebSocket:", error);

      // Deixamos o navegador disparar onclose caso a conexão caia.
    };

  ws.onclose = (event) => {
  console.log(
    "WebSocket fechado:",
    event.code,
    event.reason
  );

  // Não permite que conexões antigas afetem a atual
  if (wsRef.current !== ws) {
    return;
  }

  wsRef.current = null;
  setConnected(false);

  if (
    shouldReconnectRef.current &&
    !isUnmountingRef.current
  ) {
    console.log("Tentando reconectar em 2 segundos...");

    if (reconnectTimerRef.current) {
      clearTimeout(reconnectTimerRef.current);
    }

    reconnectTimerRef.current = setTimeout(() => {
      reconnectTimerRef.current = null;
      connect();
    }, 2000);
  }
};
  }

  function handleTerritorySelection(territory) {
    setSelectedTerritory(territory);

    if (
      !wsRef.current ||
      wsRef.current.readyState !== WebSocket.OPEN
    ) {
      return;
    }

    wsRef.current.send(
      JSON.stringify({
        type: "select_territory",
        territory_id: territory.territory_id,
        payload: {
          territory_id: territory.territory_id,
        },
      })
    );
  }

  function sendAttack(optionId, action_type) {
    console.log("ACTION ID:", optionId);

    if (
      !wsRef.current ||
      wsRef.current.readyState !== WebSocket.OPEN
    ) {
      alert("WebSocket não está conectado.");
      return;
    }

    if (!selectedTerritory) {
      alert("Selecione um território no mapa.");
      return;
    }

    localActionPendingRef.current = true;
    lastDiceResultRef.current = null;
    answeredQuestionRef.current = null;
    pendingDiceResultRef.current = null;
    pendingCompletionNoticesRef.current = [];

    wsRef.current.send(
      JSON.stringify({
        type: "choose_attack_option",
        target_territory_id: selectedTerritory.territory_id,
        territory_id: selectedTerritory.territory_id,
        action_id: optionId,
        action_type,
        payload: {
          target_territory_id: selectedTerritory.territory_id,
          territory_id: selectedTerritory.territory_id,
          action_id: optionId,
          action_type,
        },
      })
    );

    setSelectedTerritory(null);
  }

  function answerAttackQuestion(answer) {
    if (
      !wsRef.current ||
      wsRef.current.readyState !== WebSocket.OPEN
    ) {
      alert("WebSocket não está conectado.");
      return;
    }

    answeredQuestionRef.current = {
      question: pendingQuestion,
      selectedAnswer: answer,
    };

    wsRef.current.send(
      JSON.stringify({
        type: "answer_attack_question",
        answer,
        payload: {
          answer,
        },
      })
    );
  }

  function sendInfluenceDistribution() {
    if (
      !wsRef.current ||
      wsRef.current.readyState !== WebSocket.OPEN
    ) {
      showGameNotice("error", "Sem conexão com a partida.");
      return;
    }

    const distributions = Object.entries(pendingDistributions)
      .filter(([, amount]) => Number(amount) > 0)
      .map(([territoryId, amount]) => {
        const territory = myTerritories.find(
          (item) =>
            String(item.territory_id) === String(territoryId)
        );

        return {
          territory_id: territory?.territory_id ?? territoryId,
          distributed_influence: Number(amount),
        };
      });

    if (distributions.length === 0) {
      showGameNotice(
        "error",
        "Salve a distribuição de pelo menos um território."
      );
      return;
    }

    if (
      distributions.some(
        (distribution) =>
          !Number.isInteger(distribution.distributed_influence) ||
          distribution.distributed_influence <= 0
      )
    ) {
      showGameNotice(
        "error",
        "Todas as quantidades devem ser inteiros positivos."
      );
      return;
    }

    const totalDistributed = distributions.reduce(
      (total, distribution) =>
        total + distribution.distributed_influence,
      0
    );

    const availableInfluence = Number(me?.match_influence ?? 0);

    if (totalDistributed > availableInfluence) {
      showGameNotice(
        "error",
        "A distribuição ultrapassa sua influência disponível."
      );
      return;
    }

    if (totalDistributed !== availableInfluence) {
        showGameNotice(
            "error",
            `Você precisa distribuir toda a influência disponível. Faltam ${
                availableInfluence - totalDistributed
            } pontos para distribuir.`
        );
        return;
    }

    wsRef.current.send(
      JSON.stringify({
        type: "distribute_influence",
        payload: {
          distributions,
        },
      })
    );
  }

  useEffect(() => {
    if (!matchId || !playerId) {
      return;
    }

    isUnmountingRef.current = false;
    shouldReconnectRef.current = true;

    connect();

    return () => {
      isUnmountingRef.current = true;
      shouldReconnectRef.current = false;

      if (reconnectTimerRef.current) {
        clearTimeout(reconnectTimerRef.current);
        reconnectTimerRef.current = null;
      }

      if (gameNoticeTimerRef.current) {
        clearTimeout(gameNoticeTimerRef.current);
        gameNoticeTimerRef.current = null;
      }

      if (skipTurnTimerRef.current) {
        clearTimeout(skipTurnTimerRef.current);
        skipTurnTimerRef.current = null;
      }

      if (wsRef.current) {
        wsRef.current.close();
        wsRef.current = null;
      }
    };
  }, [matchId, playerId]);

  const missionText = formatMission(
    matchState?.your_mission,
    players
  );

  const isMissionReveal =
    matchState?.status === "running" &&
    matchState?.phase === "mission_reveal";

  const demoActionResult = {
    ...DEMO_ACTION_RESULT,
    old_owner_id: players[1]?.player_id ?? players[0]?.player_id,
    new_owner_id: players[0]?.player_id,
  };

  return (
    <div
      className={`polis-game-page${
        showVictoryScreen ? " polis-victory-opened" : ""
      }`}
    >
      {matchState?.status === "running" && matchState?.your_mission && !isMissionReveal && (
        <button
          type="button"
          className="polis-victory-open polis-mission-preview-open"
          onClick={() => setShowLargeMission(true)}
        >
          <span aria-hidden="true">📜</span>
          Missão grande
        </button>
      )}

      {matchState?.status === "running" && (isMissionReveal || showMission || matchState?.your_mission) && (
        <MissionModal
          mission={matchState?.your_mission}
          players={players}
          endsAt={
            isMissionReveal
              ? matchState?.mission_reveal_ends_at
              : null
          }
          isOpen={showMission && !isMissionReveal}
          isRevealing={isMissionReveal}
          showLargeMission={showLargeMission}
          onOpen={() => setShowMission(true)}
          onClose={() => setShowMission(false)}
          onCloseLarge={() => setShowLargeMission(false)}
        />
      )}

      {skipTurnMessage && (
        <div
          className="polis-skip-turn-message"
          role="status"
          aria-live="polite"
        >
          {skipTurnMessage}
        </div>
      )}

      {!showVictoryScreen && (
        <button
          type="button"
          className="polis-victory-open"
          onClick={() => setShowVictoryScreen(true)}
          aria-label="Abrir tela de vitória"
        >
          <img src="/coroa.png" alt="" />
          Vitória
        </button>
      )}

      {!showInitialDistribution && !showVictoryScreen && (
        <button
          type="button"
          className="polis-victory-open polis-distribution-open"
          onClick={() => {
            setDistributionConfirmed(false);
            setShowInitialDistribution(true);
          }}
          aria-label="Abrir distribuição"
        >
          <span
            className="polis-distribution-open-icon"
            aria-hidden="true"
          >
            +
          </span>
          Distribuição
        </button>
      )}

      {!showVictoryScreen && !showQuestionPreview && (
        <button
          type="button"
          className="polis-victory-open polis-question-preview-open"
          onClick={() => {
            const randomIndex = Math.floor(
              Math.random() * QUESTION_PREVIEW_BANK.length
            );

            setPreviewQuestion(QUESTION_PREVIEW_BANK[randomIndex]);
            setShowQuestionPreview(true);
          }}
          aria-label="Abrir tela demonstrativa de pergunta"
        >
          <span
            className="polis-question-preview-icon"
            aria-hidden="true"
          >
            ?
          </span>
          Pergunta
        </button>
      )}

      {!showVictoryScreen && !showQuestionPreview && (
        <button
          type="button"
          className="polis-victory-open polis-action-result-preview-open"
          onClick={() => setShowActionResultDemo(true)}
          aria-label="Abrir tela demonstrativa de resultado da ação"
        >
          <span aria-hidden="true">✓</span>
          Resultado (demo)
        </button>
      )}

      <main className="polis-game-screen">
        <div className="polis-turn-title">
          Vez de{" "}
          <span
            style={{
              color:
                PARTY_COLORS[currentPlayer?.party_id] ?? "#ffffff",
            }}
          >
            {currentPlayer?.username ?? "..."}
          </span>
        </div>

        <div className="polis-position polis-position-top-left">
          <PlayerCard
            player={playerPositions[0]}
            isCurrentTurn={
              playerPositions[0]?.player_id ===
              matchState?.current_turn_player_id
            }
            isNext={
              playerPositions[0]?.player_id ===
              nextPlayer?.player_id
            }
            isMe={
              playerPositions[0]?.player_id ===
              matchState?.your_player_id
            }
            partyColors={PARTY_COLORS}
            territories={territories}
            side="left"
          />
        </div>

        <div className="polis-position polis-position-top-right">
          <PlayerCard
            player={playerPositions[1]}
            isCurrentTurn={
              playerPositions[1]?.player_id ===
              matchState?.current_turn_player_id
            }
            isNext={
              playerPositions[1]?.player_id ===
              nextPlayer?.player_id
            }
            isMe={
              playerPositions[1]?.player_id ===
              matchState?.your_player_id
            }
            partyColors={PARTY_COLORS}
            territories={territories}
            side="right"
          />
        </div>

        <div className="polis-position polis-position-bottom-left">
          <PlayerCard
            player={playerPositions[2]}
            isCurrentTurn={
              playerPositions[2]?.player_id ===
              matchState?.current_turn_player_id
            }
            isNext={
              playerPositions[2]?.player_id ===
              nextPlayer?.player_id
            }
            isMe={
              playerPositions[2]?.player_id ===
              matchState?.your_player_id
            }
            partyColors={PARTY_COLORS}
            territories={territories}
            side="left"
          />
        </div>

        <div className="polis-position polis-position-bottom-right">
          <PlayerCard
            player={playerPositions[3]}
            isCurrentTurn={
              playerPositions[3]?.player_id ===
              matchState?.current_turn_player_id
            }
            isNext={
              playerPositions[3]?.player_id ===
              nextPlayer?.player_id
            }
            isMe={
              playerPositions[3]?.player_id ===
              matchState?.your_player_id
            }
            partyColors={PARTY_COLORS}
            territories={territories}
            side="right"
          />
        </div>

        <section className="polis-map-container">
          <img
            className="polis-america-backdrop"
            src="/AMERICA.png"
            alt=""
            aria-hidden="true"
          />

          <BrazilMapSvg
            territories={territories}
            players={players}
            partyColors={PARTY_COLORS}
            currentPlayerId={matchState?.your_player_id}
            selectedTerritoryId={selectedTerritory?.territory_id}
            isActionable={isMyTurn}
            onSelectTerritory={handleTerritorySelection}
            className="polis-main-map"
          />
        </section>

        {selectedTerritory && (
          <TerritoryActions
            selectedTerritory={selectedTerritory}
            isMyTurn={isMyTurn}
            availableActions={availableActions}
            onChooseAction={sendAttack}
            onClose={() => setSelectedTerritory(null)}
          />
        )}

        {pendingQuestion && (
          <QuestionPresentation
            question={pendingQuestion}
            targetName={pendingActionInfo?.territory_name}
            onAnswer={answerAttackQuestion}
            feedback={questionFeedback}
            onDismiss={
              questionFeedback ? closeQuestionFeedback : undefined
            }
          />
        )}

        {showQuestionPreview && (
          <QuestionPresentation
            key={previewQuestion?.question_id}
            question={previewQuestion}
            targetName="São Paulo"
            isDemo
            onAnswer={() => {}}
            onDismiss={() => setShowQuestionPreview(false)}
          />
        )}

        {(matchState?.must_distribute || showInitialDistribution) && (
          <InfluenceDistributionScreen
            matchState={matchState}
            territories={territories}
            players={players}
            me={me}
            partyColors={PARTY_COLORS}
            myTerritories={myTerritories}
            distributionTerritory={distributionTerritory}
            distributionAmount={distributionAmount}
            setDistributionAmount={setDistributionAmount}
            distributionAmountValue={distributionAmountValue}
            maxDistributionInfluence={maxDistributionInfluence}
            pendingDistributions={pendingDistributions}
            onSelectTerritory={handleSelectDistributionTerritory}
            onSaveDistribution={savePendingDistribution}
            onRemoveDistribution={removePendingDistribution}
            onConfirm={sendInfluenceDistribution}
          />
        )}

        {!connected && (
          <div className="polis-connection-warning">
            Conectando à partida...
          </div>
        )}

        <GameNotice notice={gameNotice} />
        <LastActionResult
          result={showActionResultDemo ? demoActionResult : lastActionResult}
          players={players}
          partyColors={PARTY_COLORS}
          onClose={() => {
            if (showActionResultDemo) {
              setShowActionResultDemo(false);
            } else {
              setLastActionResult(null);
            }
          }}
        />

        {showVictoryScreen && (
          <VictoryScreen
            victoryRanking={victoryRanking}
            matchState={matchState}
            players={players}
            formatMission={formatMission}
            partyColors={PARTY_COLORS}
            onReturnRoom={onReturnRoom}
            onLeaveRoom={onLeaveRoom}
          />
        )}
      </main>

      <DiceAnimation diceAnimation={diceAnimation} />

    </div>
  );
}
