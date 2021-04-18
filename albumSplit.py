import sys
import glob
from pydub import AudioSegment

class Song():
    cumulativeDurationInMs = 0

    def __init__(self, name, lowTimestamp):
        self.SetName(name)
        self.lowTimestamp = lowTimestamp
        self.highTimestamp = 0

        self.durationInMs = 0
        self.startTimeInMs = 0
        self.endTimeInMs = 0

    def GetName(self):
        return self.name

    def GetLowTimestamp(self):
        return self.lowTimestamp

    def GetHighTimestamp(self):
        return self.highTimestamp

    def GetStartTimeInMs(self):
        return self.startTimeInMs

    def GetEndTimeInMs(self):
        return self.endTimeInMs

    def GetDurationInMs(self):
        return self.durationInMs

    def SetName(self, name):
        forbiddenChars = ('\\', '/', ':', '*', '?', '"', '<', '>', '|')
        for char in forbiddenChars:
            name = name.replace(char, '')

        name = name.strip()
        self.name = name

    def SetHighTimestamp(self, highTimestamp):
        self.highTimestamp = highTimestamp

    def SetDurationInMs(self, durationInMs):
        self.durationInMs = durationInMs

    def SetStartTime(self):
        startTimeHour = int(self.lowTimestamp[0])
        startTimeMinute = int(self.lowTimestamp[1])
        startTimeSecond = int(self.lowTimestamp[2])

        startTimeHourMs = startTimeHour * 60 * 60 * 1000
        startTimeMinuteMs = startTimeMinute * 60 * 1000
        startTimeSecondMs = startTimeSecond * 1000

        self.startTimeInMs = startTimeHourMs + startTimeMinuteMs + startTimeSecondMs
        
    def SetEndTime(self):
        self.endTimeInMs = self.startTimeInMs + self.durationInMs

    def CalculateDurationInMs(self):
        deltaHours = int(self.highTimestamp[0]) - int(self.lowTimestamp[0])
        deltaMinutes = int(self.highTimestamp[1]) - int(self.lowTimestamp[1])
        deltaSeconds = int(self.highTimestamp[2]) - int(self.lowTimestamp[2])

        hoursInMs = deltaHours * 60 * 60 * 1000
        minutesInMs = deltaMinutes * 60 * 1000
        secondsInMs = deltaSeconds * 1000

        duration = hoursInMs + minutesInMs + secondsInMs
        Song.cumulativeDurationInMs += duration
        
        self.SetDurationInMs(duration)
        self.SetStartTime()
        self.SetEndTime()

invertTimestampPosition = False
if len(sys.argv) > 1:
    if sys.argv[1].lower() == 'y':
        invertTimestampPosition = True

for file in glob.glob("*.mp3"):
    albumFile = file

print(f"Loading {albumFile.title()}...\n")
albumSegment = AudioSegment.from_mp3(albumFile)

for file in glob.glob("*.txt"):
    albumStampFile = file
albumStamps = open(albumStampFile, "r", encoding='utf-8')

allSongs = []
for stamp in albumStamps:
    stamp = stamp.strip()
    titleAndStamp = stamp.split(" ")

    if invertTimestampPosition:
        songTitle = titleAndStamp[0:-1]
        songLowTimeStamp = titleAndStamp[-1]
    else:
        songTitle = titleAndStamp[1:]
        songLowTimeStamp = titleAndStamp[0]

    fullTitle = " ".join(songTitle)

    songLowTimeStamp = songLowTimeStamp.split(":")
    songLowTimeStamp[-1] = songLowTimeStamp[-1][0:2] # remove some artifacts on last item of the list

    if len(songLowTimeStamp) < 3:
        songLowTimeStamp.insert(0, "00")

    newSong = Song(fullTitle, songLowTimeStamp)
    allSongs.append(newSong)

for i in range(len(allSongs)):
    song = allSongs[i]
    if i != len(allSongs)-1:
        song.SetHighTimestamp(allSongs[i+1].GetLowTimestamp())
        song.CalculateDurationInMs()

    finalName = f"{i+1:02d}- {song.GetName()}" # :02d adds leading zeroes
    print(f"Saving {finalName}...")

    if i == 0:
        songSegment = albumSegment[:song.GetDurationInMs()]
    elif i == len(allSongs)-1:
        songSegment = albumSegment[Song.cumulativeDurationInMs:]
    else:
        songSegment = albumSegment[song.GetStartTimeInMs():song.GetEndTimeInMs()]

    songSegment.export(f"{finalName}.mp3", format="mp3")