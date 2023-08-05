# 国税总局发票查验平台验证码获取与识别


## 使用指北

1. ```pip install invoice-captcha```

2. 调用示例：

    ```python
    import requests
    from invoice_captcha.utils import get_captcha_params, parse_captcha_resp, kill_captcha_fast, ua
    
    CAPTCHA_URL = "https://fpcy.guangdong.chinatax.gov.cn/NWebQuery/yzmQuery"
    
    
    # 发票代码
    key1 = "011111111111"
    # 发票号码
    key2 = "11111111"
    
    # # 开票日期
    # key3 = "20200603"
    # # 校验码或发票金额
    # key4 = "000000"
    
    
    def fetch_captcha(invoice_code, invoice_no):
    
        sess = requests.Session()
    
        # 使用代理，需要自备代理
        # sess.proxies = proxy
        sess.headers = {"User-Agent": ua.random}
    
        # 获取验证码请求参数
        payload = get_captcha_params(
            invoice_code=invoice_code, invoice_no=invoice_no
        )
    
        # 通过官网获取验证码
        r = sess.get(CAPTCHA_URL, params=payload)
    
        # 验证码请求参数解密
        plain_dict = parse_captcha_resp(r)
    
        # 验证码请求返回明文
        # key1 图片base64
        # key4 验证码需要识别的颜色代码
        print("解密参数 --- ", plain_dict)
    
        # 调用识别测试接口
        captcha_text = kill_captcha_fast(
            plain_dict, 
          	# 默认API有使用次数限制，可联系作者QQ：27009583，测试独立接口
            # api="http://kerlomz-ac86u.asuscomm.com:19811/captcha/v1"
        )
    
        # 输出识别结果
        print("识别结果 --- ", captcha_text)
        
        
    if __name__ == '__main__':
        for i in range(10):
            fetch_captcha(key1, key2)
    ```



**输出结果:**

```shell script
解密参数 ---  {'key1': 'iVBORw0KGgoA...5ErkJggg==', 'key2': '2020-06-16 16:56:36', 'key3': '9636e07df9aae6bd0483c5f6ea1ecbdc', 'key4': '03', 'key5': '2'}
识别结果 ---  xm8
解密参数 ---  {'key1': 'iVBORw0KGgoA...UVORK5CYII=', 'key2': '2020-06-16 16:56:42', 'key3': 'd202f846119faa08a0e95eec48ca1bfe', 'key4': '01', 'key5': '2'}
识别结果 ---  命初
```



