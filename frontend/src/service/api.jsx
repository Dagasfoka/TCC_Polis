
const API_URL = "http://localhost:8000";

async function request(endpoint, options = {}) {
    const response = await fetch(`${API_URL}${endpoint}`, {
        ...options,
        headers: {
            "Content-Type": "application/json",
            ...options.headers
        }
    });

    const data = await response.json();

    if (!response.ok) {
        throw new Error(
            typeof data.detail === "string"
                ? data.detail
                : "Erro ao comunicar com o servidor."
        );
    }

    return data;
}

// JOGADORES

export function createPlayer(username) {
    return request("/players", {
        method: "POST",
        body: JSON.stringify({ username })
    });
}

export function getPlayer(playerId) {
    return request(`/players/${playerId}`);
}

// SALAS

export function createRoom(hostId) {
    return request("/rooms", {
        method: "POST",
        body: JSON.stringify({
            host_id: hostId
        })
    });
}

export function joinRoom(roomCode, playerId) {
    return request(`/rooms/${roomCode}/join`, {
        method: "POST",
        body: JSON.stringify({
            player_id: playerId
        })
    });
}

export function getRoom(roomCode) {
    return request(`/rooms/${roomCode}`);
}

export function readyPlayer(roomCode, playerId) {
    return request(`/rooms/${roomCode}/ready`, {
        method: "POST",
        body: JSON.stringify({
            player_id: playerId
        })
    });
}

export function kickPlayer(roomCode, hostId, targetId) {
    return request(`/rooms/${roomCode}/delete`, {
        method: "DELETE",
        body: JSON.stringify({
            host_id: hostId,
            target_id: targetId
        })
    });
}

export function startGame(roomCode, hostId) {
    return request(`/rooms/${roomCode}/start`, {
        method: "POST",
        body: JSON.stringify({
            host_id: hostId
        })
    });
}

export function exitRoom(roomCode, playerId) {
    return request(`/rooms/${roomCode}/exit`, {
        method: "DELETE",
        body: JSON.stringify({
            player_id: playerId
        })
    });
}