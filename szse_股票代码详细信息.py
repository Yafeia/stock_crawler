import requests
import pandas as pd

# 目标 URL
url = "https://www.cninfo.com.cn/new/data/szse_stock.json"

# 请求头模拟浏览器
headers = {
    "accept": "application/json, text/plain, */*",
    "referer": "https://www.cninfo.com.cn/new/index.jsp",
    "sec-ch-ua": '"Google Chrome";v="137", "Chromium";v="137", "Not/A)Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.37"
}

# 发送请求
response = requests.get(url, headers=headers)
response.encoding = 'utf-8'

# 检查响应状态
if response.status_code == 200:
    data = response.json()
    stock_list = data.get('stockList', [])

    # 转为DataFrame
    df = pd.DataFrame(stock_list)

    # 保存为CSV
    df.to_csv('szse_stock_list.csv', index=False, encoding='utf-8-sig')
    print("✅ 数据已成功保存到 szse_stock_list.csv")
else:
    print(f"❌ 请求失败，状态码: {response.status_code}")
