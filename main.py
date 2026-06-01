import requests, feedparser, os, urllib3, time
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# 設定台灣時區
TW = timedelta(hours=8)
def get_now_tw():
    return datetime.utcnow() + TW

# --- 重要設定 ---
GAS_PROXY_URL = "https://script.google.com/macros/s/AKfycbwcMA_Ge2NKS2zGlQV-D81SxL_yK8xvlw9FE_pvmtCSPvqTmnIEUKkl90K8IEa6zXn6/exec" # 請填入您的 Google App Script 網址

def get_last_run_time():
    if os.path.exists("last_run_time.txt"):
        with open("last_run_time.txt", "r") as f:
            try: return datetime.strptime(f.read().strip(), "%Y-%m-%d %H:%M:%S")
            except: pass
    return (get_now_tw() - timedelta(minutes=30)).replace(tzinfo=None)

def save_current_run_time(t):
    with open("last_run_time.txt", "w") as f:
        f.write(t.strftime("%Y-%m-%d %H:%M:%S"))

def fetch_chinatimes(start_time):
    res = []; seen = set()

    # --- 第一區：即時新聞 (原初定稿版邏輯，增加至 15 頁) ---
    print("  - 正在掃描 [即時新聞]...")
    for page in range(1, 16): 
        target = f"https://www.chinatimes.com/realtimenews/?chdtv&page={page}"
        try:
            resp = requests.get(f"{GAS_PROXY_URL}?url={target}", timeout=30)
            soup = BeautifulSoup(resp.text, 'html.parser')
            items = soup.select('ul.vertical-list > li')
            for art in items:
                title_tag = art.select_one('h3.title a')
                time_tag = art.select_one('time')
                if not title_tag or not time_tag: continue
                t_raw = time_tag.get('datetime') or time_tag.text.strip()
                try:
                    dt = datetime.strptime(t_raw[:16].replace('T', ' '), "%Y-%m-%d %H:%M")
                    if dt >= start_time:
                        url = "https://www.chinatimes.com" + title_tag['href']
                        if url not in seen:
                            res.append((dt, title_tag.text.strip(), url))
                            seen.add(url)
                except: continue
        except: continue

    # --- 第二區：政治頻道 (獨立規則) ---
    print("  - 掃描 [政治頻道]...")
    for page in range(1, 4):
        target = f"https://www.chinatimes.com/politic/?chdtv&page={page}"
        try:
            resp = requests.get(f"{GAS_PROXY_URL}?url={target}", timeout=30)
            soup = BeautifulSoup(resp.text, 'html.parser')
            items = soup.select('.article-list .col')
            for art in items:
                title_tag = art.select_one('.title a')
                time_tag = art.select_one('time')
                if not title_tag or not time_tag: continue
                t_raw = time_tag.get('datetime') or time_tag.text.strip()
                try:
                    t_str = t_raw[:16].replace('T', ' ')
                    if t_str[2] == ':':
                        p = t_str.split(' ')
                        t_str = f"{p[1]} {p[0]}"
                    dt = datetime.strptime(t_str, "%Y-%m-%d %H:%M")
                    if dt >= start_time:
                        url = title_tag['href']
                        if not url.startswith('http'): url = "https://www.chinatimes.com" + url
                        if url not in seen:
                            res.append((dt, title_tag.text.strip(), url))
                            seen.add(url)
                except: continue
        except: continue

    # --- 第三區：言論頻道 (獨立規則) ---
    print("  - 掃描 [言論頻道]...")
    for page in range(1, 4):
        target = f"https://www.chinatimes.com/opinion/?chdtv&page={page}"
        try:
            resp = requests.get(f"{GAS_PROXY_URL}?url={target}", timeout=30)
            soup = BeautifulSoup(resp.text, 'html.parser')
            items = soup.select('.article-list .col')
            for art in items:
                title_tag = art.select_one('.title a')
                time_tag = art.select_one('time')
                if not title_tag or not time_tag: continue
                t_raw = time_tag.get('datetime') or time_tag.text.strip()
                try:
                    t_str = t_raw[:16].replace('T', ' ')
                    if t_str[2] == ':':
                        p = t_str.split(' ')
                        t_str = f"{p[1]} {p[0]}"
                    dt = datetime.strptime(t_str, "%Y-%m-%d %H:%M")
                    if dt >= start_time:
                        url = title_tag['href']
                        if not url.startswith('http'): url = "https://www.chinatimes.com" + url
                        if url not in seen:
                            res.append((dt, title_tag.text.strip(), url))
                            seen.add(url)
                except: continue
        except: continue

    # --- 第四區：生活頻道 (比照政治/言論模式) ---
    print("  - 掃描 [生活頻道]...")
    for page in range(1, 4):
        target = f"https://www.chinatimes.com/life/?chdtv&page={page}"
        try:
            resp = requests.get(f"{GAS_PROXY_URL}?url={target}", timeout=30)
            soup = BeautifulSoup(resp.text, 'html.parser')
            items = soup.select('.article-list .col')
            for art in items:
                title_tag = art.select_one('.title a')
                time_tag = art.select_one('time')
                if not title_tag or not time_tag: continue
                t_raw = time_tag.get('datetime') or time_tag.text.strip()
                try:
                    t_str = t_raw[:16].replace('T', ' ')
                    if t_str[2] == ':':
                        p = t_str.split(' ')
                        t_str = f"{p[1]} {p[0]}"
                    dt = datetime.strptime(t_str, "%Y-%m-%d %H:%M")
                    if dt >= start_time:
                        url = title_tag['href']
                        if not url.startswith('http'): url = "https://www.chinatimes.com" + url
                        if url not in seen:
                            res.append((dt, title_tag.text.strip(), url))
                            seen.add(url)
                except: continue
        except: continue

    # --- 第五區：社會頻道 (比照政治/言論模式) ---
    print("  - 掃描 [社會頻道]...")
    for page in range(1, 4):
        target = f"https://www.chinatimes.com/society/?chdtv&page={page}"
        try:
            resp = requests.get(f"{GAS_PROXY_URL}?url={target}", timeout=30)
            soup = BeautifulSoup(resp.text, 'html.parser')
            items = soup.select('.article-list .col')
            for art in items:
                title_tag = art.select_one('.title a')
                time_tag = art.select_one('time')
                if not title_tag or not time_tag: continue
                t_raw = time_tag.get('datetime') or time_tag.text.strip()
                try:
                    t_str = t_raw[:16].replace('T', ' ')
                    if t_str[2] == ':':
                        p = t_str.split(' ')
                        t_str = f"{p[1]} {p[0]}"
                    dt = datetime.strptime(t_str, "%Y-%m-%d %H:%M")
                    if dt >= start_time:
                        url = title_tag['href']
                        if not url.startswith('http'): url = "https://www.chinatimes.com" + url
                        if url not in seen:
                            res.append((dt, title_tag.text.strip(), url))
                            seen.add(url)
                except: continue
        except: continue

    # --- 第六區：寶島頻道 (比照政治/言論模式) ---
    print("  - 掃描 [寶島頻道]...")
    for page in range(1, 4):
        target = f"https://www.chinatimes.com/taiwan/?chdtv&page={page}"
        try:
            resp = requests.get(f"{GAS_PROXY_URL}?url={target}", timeout=30)
            soup = BeautifulSoup(resp.text, 'html.parser')
            items = soup.select('.article-list .col')
            for art in items:
                title_tag = art.select_one('.title a')
                time_tag = art.select_one('time')
                if not title_tag or not time_tag: continue
                t_raw = time_tag.get('datetime') or time_tag.text.strip()
                try:
                    t_str = t_raw[:16].replace('T', ' ')
                    if t_str[2] == ':':
                        p = t_str.split(' ')
                        t_str = f"{p[1]} {p[0]}"
                    dt = datetime.strptime(t_str, "%Y-%m-%d %H:%M")
                    if dt >= start_time:
                        url = title_tag['href']
                        if not url.startswith('http'): url = "https://www.chinatimes.com" + url
                        if url not in seen:
                            res.append((dt, title_tag.text.strip(), url))
                            seen.add(url)
                except: continue
        except: continue

    res.sort(key=lambda x: x[0], reverse=True)
    return res
    
