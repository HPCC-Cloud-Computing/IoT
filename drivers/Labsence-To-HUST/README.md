#Các index lưu trữ trong Elasticsearch

##day-stats-summary

Trong index, type name được đặt theo ngày lấy dữ liệu, id là giá trị băm của tất cả các trường được lưu trữ trong index.

| Parameter   |		Description               |
|-------------|-----------------------------------|
| regionId        | ID của region            |
| regionName        | Tên của region            |
| date        | Ngày ghi nhận thông tin           |
| numVisitors       | Số lượng người tới region trong ngày           |
| avgDuration       | Thời gian trung bình lưu lại region của tất cả các visitor            |
| numReturningVisitors       | Số lượng người quay trở lại region đồng thời đã từng tới region trong vong 4 tháng gần đây      |

##day-stats-summary

| Parameter   |		Description               |
|-------------|-----------------------------------|
| type   | RegionNames          |

##day-stats-summary

| Parameter   |		Description               |
|-------------|-----------------------------------|
| type   | RegionNames          |

##day-stats-summary

| Parameter   |		Description               |
|-------------|-----------------------------------|
| type   | RegionNames          |

##day-stats-summary

| Parameter   |		Description               |
|-------------|-----------------------------------|
| type   | RegionNames          |


Ngoài ra script còn đồng thời lưu trữ dữ liệu lấy được ra file text, trong các folder có tên trùng với index name trong Elasticsearch nhằm tránh trường hợp Elasticsearch bị lỗi.



