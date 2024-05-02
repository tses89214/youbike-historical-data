cd /home/tses89214/ubike-historical-data
date=$(date -d "1 days ago" +%Y-%m-%d)
git pull
/home/tses89214/ubike-historical-data/my_venv/bin/python3 /home/tses89214/ubike-historical-data/daily_upload_data.py
git add data/*
git commit -m "Data: auto add data $date"
git push