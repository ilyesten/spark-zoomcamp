#!/bin/bash
set -e

TAXI_TYPE=$1
YEAR=$2

echo "Type : ${TAXY_TYPE}, year: ${YEAR}"
URL_PREFIX="https://github.com/DataTalksClub/nyc-tlc-data/releases/download"

for MONTH in {1..12}; do

    FMONTH=$(printf "%02d" ${MONTH})
    FILE_NAME="${TAXI_TYPE}_tripdata_${YEAR}-${FMONTH}.csv.gz"
    URL="${URL_PREFIX}/${TAXI_TYPE}/${FILE_NAME}"

    LOCAL_DIR="data/raw/${TAXI_TYPE}/${YEAR}/${FMONTH}"
    LOCAL_PATH="${LOCAL_DIR}/${FILE_NAME}"


    echo "${URL} -> ${LOCAL_PATH}"
    mkdir -p ${LOCAL_DIR}
    wget ${URL} -O ${LOCAL_PATH}
    

done








