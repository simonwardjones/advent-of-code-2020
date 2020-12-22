import time
from itertools import cycle, islice
from collections import deque

start_time = time.time()


def load_data():
    with open('day_twenty_two_data.txt') as fh:
        players = fh.read().split('\n\n')
        players = [deque(map(int, player.split('\n')[1:]))
                   for player in players]
        return players


def play(player_one, player_two):
    while len(player_one) > 0 and len(player_two) > 0:
        # print(player_one, player_two)
        card_one = player_one.popleft()
        card_two = player_two.popleft()
        if card_one == card_two:
            raise Exception('same card not handled')
        if card_one > card_two:
            player_one += [card_one, card_two]
        else:
            player_two += [card_two, card_one]
    return player_one, player_two, 1 if player_one else 2


# player_one, player_two = load_data()
# player_one, player_two, winner = play(player_one, player_two)
# for i, player in enumerate((player_one, player_two)):
#     if player:
#         print(f'Player {winner} WON (the crab) ! with score:')
#         print(sum((j+1)*card for j, card in enumerate(list(player)[::-1])))


# part  2


def play_recursive(player_one, player_two, game=1):
    freeze_frames = []
    round = 1
    # print(f'=== Game {game} ===\n')
    while len(player_one) > 0 and len(player_two) > 0:
        freeze_frame = tuple((tuple(player_one), tuple(player_two)))
        if freeze_frame in freeze_frames:
            # print('freeze win !!')
            return player_one, player_two, 1
        # print(f"-- Round {round} (Game {game}) --")
        # print("Player 1's deck: ", player_one)
        # print("Player 2's deck: ", player_two)
        card_one = player_one.popleft()
        card_two = player_two.popleft()
        # print("Player 1 plays: ", card_one)
        # print("Player 2 plays: ", card_two)
        if len(player_one) >= card_one and len(player_two) >= card_two:
            _, _, winner = play_recursive(
                deque(islice(player_one, card_one)),
                deque(islice(player_two, card_two)),
                game+1)
        else:
            winner = 1 if card_one > card_two else 2
        # print(f'Player {winner} wins round {round} of game {game}!\n')
        if winner == 1:
            player_one += [card_one, card_two]
        elif winner == 2:
            player_two += [card_two, card_one]
        freeze_frames.append(freeze_frame)
        round += 1
    return player_one, player_two, 1 if player_one else 2


player_one, player_two = load_data()
player_one, player_two, winner = play_recursive(player_one, player_two)
print(player_one, player_two, winner)

print(sum((j+1)*card
          for j, card in enumerate(list([player_one, player_two][winner-1])[::-1])
          )
      )


print("--- %s seconds ---" % (time.time() - start_time))