# 2. 聯合報 (維持您要求的邏輯)
def fetch_udn(start_time):
    res = []; seen = set()
    for p in range(1, 10):
        target = f"https://udn.com/news/breaknews/1/0/{p}"
        try:
            resp = requests.get(f"{GAS_PROXY_URL}?url={target}", timeout=25)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for art in soup.select('.story-list__text'):
                title_tag = art.find('a'); time_tag = art.find('time')
                if title_tag and time_tag:
                    t_str = time_tag.text.strip()
                    if len(t_str) <= 11: t_str = f"{get_now_tw().year}-{t_str}"
                    dt = datetime.strptime(t_str, "%Y-%m-%d %H:%M")
                    if dt >= start_time:
                        url = title_tag['href'] if title_tag['href'].startswith('http') else "https://udn.com"+title_tag['href']
                        if url not in seen:
                            res.append((dt, title_tag.text.strip(), url))
                            seen.add(url)
                    else: return res
        except: break
    return res

# 3. 中央社 (恢復指定之 25 頁深度邏輯)
def fetch_cna(start_time):
    res = []; seen = set()
    headers = {'User-Agent': 'Mozilla/5.0'}
    for p in range(1, 26):
        try:
            resp = requests.get(f"https://www.cna.com.tw/list/aall.aspx?page={p}", headers=headers, timeout=15)
            soup = BeautifulSoup(resp.text, 'html.parser')
            for art in soup.select('#jsMainList li'):
                link_tag = art.select_one('a')
                if link_tag:
                    url = "https://www.cna.com.tw" + link_tag['href']
                    if url in seen: continue
                    t_tag = art.select_one('.date'); title_tag = art.select_one('h2')
                    if t_tag and title_tag:
                        dt = datetime.strptime(t_tag.text.strip().replace('/', '-'), "%Y-%m-%d %H:%M")
                        if dt >= start_time:
                            res.append((dt, title_tag.text.strip(), url)); seen.add(url)
        except: break
    return res

