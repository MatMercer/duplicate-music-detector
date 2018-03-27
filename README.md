# Duplicate music detector

A simple command line utillity that detects duplicate music inside a folder, using pytaglib library.

## Usage

```bash
# Search for duplicate musics inside ~/Music folder, verbosely
ddsong -v ~/Music 

# Deletes every detected duplicate music inside ~/Music folder, take caution
ddsong ~/Music | xarg rm -v

# Display help & exit
ddsong -h

# Display version & exit
ddsong -V
```

## How it detects duplicate music

The algorithm is very simple:
1. Extract the title of the music
2. Clean the title, using lower case, removing remastered, live, etc keywords. Currently quite buggy, since it only detects keywords inside parentheisis, like (remastered)
3. Append lower case artist to the extrated title. ie: "bring it down - oasis"
4. If the title + artist isn't already in a array, append the title + artist to a array. If it already is, a dupe is detected
5. After parsing all files, send the dupe list to stdout

