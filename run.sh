

curl -o all-states-history.csv https://covidtracking.com/data/download/all-states-history.csv

python3 create_small_multiples.py 

aws s3 cp ./ s3://nerdthoughts.net/images/ --recursive --exclude "*" --include "state_*.png"
aws s3 cp ./ s3://www.nerdthoughts.net/images/ --recursive --exclude "*" --include "state_*.png"

