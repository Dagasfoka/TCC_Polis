from backend.app.repositories.redis.match_repo import get_match_state


def test_get_match() -> None:
        print(get_match_state(1))

if __name__ == "__main__":
    test_get_match()
