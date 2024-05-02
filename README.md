# Youbike 歷史數據資料庫
因目前 Youbike 相關數據僅提供實時數據，沒辦法知道:「`我家旁邊的站點何時會補車?`」、「`我家旁邊的站點沒車的時段大約是幾點?`」諸如此類的資訊。因此想新增一個專案來累積 Youbike 站點車輛數的歷史車輛數數據。


## Schema

### sites
站點基本資料，是一張維度表。

| 欄位名稱 | 資料型態 | 描述     |
|----------|----------|----------|
| sno      | STRING   | 站點編號         |
| sna      | STRING   |  站點中文名稱        |
| tot      | INT      | 總停車格數         |
| sarea    | STRING   |  站點所在行政區        |
| lat      | DOUBLE   | 站點緯度         |
| lng      | DOUBLE   | 站點經度         |
| ar       | STRING   |  站點地址        |
| sareaen  | STRING   |  站點行政區(英文)        |
| aren     | STRING   | 站點地址(英文)         |
| act      | STRING   |  全站禁用狀態(0:禁用中、1:啟用中)        |
---

### slots
站點車輛數量的資訊，是一張事實表。

| 欄位名稱 | 資料型態 | 描述     |
|----------|----------|----------|
| sno      | STRING   | 站點編號         |
| sbi      | INT   |  站點目前車輛數量        |
| infoTime      | DATETIME      | 資料更新時間         


## Note
- 沒有保留車輛"空位資訊"，請自行將總停車格數(sites.tot) 減去目前車輛數 (slots.sbi)。
- 蒐集過程中發現不是所有站點都會上傳數據，有些站點最新的更新數據是過去好幾個月的。如果找不到站點的歷史數據，有可能是沒在傳數據的站點。可以自行呼叫 [API](https://tcgbusfs.blob.core.windows.net/dotapp/youbike/v2/youbike_immediate.json) 確認一下。


## Reference
- 數據來源: https://data.gov.tw/dataset/137993
