#!2048env/bin/python3
import Dojo
import BoardGame

D = Dojo.Darwin(n=1)
D.recall_players(n=10)
D.trainning(epochs=200)
D.plot_history()

D.get_best().play_game(BoardGame.board(), delay=True)
