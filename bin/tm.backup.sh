#!/bin/sh

BACKUPS=$1
ITEM_LIST_FILE=$2

if [ ! -n "$BACKUPS" ];
then
        echo "no timemachine target specified."
        exit
fi

if [ ! -n "$ITEM_LIST_FILE" ];
then
        echo "no item list file specified."
	exit
fi
                                

if [ ! -d $BACKUPS ];
then
 	echo "$BACKUPS doesn't exist -> stopping"
	exit
fi


TSTMP=`date +%Y%m%d_%w_%H.%M.%S`

DST_FOLDER="$BACKUPS/$TSTMP"
LAST_DIR="$BACKUPS/last"

echo "making backup for $DST_FOLDER"
echo "LAST_DIR = $LAST_DIR"



if [ -d $DST_FOLDER ];
then
	echo "...already exists -> stopping"
	exit
fi

mkdir -p $DST_FOLDER

if [ -d $LAST_DIR ];
then
	echo "# make delta."

	# sync directory structure
	rsync -av --include '*/' --exclude '*' $LAST_DIR/* $DST_FOLDER/

	# make links
	cd $LAST_DIR
	#find * -type f | xargs --verbose -I'{}' ln '{}' ../$TSTMP/'{}'
	find * -type f -exec ln "{}" ../$TSTMP/"{}" \;
	cd -

	# sync
	cat $ITEM_LIST_FILE | \
		xargs -I{} rsync -av --delete {} $DST_FOLDER/
else
	echo "# initial."
	cat $ITEM_LIST_FILE | \
		xargs -I{} rsync -av {} $DST_FOLDER/
fi

# link last backup
rm -f $LAST_DIR
ln -s $TSTMP $LAST_DIR

# thin out backups:
# keep hourly for last 24, keep daily for last 7 days, and keep monthly for the rest

# find all hourly backups older than 24h which are made at the end of the day (22:00)
# add _d as suffix
find $BACKUPS/????????_?_22.??.?? -maxdepth 0 -type d -mmin +1440 -exec mv "{}" "{}"_d \;

# now repeat the search to get all remaining hourly backups older than 24h and remove them
find $BACKUPS/????????_?_??.??.?? -maxdepth 0 -type d -mmin +1440 -exec rm -Rf "{}" \;

# same game for weekly backups
# find all daily older than 30 days, which are made on sunday, append _w as suffix
find $BACKUPS/????????_0_??.??.??_d -maxdepth 0 -type d -mtime +30 -exec mv "{}" "{}"_w \; 

# then remove all remaining older than 28 days
find $BACKUPS/????????_?_??.??.??_d -maxdepth 0 -type d -mtime +30 -exec rm -Rf "{}" \;

# finally remove everything older than 180 days
find $BACKUPS/????????_?_??.??.??* -maxdepth 0 -type d -mtime +180 -exec rm -Rf "{}" \;