# 4. 自由時報 (維持指定邏輯)
def fetch_ltn(start_time):
    res = []; seen = set()
    for ch in ["all", "politics", "society", "life"]:
        try:
            feed = feedparser.parse(f"https://news.ltn.com.tw/rss/{ch}.xml")
            for e in feed.entries:
                dt = datetime(*(e.published_parsed[0:6])) + timedelta(hours=8)
                if dt >= start_time and e.link not in seen:
                    res.append((dt, e.title, e.link)); seen.add(e.link)
        except: continue
    return res

def send_telegram_file(file_path, caption):
    token = os.getenv("TELEGRAM_TOKEN")
    chat_id = os.getenv("TELEGRAM_CHAT_ID")
    url = f"https://api.telegram.org/bot{token}/sendDocument"
    with open(file_path, "rb") as f:
        requests.post(url, data={"chat_id": chat_id, "caption": caption}, files={"document": f})

def main():
    now_tw = get_now_tw().replace(tzinfo=None)
    fn = now_tw.strftime('%Y%m%d_%H%M')
    last_run_time = get_last_run_time()
    buffer_start_ts = last_run_time - timedelta(minutes=21)
    
    all_data = {
        "中時新聞網": fetch_chinatimes(buffer_start_ts),
        "中央社": fetch_cna(buffer_start_ts),
        "自由時報": fetch_ltn(buffer_start_ts),
        "聯合新聞網": fetch_udn(buffer_start_ts)
    }
    
    total = sum(len(v) for v in all_data.values())

    # --- HTML 樣式：大字體 (套用您提供的模板) ---
    html_content = f"""<html><head><meta charset='utf-8'>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{ font-family: "Microsoft JhengHei", Arial, sans-serif; line-height: 1.4; padding: 10px; color: #111; background-color: #fff; margin: 0; }}
        .container {{ max-width: 800px; margin: auto; }}
        h1 {{ font-size: 28px; text-align: center; margin: 10px 0 5px 0; color: #333; }}
        .start-time {{ text-align: center; font-size: 16px; color: #666; margin-bottom: 15px; }}
        h2 {{ font-size: 24px; background: #eee; padding: 5px 10px; margin: 20px 0 5px 0; border-left: 5px solid #333; }}
        ul {{ list-style: none; padding: 0; margin: 0; }}
        li {{ padding: 12px 0; border-bottom: 1px solid #ddd; display: flex; align-items: baseline; }}
        .time {{ color: #e74c3c; font-size: 20px; font-weight: bold; margin-right: 12px; min-width: 60px; }}
        a {{ text-decoration: none; color: #004a99; font-size: 26px; font-weight: bold; flex: 1; }}
        .footer {{ text-align: center; margin-top: 30px; font-size: 15px; color: #888; padding: 10px; }}
        /* 加入關鍵字橘色樣式 */
        .hl {{ color: orange; font-weight: bold; }}
    </style></head><body><div class="container">
    <h1>新聞摘要 {fn}</h1>
    <div class="start-time">基準時間：{buffer_start_ts.strftime('%Y-%m-%d %H:%M:%S')}</div>"""
    
    # 定義要變橘色的關鍵字清單
    highlight_kws = ["考試院", "試院", "考選部", "銓敘部", "保訓會", "年金改革", "退撫", "年金", "公職", "公務員", "鐵飯碗", "公務人員", "文官", "飛躍方案", "總預算", "程序委員會", "年改", "周弘憲", "劉建忻", "翁曉玲", "李來希", "專技", "植物診療師", "軍公教", "公教", "警消", "警勤", "主計總處", "經濟成長率", "首都加給", "身心調適假", "高考", "普考", "高普考", "特考", "國考", "作弊", "扣考", "考績", "考核", "吃乙", "甲等", "乙等", "人事總處", "人總", "人事長", "新任", "上任", "接任", "出任", "初任", "調任", "具結", "任命", "駐外", "大使", "國情報告", "優先法案", "總召", "科長", "書記官", "警勤", "加給", "加成", "公部門", "李貞秀", "工時", "程委會", "院會", "木柵", "索賄", "貪汙", "回扣", "霸凌", "副署", "身心調適假", "電腦化測驗", "電腦測驗", "律訓", "律師", "員額", "行賄", "收賄", "洩密", "涉貪", "召委", "圖利", "土木", "人事", "同意權", "彈劾", "公務車", "考試", "技師", "分階段", "大地工程", "失業率", "育嬰留停", "育嬰", "育嬰津貼", "津貼", "旋轉門","主秘", "預算", "社工", "職場排擠", "監委", "監院", "監察院", "人口", "軍警", "釋憲", "機關", "貪瀆", "撤職", "代理", "提名", "護病比"]
    
    for media, items in all_data.items():
        html_content += f"<h2>{media} ({len(items)})</h2><ul>"
        if items:
            items.sort(key=lambda x: x[0], reverse=True)
            for dt, title, url in items:
                # --- 新增：處理標題關鍵字高亮 (橘色) ---
                display_title = title
                for kw in highlight_kws:
                    if kw in display_title:
                        # 將關鍵字包覆在帶有 hl 類別的 span 中
                        display_title = display_title.replace(kw, f"<span class='hl'>{kw}</span>")
                
                html_content += f"<li><span class='time'>{dt.strftime('%H:%M')}</span><a href='{url}' target='_blank'>{display_title}</a></li>"
        else:
            html_content += "<li style='color:#ccc; font-size: 20px;'>無更新</li>"
        html_content += "</ul>"
    
    html_content += f"<div class='footer'>區間: {buffer_start_ts.strftime('%H:%M')} ~ {now_tw.strftime('%H:%M')}</div></div></body></html>"
    
    file_path = f"news_{fn}.html"
    with open(file_path, "w", encoding="utf-8") as f: 
        f.write(html_content)
    
    if total > 0: 
        send_telegram_file(file_path, f"📊 共 {total} 則 | 基準 {buffer_start_ts.strftime('%H:%M')}")
        save_current_run_time(now_tw)
    else:
        print("沒有新新聞。")

if __name__ == "__main__":
    main()
