from gql import gql, Client
from gql.transport.aiohttp import AIOHTTPTransport

transport = AIOHTTPTransport(url="http://127.0.1.1:8000")

client = Client(transport=transport, fetch_schema_from_transport=True)

query_all_games = gql(
    """
    {
      games {
        id
        players {
          id
          name
          score
        }
        comments
      }
    }
"""
)

template_get_game = """
{
  games(id: <game_id>) {
    id
    players {
      id
      name
      score
    }
    comments
  }
}
"""

template_add_comment = """
mutation {
  addComment(id: <game_id>, comment:"<comment>") {
    id
    players {
      id
      name
      score
    }
    comments
  }
}
"""


def print_game(game):
    print(f'Game {game["id"]} {{')
    for player in game['players']:
        print(f'    player {player["id"]}: name = {player["name"]}, score = {player["score"]}')
    print('}')
    print('Comments:', game['comments'])


while True:
    command = input('next command: ')
    if command == 'exit':
        break
    elif command == 'get_all_games':
        result = client.execute(query_all_games)
        for game in result['games']:
            print_game(game)
    else:
        split = command.split()
        if len(split) == 2:
            command, game_id = command.split()

            if command == 'get_game':
                result = client.execute(gql(template_get_game.replace('<game_id>', game_id)))
                if len(result['games']) == 0:
                    print('Game not found')
                else:
                    print_game(result['games'][0])
            elif command == 'add_comment':
                comment = input('comment: ')
                result = client.execute(
                    gql(template_add_comment.replace('<game_id>', game_id).replace('<comment>', comment)))
                if result is None:
                    print('Game not found')
                else:
                    print_game(result['addComment'])
            else:
                print('available commands: "exit", "get_all_games", "get_game <game_id>", "add_comment <game_id>"')
        else:
            print('available commands: "exit", "get_all_games", "get_game <game_id>", "add_comment <game_id>"')
