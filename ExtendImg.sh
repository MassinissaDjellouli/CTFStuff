verbose_only=0
if [ $# -eq 0 ]; then
    echo "ExtendImg.sh [image] -v for verbose only"
    exit 1
fi
if [ -z $2 ]
then
    verbose_only=0
else
    verbose_only=1
fi

if [ $verbose_only -eq 0 ]
then
    identify -verbose $1
    read -p "Extend? (y/n) " yn
    case $yn in
        [Yy]* ) imganalyzer.exe $1 -t jpg --height 3000;;
        * ) exit;;
    esac
else
    identify -verbose $1
fi
