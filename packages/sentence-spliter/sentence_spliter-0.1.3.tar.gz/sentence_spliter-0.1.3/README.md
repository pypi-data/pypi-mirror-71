# sentence-spliter

## 介绍
sentence-spliter 句子切分工具，将一个长的句子，切分为短句的 List 。支持自然切分，最长句切分，最短句合并。



## Features

目前支持：

中文
1. 自然切分，按照句号，感叹号，问号,分号，省略号切分。说话双引号内遇到切分符号不切分；括号内遇到切分符号不切分。
2. 最长句子切分
3. 最短句合并
4. 强制截断

英文

1.自然切分，按照句号，感叹号，问号,分号，省略号切分。




TODO：

英文的切分有例如人名：H.D.Semon 我们现在的切句工具会把句号当做切分符号给切开。



## 项目结构

```

├── README.md
├── app 									# web服务接口
├── bin 									# 命令行工具
├── src 									# 项目的源代码
│   ├── sentence_spliter.py
│   └── spliter.py
└── test 									# 测试代码以及测试数据
    ├── data
    └── test_sentence_spliter.py
```


## Setup

PYPI 安装

```
pip install sentence_spliter
```

本地安装

```
git clone git@git.yy.com:aimodel/nlp/sentence-spliter.git
cd sentence-spliter
python setup.py install
```

## Usage

```python
from sentence_spliter import Spliter

options = {}
spliter = Spliter(options)
paragraph = "“你真漂亮呢！哈哈哈”。“谢谢你啊”。今天很开心！"
cut_sentences =  spliter.cut_to_sentences(paragraph)
print(cut_sentences)

# outputs
['“你真漂亮呢！哈哈哈”。','“谢谢你啊”。','今天很开心！']
```



## Options

```
options = {
  'language': 'zh',  			# 'zh'中文 'en' 英文
  'long_short_sent_handle':'y'  # 'y'自然切分，不处理长短句；'n'处理长短句
  'max_length': 150, 			#  最长句子，默认值150
  'min_length': 15,  			#  最短句子，默认值15
  'hard_max_length': 300        #  强制截断，默认值300
  'remove_blank' : True         #  是否要我删除句子中的空白 
}
```



## Deployment

Docker 部署



pm2 部署(需要安装 `npm install -g pm2`)

```shell
pm2 start ./bin/spliter-service.sh
```



## Web API

```
GET

POST
```







