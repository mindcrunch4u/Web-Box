LINK="$1"
FOLDER="$2"
DEST="$2"/'%(title)s-%(id)s.%(ext)s'
LOG="$FOLDER"/"../description.txt"
echo "INPUT: $LINK"
echo "DEST: $DEST"
mkdir -p "$FOLDER"
touch "$LOG"
yt-dlp -o "$DEST" --extract-audio --audio-format mp3 "$LINK" 2>&1 >> "$LOG"
cd "$FOLDER"/"../"
7z a -p"longpasswordchangeme" -mhe cryptblock ./datablock/* 2>&1 >> "$LOG"
rm -rf "$FOLDER"
echo "1" > confirmation
