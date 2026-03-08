from DrissionPage import Chromium
import json
import time
import os
from typing import List, Dict, Optional

BASE_URL = "https://chart.tencentmusic.com/unichartsapi/pc/yobang/history"
PAGE_SIZE = 10
STATICS_DIR = os.path.join(os.path.dirname(__file__), "statics")

class DataFetcher:
    """通过 API 接口分页获取指定期数的榜单数据"""

    def __init__(self, tab):
        self.tab = tab
        self.tab.change_mode("s")
        self.headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://chart.tencentmusic.com/uni-chart?issue=202551',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0'
        }

    def get_single_issue(self, issue: str) -> List[Dict]:
        """获取单个期刊所有数据"""
        print(f">>> 正在抓取期刊: {issue}")

        # 第一页：获取总数和第一批数据
        url = f"{BASE_URL}?issue={issue}&offset=0&limit={PAGE_SIZE}&platform=pc"
        self.tab.get(url, headers=self.headers)
        res = self.tab.response.json()
        
        data_block = res.get("data", {})
        total = data_block.get("page", {}).get("total", 0)
        songs = data_block.get("content", {}).get("chartsList", []) or []

        # 继续拉取剩余页
        for offset in range(PAGE_SIZE, total, PAGE_SIZE):
            url = f"{BASE_URL}?issue={issue}&offset={offset}&limit={PAGE_SIZE}&platform=pc"
            self.tab.get(url, headers=self.headers)
            page_data = self.tab.response.json()
            
            batch = page_data.get("data", {}).get("content", {}).get("chartsList", [])
            songs.extend(batch)

        print(f"--- 期刊 {issue} 抓取完成，共 {len(songs)} 条数据")
        return songs

    def get_years(self) -> List[str]:
        """获取所有年份"""
        print(">>> 正在获取年份列表...")
        url = "https://chart.tencentmusic.com/unichartsapi/pc/yobang/year"
        self.tab.get(url, headers=self.headers)
        res = self.tab.response.json()
        
        if res.get("code") == "0":
            years = res.get("data", {}).get("years", [])
            print(f"--- 已获取 {len(years)} 个年份")
            return years
        else:
            print(f"!!! 获取年份失败: {res}")
            return []

    def get_all_issue(self, year: str) -> List[Dict]:
        """获取指定年份的所有期刊列表"""
        print(f">>> 正在获取 {year} 年的期刊列表...")
        url = f"https://chart.tencentmusic.com/unichartsapi/pc/yobang/scope?year={year}&sort=desc"
        self.tab.get(url, headers=self.headers)
        res = self.tab.response.json()
        
        if res.get("code") == "0":
            scope_infos = res.get("data", {}).get("scopeInfos", [])
            print(f"--- {year} 年共发现 {len(scope_infos)} 个期刊")
            return scope_infos
        else:
            print(f"!!! 获取 {year} 年期刊失败: {res}")
            return []

    def get_all(self):
        """获取所有数据"""

        print("=== 开始全量抓取流程===")
        years = self.get_years()
        if not years:
            return

        # 1. 保存所有年份数据
        save_json(years, "years_data.json")

        all_years_issues = {} # 对应 years_issue_data
        result_data = {}      # 对应 result_data

        target_years = years[1:] # 测试用，取部分年份
        
        for year in target_years:
            scope_infos = self.get_all_issue(year)
            if not scope_infos:
                continue

            # 收集年份对应的期刊信息
            all_years_issues[year] = scope_infos
            result_data[year] = {}

            # 提取期刊号进行抓取
            issues = [item.get("issue") for item in scope_infos if item.get("issue")]
            target_issues = issues # 测试用，取全部期刊或切片
            
            for issue in target_issues:
                songs = self.get_single_issue(issue)
                if songs:
                    result_data[year][issue] = songs
                time.sleep(2)

        # 2. 保存所有年份和对应的所有期刊数据
        if all_years_issues:
            save_json(all_years_issues, "years_issue_data.json")

        # 3. 保存汇总数据
        if result_data:
            save_json(result_data, "result_data.json")
            print("=== 全量抓取完成 ===")
        else:
            print("!!! 未获取到任何数据")

    def get_latest_rank(self) -> Optional[List[Dict]]:
        """获取当日最新排行榜数据"""
        print(">>> 正在获取最新排行榜数据...")

        url = "https://yobang.tencentmusic.com/unichartsapi/yobang/daily/chart?page=1&pageSize=200"
        headers = {
            'accept': '*/*',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
            'cache-control': 'no-cache',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://yobang.tencentmusic.com/chart/uni-chart/rankList/?chartType=daily',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/133.0.0.0'
        }

        self.tab.get(url, headers=headers)
        res = self.tab.response.json()

        if res.get("code") == "0":
            data = res.get("data", {}).get("data", [])
            if data:
                save_json(data, "latest_data.json")
                print(f"--- 最新排行榜数据获取完成，共 {len(data)} 条")
                return data
            else:
                print("!!! 响应数据为空")
                return None
        else:
            print(f"!!! 获取最新排行榜失败: {res}")
            return None



# ── 工具函数 ───────────────────────────────────────────────────

def save_json(data, filename="tencent_music_data.json"):
    if not os.path.exists(STATICS_DIR):
        os.makedirs(STATICS_DIR)
    
    filepath = os.path.join(STATICS_DIR, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"数据已保存至: {filepath}")


# ── 启动函数 ───────────────────────────────────────────────────

def run_fetcher(tab):
    """接口拉取：手动输入期数，直接调用 API 获取数据"""
    fetcher  = DataFetcher(tab)
    fetcher.get_all() # 直接调用 get_all 进行测试



# ── 入口 ───────────────────────────────────────────────────────

def main():
    browser = Chromium()
    tab = browser.latest_tab
    tab.get("https://chart.tencentmusic.com/uni-chart")
    tab.wait(3)

    try:
        run_fetcher(tab)       # 模式一：指定期数，接口拉取
    except Exception as e:
        import traceback
        print(f"\n程序异常: {e}")
        traceback.print_exc()
    finally:
        browser.quit()
        print("浏览器已关闭")


if __name__ == "__main__":
    main()
