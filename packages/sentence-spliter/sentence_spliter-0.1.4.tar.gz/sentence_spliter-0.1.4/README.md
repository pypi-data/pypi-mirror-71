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

1.自然切分，按照句号，感叹号，问号,分号，省略号切分。英文没有处理长短句.




TODO：

英文的切分有例如人名：H.D.Semon 我们现在的切句工具会把句号当做切分符号给切开。



## 项目结构

```
.
├── app                                    # web服务接口
├── bin                                    # 命令行工具
├── LICENSE.txt
├── README.md
├── requirements.txt
├── sentence_spliter                        # 项目的源代码
│   ├── spliter_sentence.py
│   ├── spliter_simple.py
│   └── time_it.py
├── setup.py
└── test                                    # 测试代码以及测试数据
    ├── data
    ├── __init__.py
    ├── test_ntnc_spliter_speed.py
    ├── test_spliter_sentence.py
    ├── test_spliter_simple.py
    └── test_split.py

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
case 1:不输入任何参数,使用默认参数

from sentence_spliter import split
sentence = '锄禾日当午,汗滴禾下土.谁知盘中餐,粒粒皆辛苦.'
out = split(sentence)

# outputs
['锄禾日当午,汗滴禾下土.','谁知盘中餐,粒粒皆辛苦.']

case 2:输入你自己的参数

from sentence_spliter import Spliter
options = {'language': 'zh',  # 'zh' chinese, 'en' english
           'long_short_sent_handle': True,  # False自然切分，不处理长短句；True处理长短句
            'max_length': 15,  # 最长句子，默认值150
            'min_length': 4,  # 最短句子，默认值15
            'hard_max_length': 20,  # 强制截断，默认值300
            'remove_blank': True  # 是否要我删除句子中的空白}
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
  'long_short_sent_handle':'True'  # 'False'自然切分，不处理长短句；'True'处理长短句
  'max_length': 150, 			#  最长句子，默认值150
  'min_length': 15,  			#  最短句子，默认值15
  'hard_max_length': 300        #  强制截断，默认值300
  'remove_blank' : 'True'        #  是否要我删除句子中的空白,英文不能删除. 
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







