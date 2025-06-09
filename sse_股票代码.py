import requests
import pandas as pd
import json
import re
import time

# 固定参数设置
url = "https://query.sse.com.cn/sseQuery/commonQuery.do"
headers = {
    "Referer": "https://www.sse.com.cn/",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.37",
    "Accept": "*/*",
}
base_params = {
    "STOCK_TYPE": "1",
    "REG_PROVINCE": "",
    "CSRC_CODE": "",
    "STOCK_CODE": "",
    "sqlId": "COMMON_SSE_CP_GPJCTPZ_GPLB_GP_L",
    "COMPANY_STATUS": "2,4,5,7,8",
    "type": "inParams",
    "isPagination": "true",
    "pageHelp.cacheSize": "1",
    "pageHelp.pageSize": "25",  # 每页 25 条
}

# 总页数为 68，根据实际情况修改
total_pages = 68
all_results = []

for page_no in range(1, total_pages + 1):
    print(f"📄 正在抓取第 {page_no} 页 ...")

    params = base_params.copy()
    params["pageHelp.beginPage"] = str(page_no)
    params["pageHelp.pageNo"] = str(page_no)
    params["pageHelp.endPage"] = str(page_no)
    params["jsonCallBack"] = f"jsonpCallback{int(time.time() * 1000)}"
    params["_"] = str(int(time.time() * 1000))

    response = requests.get(url, headers=headers, params=params)
    text = response.text

    # 提取 JSON 内容
    match = re.search(r"jsonpCallback\d+\((.*)\)", text)
    if match:
        json_str = match.group(1)
        data = json.loads(json_str)
        page_data = data.get("result", [])
        all_results.extend(page_data)
    else:
        print(f"❌ 第 {page_no} 页提取失败！")
    
    time.sleep(0.3)  # 避免请求过快被封

# 转换为 DataFrame 并保存
df = pd.DataFrame(all_results)
df.to_csv("sse_stock_list.csv", index=False, encoding="utf-8-sig")
print("✅ 所有页数据已保存到 sse_stock_list.csv")
