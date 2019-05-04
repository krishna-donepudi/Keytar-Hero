import os, aubio

#creates a text file of the beats of a song if the file does not exist
def createBeats(song):
	if os.path.isfile("songs/beats" + song + ".txt"):
		pass
	else:
		os.system("aubio beat songs/%s.wav > songs/beats%s.txt" % (song, song))

#creates a text file of the pitches if the file does not exist
def createPitches(song):
	if os.path.isfile("songs/pitches" + song + ".txt"):
		pass
	else:
		os.system("aubio pitch songs/%s.wav > songs/pitches%s.txt" % (song, song))

#creates a text file of the BPM if the file does not exist
def createBPM(song):
	if os.path.isfile("songs/BPM" + song + ".txt"):
		pass
	else:
		os.system("aubio tempo songs/%s.wav > songs/BPM%s.txt" % (song, song))

#checks if the beat and pitch timings are close
def isClose(n1, n2):
	return abs(n1 - n2) < 10

#from https://www.cs.cmu.edu/~112/notes/notes-strings.html
def readFile(path):
    with open(path, "rt") as f:
        return f.read()

#reads the beats from the text file
def readBeats(path):
    file = readFile(path)
    beats = []
    for line in file.splitlines():
        beat = int(float(line[:-1])*1000)
        beats.append(beat)
    return beats

#reads the BPM from a text file
def readBPM(path):
	file = readFile(path)
	[BPM, word] = file.split(" ")
	return float(BPM)

#creates the pitches at the beats of the song
def detect(song):
	file = readFile("songs/pitches" + song + ".txt")
	result = []
	beats = readBeats("songs/beats" + song + ".txt")
	for line in file.splitlines():
		if len(beats) == 0:
			break
		[time, pitch] = line.split("\t")
		beat = beats[0]
		if isClose(float(time)*1000, float(beat)):
			result.append(float(pitch[:-4]))
			beats.pop(0)
	return result

#classifies into notes based on pitches
#this algorithm assures an equal distribution of notes
def buckets(song):
    pitches = detect(song)
    pitchesSorted = sorted(pitches)
    length = len(pitches)
    level1 = pitchesSorted[length//4]
    level2 = pitchesSorted[length//2]
    level3 = pitchesSorted[(3 * length)//4]
    commands = []
    for pitch in pitches:
        if 0 <= pitch < level1:
            commands.append(0)
        elif level1 <= pitch < level2:
            commands.append(1)
        elif level2 <= pitch < level3:
            commands.append(2)
        else:
            commands.append(3)
    return commands