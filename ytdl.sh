if [[ $# != 3 ]];then
    echo "bash script.sh <YouTube Link> <Destination Folder> <use_zip_file | none>]"
    exit 1
fi

LINK="$1"
FOLDER="$2"
DEST="$2"/'%(title)s-%(id)s.%(ext)s'
USE_ZIP="$3"
#LOG="$FOLDER"/"../log.txt"
echo "INPUT: $LINK"
echo "DEST: $DEST"
echo "USE_ZIP: $USE_ZIP"

mkdir -p "$FOLDER"
#touch "$LOG"

yt-dlp -o "$DEST" --extract-audio --audio-format mp3 "$LINK" 2>&1 #>> "$LOG"
result=$?
if [[ $result != 0 ]]; then
    echo "-1" > confirmation
    exit 1
fi

cd "$FOLDER"/"../"

if [[ "$USE_ZIP" == "use_zip_file" ]]; then
    7z a -p"longpasswordchangeme" -mhe cryptblock ./datablock/* 2>&1 #>> "$LOG"
    result=$?
    if [[ $result != 0 ]]; then
        echo "-2" > confirmation
        exit 1
    fi
fi

rm -rf "$FOLDER"
echo "1" > confirmation
