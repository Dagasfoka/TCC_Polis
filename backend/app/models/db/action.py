class Action:
    def __init__(self, action_id: int, action_type: str, alignment : str, title:str , statement :str, content: dict):
        self.action_id = action_id
        self.action_type = action_type
        self.alignment = alignment
        self.title = title
        self.statement = statement
        self.content = content

    def to_dict(self):
        return {
            "action_id": self.action_id,
            "action_type": self.action_type,
            "alignment": self.alignment,
            "title": self.title,
            "statement": self.statement,
            "content": self.content,
        }

    @classmethod
    def create(cls, action_id: int, action_type: str, alignment : str, title:str , statement :str, content: dict):
        return cls(
            action_id, action_type, alignment, title, statement, content
        ).to_dict()

    @staticmethod
    def create_gain(money:int , influence: int, corruption: int | None = None):
        return {
            "money": money,
            "influence": influence,
            "corruption": corruption,
        }

    @staticmethod
    def create_content(description : str, cost : int, gains:dict, success_chance: int):
        return {
            "description": description,
            "cost": cost,
            "gains": gains,
            "success_chance": success_chance,
        }