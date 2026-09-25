
import { useState } from "react";

import {
    createRoom,
    joinRoom
} from "../services/api";

export default function Menu({ player, onEnterRoom }) {

    const [roomCode, setRoomCode] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

    async function handleCreateRoom() {
        try {
            setLoading(true);
            setError("");

            const room = await createRoom(
                player.player_id
            );

            onEnterRoom(room);

        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    }

    async function handleJoinRoom() {
        if (!roomCode.trim()) {
            setError("Digite o código da sala.");
            return;
        }

        try {
            setLoading(true);
            setError("");

            const room = await joinRoom(
                roomCode.trim(),
                player.player_id
            );

            onEnterRoom(room);

        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="menu-container">

            <h1>POLIS</h1>

            <h2>Bem-vindo, {player.username}!</h2>

            <button
                onClick={handleCreateRoom}
                disabled={loading}
            >
                CRIAR SALA
            </button>

            <div className="join-room">

                <input
                    type="text"
                    placeholder="Código da sala"
                    value={roomCode}
                    onChange={(event) =>
                        setRoomCode(event.target.value)
                    }
                />

                <button
                    onClick={handleJoinRoom}
                    disabled={loading}
                >
                    ENTRAR NA SALA
                </button>

            </div>

            {error && <p>{error}</p>}

        </div>
    );
}