1. 以下使用MySQL語法
    SELECT b.id, b.name, SUM(o.amount) as may_amount FROM bnbs b
    LEFT JOIN orders o ON b.id = o.bnb_id
    WHERE o.created_at BETWEEN STR_TO_DATE("2024-05-01", "%Y-%m-%d") AND STR_TO_DATE("2024-05-31", "%Y-%m-%d")
    GROUP BY b.id, b.name
    ORDER BY may_amount DESC
    LIMIT 10

2. 可以針對bnbs.bnd_id, orders.created_at建立複合索引, 能夠加速過濾出5月的所有訂單以及join的速度

API設計所使用的SOLID原則:
S(單一職責原則): validator負責資料的驗證，service負責資料的異動，兩者功能互不重疊，各司其職
O(開放封閉原則): validator的設計是使用ValidateManager管理特定model的validator，每個validator都是繼承Validator物件，這樣在未來如果model需要新增欄位，不需要去動到就有的validator，而是創建一個新的class來負責這個欄位的驗證，並且把這個class加入到ValidateManager即可
L(里氏替換原則): validator上下關係符合里氏替換原則
I(介面隔離原則): 應沒有使用到此原則
D(依賴反轉原則): OrderValidateManager在宣告validators時，指定的class是抽象類別Validator，而不是實體的類別