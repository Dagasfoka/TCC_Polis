import { useState } from "react";
import { createPlayer } from "../service/api.jsx";

export default function Login({ onLogin }) {

    const [nickname, setNickname] = useState("");
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");

    async function handleLogin(event) {
        event.preventDefault();

        if (!nickname.trim()) {
            setError("Digite um nickname.");
            return;
        }

        try {
            setLoading(true);
            setError("");

            const player = await createPlayer(
                nickname.trim()
            );

            localStorage.setItem(
                "player_id",
                player.player_id
            );

            onLogin(player);

        } catch (error) {
            setError(error.message);
        } finally {
            setLoading(false);
        }
    }

    return (
        <div className="login-container">

            <h1>POLIS</h1>

            <p>Entre no jogo</p>

            <form onSubmit={handleLogin}>

                <input
                    type="text"
                    placeholder="Seu nickname"
                    value={nickname}
                    maxLength={30}
                    onChange={(event) =>
                        setNickname(event.target.value)
                    }
                />

                {error && <p>{error}</p>}

                <button
                    type="submit"
                    disabled={loading}
                >
                    {loading ? "Entrando..." : "ENTRAR"}
                </button>

            </form>

        </div>
    );
}