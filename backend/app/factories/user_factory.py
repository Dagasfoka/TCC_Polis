from backend.app.repositories.db.user_repo import UsersRepository
from backend.app.utils.ids import generate_password_hash

class UserFactory:
    def __init__(self) -> None:
        self.user_repository=UsersRepository()
    def create_user(self,username,password):
        password_hash = generate_password_hash(password)
        return self.user_repository.create_user(username,password_hash)
    def update_player_id(self,user,player_id):
        return self.user_repository.update_player_id(user,player_id)