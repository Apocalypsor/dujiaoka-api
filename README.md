# dujiaoka-api

### 环境变量
```bash
DUJIAO_BASE_URL="https://dujiaoka.com/admin"
DUJIAO_USERNAME="admin"
DUJIAO_PASSWORD="admin"
```

### 使用方法
```python
from dujiaoka import order, carmi

orders = order.get("/order?goods_id=1", require_text=False)
carmis = carmi.get("/carmis?goods_id=1")
order.modify(id=100, status=2, order_id="1_s9csani2e")
```