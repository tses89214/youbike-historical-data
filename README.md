# Youbike 歷史數據資料庫
目前公開數據中關於台北市 Youbike 的車輛數據僅提供實時數據，沒辦法知道:「`我家旁邊的站點何時會補車?`」、「`我家旁邊的站點沒車的時段大約是幾點?`」的資訊。因此想新增一個專案來累積歷史車輛數之數據。

## 系統邏輯
1. 每十分鐘呼叫一次 [API](https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json)，取得當下的車輛數據，並切分成 sites 和 slots 兩張表:
   - sites 為站點資訊，是一張維度表，儲存站點的基本資訊如地址、編號等。
   - slots 為站點車輛數，是一張事實表，儲存站點的編號、車輛數、更新時間。
2. 資料會暫存於個人的資料庫中，並於每日晚上一點(+8)上傳前一天的數據至 Github，例如 05/02 01:00 會上傳更新時間 = 05/01 的數據。
3. slots 表基本上每天更新上傳，sites 表僅有數據有更新時才會上傳(例如站點有異動等)。

## Schema

### sites
站點基本資料。

| 欄位名稱 | 資料型態 | 描述     |
|----------|----------|----------|
| sno      | STRING   | 站點編號         |
| sna      | STRING   |  站點中文名稱        |
| sarea    | STRING   |  站點所在行政區        |
| latitude      | DOUBLE   | 站點緯度         |
| longitude      | DOUBLE   | 站點經度         |
| ar       | STRING   |  站點地址        |
| sareaen  | STRING   |  站點行政區(英文)        |
| aren     | STRING   | 站點地址(英文)         |
| act      | STRING   |  全站禁用狀態(0:禁用中、1:啟用中)        |
---

### slots
站點車輛數量的資訊。

| 欄位名稱 | 資料型態 | 描述     |
|----------|----------|----------|
| sno      | STRING   | 站點編號         |
| total      | INT      | 總停車格數         |
| available_rent_bikes      | INT   |  可借車輛數量        |
| available_return_bikes      | INT   |  可還車輛數量(空位)        |
| infoTime      | DATETIME      | 資料更新時間         


## Note
- 請注意有些時候下 total != available_rent_bikes + available_return_bikes，可能站點上面有停止服務的車輛等等。所以可能會出現 total 有 20，但 available_rent_bikes 只有 5，available_return_bikes 只有 10。換句話說站點上可能就有 5 台停止服務的車輛。
- 蒐集過程中發現不是所有站點都會上傳數據，有些站點最新的更新數據是過去好幾個月的。如果找不到站點的歷史數據，有可能是沒在傳數據的站點。可以自行呼叫 [API](https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json) 確認一下。
- 其實 API 裡面有提供好幾個時間欄位，分別是站點上傳數據的時間、Youbike DB 接收到數據的時間等。個人認為站點上傳的時間比較有參考價值，因此以 infoTime (站點上傳時間) 為主。


## Reference
- 數據來源: https://data.gov.tw/dataset/137993

## murmur
