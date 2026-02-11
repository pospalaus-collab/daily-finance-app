import yfinance as yf
import pandas as pd
from datetime import datetime

def get_market_data():
    # 定义想要监控的标的：美股指数、热门股、加密货币、黄金
    symbols = {
        '^GSPC': '标普500',
        '^IXIC': '纳斯达克',
        'BTC-USD': '比特币',
        'ETH-USD': '以太坊',
        'NVDA': '英伟达',
        'TSLA': '特斯拉',
        'AAPL': '苹果',
        'GC=F': '黄金期货'
    }
    
    report_items = []
    
    for sym, name in symbols.items():
        try:
            ticker = yf.Ticker(sym)
            hist = ticker.history(period='2d')
            if len(hist) < 2: continue
            
            # 计算涨跌幅
            prev_close = hist['Close'].iloc[-2]
            curr_close = hist['Close'].iloc[-1]
            change_pct = ((curr_close - prev_close) / prev_close) * 100
            
            status = "🚀" if change_pct > 3 else "🔻" if change_pct < -3 else "平静"
            
            report_items.append({
                'name': name,
                'price': round(curr_close, 2),
                'change': round(change_pct, 2),
                'status': status
            })
        except Exception as e:
            print(f"获取 {name} 出错: {e}")
            
    return report_items

def generate_html(items):
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 找出大变动的项目
    movers = [i for i in items if i['status'] != "平静"]
    movers_html = ""
    for m in movers:
        color = "text-green-500" if m['change'] > 0 else "text-red-500"
        movers_html += f"""
        <div class="p-4 bg-gray-800 rounded-xl mb-3 border-l-4 border-yellow-500">
            <div class="flex justify-between items-center">
                <span class="text-lg font-bold text-white">{m['name']}</span>
                <span class="{color} font-mono font-bold">{m['change']}% {m['status']}</span>
            </div>
            <p class="text-gray-400 text-sm">当前价格: ${m['price']}</p>
        </div>
        """

    # 生成完整 HTML
    html_template = f"""
    <!DOCTYPE html>
    <html lang="zh">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>AI 金融早报</title>
        <link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/2488/2488654.png">
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body {{ background-color: #111827; }}
        </style>
    </head>
    <body class="p-4 text-gray-200">
        <div class="max-w-md mx-auto">
            <header class="mb-8 mt-4 text-center">
                <h1 class="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-yellow-400 to-orange-500">AI 金融异动助手</h1>
                <p class="text-gray-500 mt-2">更新时间: {now}</p>
            </header>

            <section class="mb-6">
                <h2 class="text-xl font-semibold mb-4 flex items-center">
                    <span class="mr-2">🔥</span> 今日异动榜
                </h2>
                {movers_html if movers_html else '<p class="text-gray-500 italic">今日市场暂无剧烈波动</p>'}
            </section>

            <section>
                <h2 class="text-xl font-semibold mb-4">📊 核心观测站</h2>
                <div class="grid grid-cols-2 gap-3">
                    {"".join([f'<div class="bg-gray-800 p-3 rounded-lg text-sm border border-gray-700"><b>{i["name"]}</b><br/><span class="{"text-green-400" if i["change"]>0 else "text-red-400"}">{i["change"]}%</span></div>' for i in items])}
                </div>
            </section>
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_template)

if __name__ == "__main__":
    data = get_market_data()
    generate_html(data)
