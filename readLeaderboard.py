#this reads the leaderboard and returns the top 4 players and their scores

#from https://www.cs.cmu.edu/~112/notes/notes-strings.html
def readFile(path):
	with open(path, "rt") as f:
		return f.read()

#creates a list of tuples with the player and his score
def createList(path):
	players = []
	leaderboard = readFile(path)
	for line in leaderboard.splitlines():
		[person, score] = line.split("\t")
		players.append((person, score))
	return players

#returns the highest scorer on a list of tuple
def getHighest(players):
	high = 0
	for (player, score) in players:
		if int(score) > high:
			high = int(score)
			highestPlayer = player
	players.remove((highestPlayer, str(high)))
	return (highestPlayer, str(high))

#returns the top4 players and their scores
def makeLeaderboard(path):
	players = createList(path)
	(first, high1) = getHighest(players)
	(second, high2)= getHighest(players)
	(third, high3) = getHighest(players)
	(fourth, high4) = getHighest(players)
	return [(first, high1), (second, high2), (third, high3),
		(fourth, high4)]