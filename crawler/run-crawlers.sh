#!/usr/bin/env bash

# ----------------------------------------------------------------------
# Runs all crawlers.
# ----------------------------------------------------------------------

function make_backup_of() {
    BKP_FILENAME="${1}.bkp"
    if [ -f $BKP_FILENAME ]; then
        rm $BKP_FILENAME
    fi

    if [ -f $1 ]; then
        mv $1 $BKP_FILENAME
    fi
}


DEFAULT_FILENAME=items.json

echo "**************************************************"
echo "*** BEGIN"
echo "**************************************************"
echo ""

echo "**************************************************"
echo "*** crawler cnpq"

cd cnpq
make_backup_of $DEFAULT_FILENAME
scrapy crawl --output=$DEFAULT_FILENAME --output-format=json cnpq

echo "**************************************************"
echo "*** crawler dfg.de"
cd ../dfg.de
make_backup_of $DEFAULT_FILENAME
python prizes.py

echo "**************************************************"
echo "*** crawler faperj"
cd ../faperj
make_backup_of $DEFAULT_FILENAME
scrapy crawl --output=$DEFAULT_FILENAME --output-format=json faperj

echo "**************************************************"
echo "*** crawler grant.gov"
cd ../grant.gov
make_backup_of grants_gov_ca.json
python spiders/cooperative_agreement.py
make_backup_of grants_gov_g.json
python spiders/grants.py

echo "**************************************************"
echo "*** crawler nsf"
cd ../nsf
make_backup_of $DEFAULT_FILENAME
scrapy crawl --output=$DEFAULT_FILENAME --output-format=json nsf

echo ""
echo "**************************************************"
echo "*** END"
echo "**************************************************"
