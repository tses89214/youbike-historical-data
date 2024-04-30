today=$(date +%Y-%m-%d)
branch_name=upload-data-$today

python weekly_upload_data.py

git checkout develop
git pull
git checkout -b chore/$branch_name
git add data/$today.csv

git commit -m "chore: auto add data $today"
git push

rm data/$today.csv