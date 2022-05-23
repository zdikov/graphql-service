import typing
import strawberry


@strawberry.type
class Player:
    id: int
    name: str
    score: int


@strawberry.type
class Game:
    id: int
    players: typing.List[Player]
    comments: typing.List[str]


@strawberry.type
class Query:
    games: typing.List[Game]


players = [
    Player(id=0, name="player1", score=300),
    Player(id=1, name="player2", score=200),
    Player(id=2, name="player3", score=100),
]

id_to_game = {
    0: Game(id=0, players=players, comments=[]),
    1: Game(id=1, players=players, comments=[]),
    2: Game(id=2, players=players, comments=[])
}


@strawberry.type
class Query:
    @strawberry.field
    def games(self, id: typing.Optional[int] = None) -> typing.List[Game]:
        if id is None:
            return list(id_to_game.values())
        else:
            try:
                return [id_to_game[id]]
            except:
                return []


@strawberry.type
class Mutation:
    @strawberry.mutation
    def add_comment(self, id: int, comment: str) -> typing.Optional[Game]:
        try:
            id_to_game[id].comments.append(comment)
            return id_to_game[id]
        except:
            return None


schema = strawberry.Schema(query=Query, mutation=Mutation)
