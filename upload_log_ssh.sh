#/bin/sh
DIR=/home/pi/ph
LOG=$DIR/thermoheater.log
TMP=$DIR/thermoheater.tmp
SAV=$DIR/thermoheater.logged
RDY=$DIR/thermoheader.ready
UPL=david@ubmedia:data/thermoheater_`uname -n`_`date +%Y%m%d_%H%M%S`.log
UPLOAD="scp"
if [ -f $TMP ]; then rm -f $TMP; fi
if [ -f $LOG ]; then
    # immediately rename in case logger runs while we are uploading
    mv $LOG $TMP
    cat $TMP >> $RDY
    cat $TMP >> $SAV
    rm $TMP
fi
if [ -f $RDY ]; then
    # upload the ready file as a new destination file
    $UPLOAD $RDY $UPL
    if [ "$?" = "0" ]; then
        rm $RDY
    fi
fi

