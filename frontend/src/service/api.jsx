
const API_URL = (
  import.meta.env.VITE_API_URL ||
  "https://tcc-polis-42o9.onrender.com"
).replace(/\/$/, "");

// Função central para fazer requisições ao FastAPI.
async function request(path, options = {}) {
  let response;

  try {
    response = await fetch(`${API_URL}${path}`, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });
  } catch (error) {
  console.error("ERRO DE CONEXÃO COM O BACKEND:", {
    url: `${API_URL}${path}`,
    metodo: options.method || "GET",
    erro: error,
  });

  throw new Error(
    "Não foi possível conectar ao servidor. Verifique o Console (F12)."
  );
}

  const contentType =
    response.headers.get("content-type") || "";

  const data = contentType.includes("application/json")
    ? await response.json()
    : await response.text();

  if (!response.ok) {
    const detail =
      data && typeof data === "object"
        ? data.detail
        : data;

    const message = Array.isArray(detail)
      ? detail
          .map((item) => item.msg || JSON.stringify(item))
          .join("; ")
      : typeof detail === "string"
        ? detail
        : `Erro HTTP ${response.status}`;

    const error = new Error(
      message || `Erro HTTP ${response.status}`
    );

    error.status = response.status;

    throw error;
  }

  return data;
}

// ==============================
// JOGADORES
// ==============================

// Criar jogador pelo nickname.
export function createPlayer(username) {
  return request("/players", {
    method: "POST",
    body: JSON.stringify({
      username,
    }),
  });
}

// Buscar jogador pelo ID.
export function getPlayer(playerId) {
  return request(
    `/players/${encodeURIComponent(playerId)}`
  );
}

// ==============================
// SALAS
// ==============================

// Buscar informações da sala.
export function getRoom(roomCode) {
  return request(
    `/rooms/${encodeURIComponent(roomCode)}`
  );
}

// Criar sala.
// O backend retorna room_code, então buscamos
// os dados completos da sala em seguida.
export async function createRoom(playerId) {
  const result = await request("/rooms", {
    method: "POST",
    body: JSON.stringify({
      host_id: playerId,
    }),
  });

  return getRoom(result.room_code);
}

// Entrar em uma sala existente.
export async function joinRoom(roomCode, playerId) {
  const code = roomCode.trim();

  const result = await request(
    `/rooms/${encodeURIComponent(code)}/join`,
    {
      method: "POST",
      body: JSON.stringify({
        player_id: playerId,
      }),
    }
  );

  return result?.players
    ? result
    : getRoom(code);
}

// Marcar jogador como pronto.
export function putReady(roomCode, playerId) {
  return request(
    `/rooms/${encodeURIComponent(roomCode)}/ready`,
    {
      method: "POST",
      body: JSON.stringify({
        player_id: playerId,
      }),
    }
  );
}

// Iniciar partida (somente host).
export function startRoom(roomCode, playerId) {
  return request(
    `/rooms/${encodeURIComponent(roomCode)}/start`,
    {
      method: "POST",
      body: JSON.stringify({
        host_id: playerId,
      }),
    }
  );
}

// Expulsar jogador da sala (somente host).
export function deletePlayer(
  roomCode,
  hostId,
  targetId
) {
  return request(
    `/rooms/${encodeURIComponent(roomCode)}/kick`,
    {
      method: "DELETE",
      body: JSON.stringify({
        host_id: hostId,
        target_id: targetId,
      }),
    }
  );
}

// Sair voluntariamente da sala.
export function exitRoom(roomCode, playerId) {
  return request(
    `/rooms/${encodeURIComponent(roomCode)}/exit`,
    {
      method: "DELETE",
      body: JSON.stringify({
        player_id: playerId,
      }),
    }
  );
}