

find covid/ -type f -name '*.png' -delete

curl -o all-states-history.csv https://covidtracking.com/data/download/all-states-history.csv

veb
python3 create_small_multiples.py 

aws s3 cp covid/ s3://svz-public/covid_small_multiples/ --recursive --exclude "*" --include "ß*.png"


