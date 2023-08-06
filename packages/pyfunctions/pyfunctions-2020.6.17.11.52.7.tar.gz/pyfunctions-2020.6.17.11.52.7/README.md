# pyfunctions
常用函数的封装,包括不限于python爬虫的请求、解析等



## Installation

You can get `pyfunctions` via pip:
```
pip install pyfunctions
```

Clone the source to get the latest version:
```bash
$ git clone https://github.com/broholens/pyfunctions.git
$ pip install -r requirements.txt
```

## QuickStart
  ```python
  from pyfunctions import fun
  text = fun.url2text('http://www.mogojob.com/')
  ``` 
  ```bash
  >>> '首页 职位大厅 招聘企业 猎头服务 商务服务 我要招人\n\n企业入口  个人登录\n\n\n\n全国 	北京 上海 西安 广州 杭州 深圳 成都 重庆 武汉 南京 天津         ...  
      客服工作时间 : 周一至周五 09:00 - 18:00\n\n投递信息 我的简历 退出系统\n\n'
  ```
  
## 开发小记
1. 发布包使用[setup.py][1],修改内容后执行`python setup.py upload`
2. 发布包遇到错误: [bdist_wheel报错][2]
3. 首次发布失败(包名重复),更正后再次执行遭遇`tag already exists`,需要删除tag. `git tag -d v2018.5.24`
4. `pipreqs`自动生成项目`requirements.txt`: `pipreqs . --encoding=utf8`
5. `response._content`获取图片内容

[1]: https://github.com/kennethreitz/setup.py
[2]: https://yq.aliyun.com/articles/644640