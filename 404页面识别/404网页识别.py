# coding:utf-8
import requests
requests.packages.urllib3.disable_warnings()
import difflib
Dir_Path = ['/blog/','/admin', '/login', '/manage', '/log_home', '/admin.php', '/categories/']
Black_Con = ['404 Not Found','403 Forbidden',' 秒后跳转至','页面不存在','页面没有找到','检查您输入的网址是否正确']
def Return_Http_Content(url):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
        r = requests.get(url, headers=headers, verify=False, timeout=5)
        encoding = 'utf-8'
        try:
            encoding = requests.utils.get_encodings_from_content(r.text)[0]
        except:
            pass
        content = r.content.decode(encoding, 'replace')
        for b in Black_Con:
            if b in content:
                print('页面中存在错误信息关键词')
                return ('langzi', 404)
        return (content, r.status_code)
    except Exception as e:
        return ('langzi', 404)

def Return_Content_Difflib(original, compare):
    res = (str(difflib.SequenceMatcher(None, original, compare).quick_ratio())[2:6])
    if res == '0':
        res = 0
        return res
    else:
        res = res.lstrip('0')
        return int(res)
    # return 4 integer like 1293 or 9218

class Check_Page_404:
    def __new__(cls, url):
        cls.url_200 = Return_Http_Content(url)
        cls.url_404 = Return_Http_Content(url.rstrip('/') + '/langzi.html')
        return object.__new__(cls)

    def __init__(self, url):
        self.url = url

    def Check_404(self, suffix):
        chekc_url = Return_Http_Content(self.url.rstrip('/') + suffix)
        if chekc_url[1] == 404:
            return False
        Dif_1 = Return_Content_Difflib(chekc_url[0], self.url_200[0])
        Dif_2 = Return_Content_Difflib(chekc_url[0], self.url_404[0])
        print(Dif_1,Dif_2)
        if Dif_1 > 6000 and Dif_2 < 8000:
            # 注意这里是最重要的调参
            # 判断是否为错误页面主要取决与这个调整至
            # 调整范围为1-10000
            # 按照不同页面调试出最优的参数
            return True
        else:
            return False


if __name__ == '__main__':
    url = 'https://www.taobao.com'
    test = Check_Page_404(url.strip('/'))
    for suffix in Dir_Path:
        print('Check Url : ' + url.strip('/') + suffix)
        print(test.Check_404(suffix=suffix))