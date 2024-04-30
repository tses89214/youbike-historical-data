today=$(date +%Y-%m-%d)
branch_name=upload-data-$today

git checkout develop
git pull
git checkout -b chore/$branch_name
/home/tses89214/ubike-historical-data/my_venv/bin/python3 /home/tses89214/ubike-historical-data/weekly_upload_data.py
git add data/*

git commit -m "chore: auto add data $today"
git push --set-upstream origin chore/$branch_name

rm -r data