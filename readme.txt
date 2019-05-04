Name of Project: Keytar Hero

Description: Keytar Hero allows everyone to play GuitarHero without having to buy an Xbox and the paraphernalia required for GuitarHero. It will use the direction keys to mimic the way notes are played on a GuitarHero guitar. The game will come with varying difficulties and one can record their own songs.

REQUIRED PYTHON FILES: gameFile.py, gameObjects.py, readLeaderboard.py, record.py, songAnalysys.py

REQUIRED MODULES: pygame, aubio, pyaudio

OTHER REQUIREMENTS: images (directory with all the required images for the game), songs (with at least one good wave file), leaderboard.txt with at least four entries.

Instructions:

- In your terminal navigate to the directory in which the project is stored. Navigate into the game directory and run the command 'python3 gameFile.py'. This will start the game.

- Press the play button and then sign in so you can secure highscores for later.

- Type in the name of the song or try recording your own song **[for a short game, use the provided strings3 song]**. If the song does not exist the the songs directory, the screen will reload. (WARNING: the game works well only if the song has well defined BPM, Beats, and pitches).

- Choose your difficulty (Easy, Medium, or Impossible) and play the game.

- When the song ends, the game ends and your results are displayed.

- The game can be paused by pressing the space bar and you can exit to the home screen from the pause menu.

- The home screen also has the leaderboard and the help section.

- The help screen has instructions on how to play the game.

- The leaderboard has the top 4 score along with the usernames of those who recorded those highscores.

- All screens can be navigated forward and backwards with a back button located at the top left hand side of the screen.