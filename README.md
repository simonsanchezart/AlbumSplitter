# AlbumSplitter

A cmd tool that takes an .mp3 and a .txt with timestamps, splits the mp3 based on those timestamps.

```pip install pydub``` - Requirement

## Usage

The .mp3 and .txt should be in their own folder together.

```albumSplit.py invertTimestampPosition``` (y/n)

If in your .txt the timestamps are at the right of the songs names, you must invert the timestamp position

```
Case 1:
  SongA 00:00
  SongB 01:00
  SongC 02:00

  Proper usage: albumSplit.py y

Case 2:
  00:00 SongA
  01:00 SongB
  02:00 SongC
  
  Proper usage: albumSplit.py n || albumSplit.py
