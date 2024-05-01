date=$(date -d "2 days ago" +%Y-%m-%d)
branch_name=upload-data-$date

git pull
/home/tses89214/ubike-historical-data/my_venv/bin/python3 /home/tses89214/ubike-historical-data/daily_upload_data.py
git add data/*

git commit -m "chore: auto add data $date"
git push