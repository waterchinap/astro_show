import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import pandas as pd
    import akshare as ak
    from pathlib import Path
    import logging
    from playwright.sync_api import sync_playwright
    import json
    from datetime import datetime

    return Path, ak, datetime, json, logging, sync_playwright


@app.cell
def _(logging):
    logger = logging.getLogger(__name__)
    return (logger,)


@app.cell
def _(Path, datetime):
    backend_dir = Path(__file__).parent
    project_dir = backend_dir.parent
    front_ppts = project_dir / 'src' / 'ppts'
    today_str = datetime.today().strftime("%Y-%m-%d")
    return front_ppts, today_str


@app.function
def make_cover(title: str, subtitle: str | None = None):
    cover = [{
        "template": "Cover",
        "slide": {
            "title": title, "subtitle": subtitle
        }
    }]
    return cover


@app.cell
def _(Path, ak, json, logger):
    TITLE_COL = "标题"
    CONTENT_COL = "发布时间"   # ['标题', '摘要', '发布时间', '链接']


    def get_emnews(fn: Path, limit: int | None = None) -> list[dict]:
        """抓取东方财富即时信息，生成 TitleContent 幻灯片并写入 json 文件。"""
        emnews = ak.stock_info_global_em()
        if emnews.empty:
            logger.warning("stock_info_global_em 返回空数据")
            return []

        # 按列名取值，避免依赖列顺序
        news = (
            emnews[[TITLE_COL, CONTENT_COL]]
            .rename(columns={TITLE_COL: "title", CONTENT_COL: "content"})
            .dropna()
        )
        if limit:
            news = news.head(limit)

        def make_deck(title: str, content: str) -> dict:
            return {
                "template": "TitleContent",
                "slide": {"title": title, "content": content},
            }

        # 封面
        first = news.iloc[0]
        cover = make_deck("东方财富即时信息", first["content"])

        # 内容页（跳过封面已用的第一条，或按业务需要保留）
        body = [
            make_deck(row.title, row.content)
            for row in news.itertuples(index=False)
        ]

        decks = [cover, *body]
        emnews_json = {"config": {"autoSlide": 6000}, "decks": decks}

        fn.parent.mkdir(parents=True, exist_ok=True)
        with fn.open("w", encoding="utf-8") as f:
            json.dump(emnews_json, f, ensure_ascii=False, indent=4)

        logger.info("%s saved! (%d decks)", fn, len(decks))
        return decks

    return


@app.cell
def _(Path, imgur, json, logger, sync_playwright, today_str):
    def get_doc_arr(fn: Path):
        url = "https://channel.chinanews.com.cn/u/pic/news.shtml"

        with sync_playwright() as p:

            def make_img_deck(title: str, imgurl: str) -> dict:
                return {
                    "template": "ImgTitle",
                    "slide": {"title": title, "backgroudImage": imgur, "subtitle": "  "},
                }
            # 1. 启动 Chromium 浏览器 (无头模式，不显示浏览器窗口)
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()

            logger.info(f"正在访问 {url} ...")
            # 2. 访问页面
            page.goto(url)

            # 3. 等待页面加载完成，确保 JS 已执行
            # wait_for_load_state('networkidle') 会等待网络请求基本静止，比较稳妥
            page.wait_for_load_state("networkidle")
            logger.info("页面加载完成。")

            # 4. 在浏览器上下文中执行 JS，直接获取全局变量 docArr
            # 这是最准确的方法，相当于在浏览器控制台输入 `docArr`
            try:
                doc_arr = page.evaluate("() => window.docArr")

                if doc_arr:
                    logger.info(f"成功提取！共获取到 {len(doc_arr)} 条新闻。")
                    logger.info("-" * 30)
                    res = make_cover('中新社图片新闻', today_str)  + [make_img_deck(d.get('title'), d.get('img')) for d in doc_arr]
                    with open(fn, "w", encoding="utf-8") as f:
                        json.dump(res, f, ensure_ascii=False, indent=2)
                    # 打印第一条新闻的标题作为验证
                    logger.info("第一条新闻标题:", doc_arr[0]["title"])
                    logger.info("发布时间:", doc_arr[0]["pubtime"])
                    return res
                else:
                    logger.info("错误：在页面中未找到 'docArr' 变量。")
                    # 为了调试，我们可以打印出页面标题，确认是否访问了正确的页面
                    logger.info("当前页面标题为:", page.title())
                    return None
            except Exception as e:
                logger.info("执行 JavaScript 时出错:", e)
                return None
            finally:
                # 5. 关闭浏览器
                browser.close()

    return (get_doc_arr,)


@app.cell
def _(front_ppts, get_doc_arr):
    if __name__ == "__main__":
        get_doc_arr(front_ppts / 'imgnews.json')
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
