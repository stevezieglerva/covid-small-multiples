

curl -o all-states-history.csv https://covidtracking.com/data/download/all-states-history.csv

python3 create_small_multiples.py 

aws s3 cp ./ s3://svz-public/covid_multiple_smalls/ --recursive --exclude "*" --include "covid_*.png"


