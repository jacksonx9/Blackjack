# Blackjack

> Standard game of blackjack with 1 deck and up to 6 players.

### Run Game

```shell
python play_game_regularized_version/play.py
```

### Machine Learning

#### Generate Data

```shell
python machine_learning/run.py 
```

#### Train Model

```shell
cd machine_learning/logistic_regression
octave
```

```octave
run
```

### Project Demo

![](https://github.com/jacksonx9/Blackjack/blob/master/photos%20%2B%20gifs/create_data_blackjack.gif)

![](https://github.com/jacksonx9/Blackjack/blob/master/photos%20%2B%20gifs/blackjack_play_game_example)

### Game Cycle

Collect names of players and their starting chip balance then cycle through game process:

1. deal initial cards
2. check dealer blackjack
3. for each player’s hand:
   1. offer split, double down, hit or stand if possible
   2. if player busts, mark as finished and move to next
   3. then dealer plays until busts or stands
   4. show results and settle bets

When game is complete show results for each player and their balance.