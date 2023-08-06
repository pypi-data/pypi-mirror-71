# [SmoothNLP](http://www.smoothnlp.com)
![Version](https://img.shields.io/badge/Version-0.4-green.svg) ![Python3](https://img.shields.io/badge/Python-3-blue.svg?style=flat) [![star this repo](http://githubbadges.com/star.svg?user=smoothnlp&repo=SmoothNLP)](https://github.com/smoothnlp/SmoothNLP/stargazers) [![fork this repo](http://githubbadges.com/fork.svg?user=smoothnlp&repo=SmoothNLP&color=fff&background=007ec6)](http://github.com/smoothnlp/SmoothNLP/fork)
****	

| Author | Email | 
| ----- | ------ | 
| Victor | zhangruinan@smoothnlp.com |
| Yinjun | yinjun@smoothnlp.com |
| 海蜇 | yuzhe_wang@smoothnlp.com | 

****


<!-- TOC -->

- [SmoothNLP](#smoothnlp)
    - [Install 安装](#install-安装)
    - [知识图谱](#知识图谱)
        - [调用示例&可视化](#调用示例可视化)
    - [NLP基础Pipelines](#nlp基础pipelines)
        - [1. Tokenize分词](#1-tokenize分词)
        - [2. Postag词性标注](#2-postag词性标注)
        - [3. NER 实体识别](#3-ner-实体识别)
        - [4. 金融实体识别](#4-金融实体识别)
        - [5. 依存句法分析](#5-依存句法分析)
        - [6. 切句](#6-切句)
        - [7. 多线程支持](#7-多线程支持)
        - [8. 日志](#8-日志)
    - [无监督学习](#无监督学习)
        - [新词挖掘](#新词挖掘)
        - [事件聚类](#事件聚类)
    - [有监督学习](#有监督学习)
        - [(资讯)事件分类](#资讯事件分类)
    - [Tutorial](#tutorial)
    - [服务说明](#服务说明)
        - [声明](#声明)
        - [Pro 专业版本](#pro-专业版本)
        - [常见问题](#常见问题)
    - [设置字体](#设置字体)
    - [彩蛋](#彩蛋)

<!-- /TOC -->


## Install 安装
通过`pip`安装
```shell
pip install smoothnlp>=0.4.0
```

通过源代码安装最新版本
```shell
git clone https://github.com/smoothnlp/SmoothNLP.git
cd SmoothNLP
python setup.py install
```


## 知识图谱
> 仅支持SmoothNLP `V0.3.0`以后的版本; 以下展示为`V0.4`版本后样例:

### 调用示例&可视化

```python
from smoothnlp.algorithm import kg
from kgexplore import visual
ngrams = kg.extract_ngram(["SmoothNLP在V0.3版本中正式推出知识抽取功能",
                            "SmoothNLP专注于可解释的NLP技术",
                            "SmoothNLP支持Python与Java",
                            "SmoothNLP将帮助工业界与学术界更加高效的构建知识图谱",
                            "SmoothNLP是上海文磨网络科技公司的开源项目",
                            "SmoothNLP在V0.4版本中推出对图谱节点的分类功能",
                            "KGExplore是SmoothNLP的一个子项目"])
visual.visualize(ngrams,width=12,height=10)
```

![SmoothNLP_KG_Demo](/tutorials/知识图谱/0.4demo.png)


> 功能说明
* V0.4版本中支持的边关系(edge-type), 包括: `事件触发`, `状态描述`, `属性描述`, `数值描述`. 
* V0.4版本中支持的节点种类(node-type), 包括:  `产品`、`地区`、`公司与品牌`、`货品`、`机构`、`人物`、`修饰短语`、`其他`. 

 ---------

## NLP基础Pipelines

### 1.Tokenize分词
```python
>> import smoothnlp 
>> smoothnlp.segment('欢迎在Python中使用SmoothNLP')
['欢迎', '在', 'Python', '中', '使用', 'SmoothNLP']
```

### 2.Postag词性标注

[词性标注标签解释wiki](https://github.com/smoothnlp/SmoothNLP/wiki/%E8%AF%8D%E6%80%A7%E6%A0%87%E6%B3%A8%E8%A7%A3%E9%87%8A%E6%96%87%E6%A1%A3)

```python
>> smoothnlp.postag('欢迎使用smoothnlp的Python接口')
[{'token': '欢迎', 'postag': 'VV'},
 {'token': '在', 'postag': 'P'},
 {'token': 'Python', 'postag': 'NN'},
 {'token': '中', 'postag': 'LC'},
 {'token': '使用', 'postag': 'VV'},
 {'token': 'SmoothNLP', 'postag': 'NN'}]
```


### 3.NER 实体识别
```python
>> smoothnlp.ner("中国平安2019年度长期服务计划于2019年5月7日至5月14日通过二级市场完成购股" )
[{'charStart': 0, 'charEnd': 4, 'text': '中国平安', 'nerTag': 'COMPANY_NAME', 'sTokenList': {'1': {'token': '中国平安', 'postag': None}}, 'normalizedEntityValue': '中国平安'},
{'charStart': 4, 'charEnd': 9, 'text': '2019年', 'nerTag': 'NUMBER', 'sTokenList': {'2': {'token': '2019年', 'postag': 'CD'}}, 'normalizedEntityValue': '2019年'},
{'charStart': 17, 'charEnd': 26, 'text': '2019年5月7日', 'nerTag': 'DATETIME', 'sTokenList': {'8': {'token': '2019年5月', 'postag': None}, '9': {'token': '7日', 'postag': None}}, 'normalizedEntityValue': '2019年5月7日'},
{'charStart': 27, 'charEnd': 32, 'text': '5月14日', 'nerTag': 'DATETIME', 'sTokenList': {'11': {'token': '5月', 'postag': None}, '12': {'token': '14日', 'postag': None}}, 'normalizedEntityValue': '5月14日'}]
```


### 4. 金融实体识别
```python
>> smoothnlp.company_recognize("旷视科技预计将在今年9月在港IPO")
[{'charStart': 0,
  'charEnd': 4,
  'text': '旷视科技',
  'nerTag': 'COMPANY_NAME',
  'sTokenList': {'1': {'token': '旷视科技', 'postag': None}},
  'normalizedEntityValue': '旷视科技'}]
```


### 5. 依存句法分析
> 注意, `smoothnlp.dep_parsing`返回的`Index=0` 为 dummy的`root`token.

[依存句法分析标签解释wiki](https://github.com/smoothnlp/SmoothNLP/wiki/%E4%BE%9D%E5%AD%98%E5%8F%A5%E6%B3%95%E5%88%86%E6%9E%90%E8%A7%A3%E9%87%8A%E6%96%87%E6%A1%A3)

```python
smoothnlp.dep_parsing("特斯拉是全球最大的电动汽车制造商。")
> [{'relationship': 'top', 'dependentIndex': 2, 'targetIndex': 1},
  {'relationship': 'root', 'dependentIndex': 0, 'targetIndex': 2},
  {'relationship': 'dep', 'dependentIndex': 5, 'targetIndex': 3},
  {'relationship': 'advmod', 'dependentIndex': 5, 'targetIndex': 4},
  {'relationship': 'ccomp', 'dependentIndex': 2, 'targetIndex': 5},
  {'relationship': 'cpm', 'dependentIndex': 5, 'targetIndex': 6},
  {'relationship': 'amod', 'dependentIndex': 8, 'targetIndex': 7},
  {'relationship': 'attr', 'dependentIndex': 2, 'targetIndex': 8},
  {'relationship': 'attr', 'dependentIndex': 2, 'targetIndex': 9},
  {'relationship': 'punct', 'dependentIndex': 2, 'targetIndex': 10}]
```

### 6. 切句
```python
smoothnlp.split2sentences("句子1!句子2!")
> ['句子1!', '句子2!']
```

### 7. 多线程支持
> SmoothNLP 默认使用2个Thread进行服务调用; 
```python
from smoothnlp import config
config.setNumThreads(2)
```

### 8. 日志
```python
from smoothnlp import config
config.setLogLevel("DEBUG")  ## 设定日志级别
```

-----

## 无监督学习
### 新词挖掘
[算法介绍](https://zhuanlan.zhihu.com/p/80385615) | [使用说明](https://github.com/smoothnlp/SmoothNLP/tree/master/tutorials/%E6%96%B0%E8%AF%8D%E5%8F%91%E7%8E%B0)

### 事件聚类
该功能我们目前仅支持商业化的解决方案支持, 与线上服务. 详情可联系  business@smoothnlp.com

**效果演示**
```json
[
  {
    "url": "https://36kr.com/p/5167309",
    "title": "Facebook第三次数据泄露，可能导致680万用户私人照片泄露",
    "pub_ts": 1544832000
  },
  {
    "url": "https://www.pencilnews.cn/p/24038.html",
    "title": "热点 | Facebook将因为泄露700万用户个人照片 面临16亿美元罚款",
    "pub_ts": 1544832000
  },
  {
    "url": "https://finance.sina.com.cn/stock/usstock/c/2018-12-15/doc-ihmutuec9334184.shtml",
    "title": "Facebook再曝新数据泄露 6800万用户或受影响",
    "pub_ts": 1544844120
  }
]
```
> 吐槽: 新浪小编数据错误... 夸大事实, 真实情况Facebook并没有泄露6800万张照片

## 有监督学习
### (资讯)事件分类
该功能我们目前仅支持商业化的解决方案支持, 与线上服务. 详情可联系  business@smoothnlp.com; 线上服务支持[API输出]()

**效果**

| 事件名称 | AUC | Precision|
| --- | -- | -- |
| 投资并购 | 0.996 |0.982|
| 企业合作 | 0.977 |0.885|
| 董监高管 | 0.982 |0.940|
| 营收报导 | 0.994 |0.960|
| 企业签约 | 0.993 |0.904|
| 商业拓展 | 0.968 |0.869|
| 产品报道 | 0.977 |0.911|
| 产业政策 | 0.990 |0.879|
| 经营不善 | 0.981 |0.765|
| 违规约谈 | 0.951 |0.890|

-------

参考文献
* [ASER](https://arxiv.org/abs/1905.00270)
* [HanLP](https://github.com/hankcs/hanlp)

----------

## Tutorial
- [多线程调用](tutorials/多进程调用/SmoothNLP多线程调用Demo.ipynb)


## 服务说明

### 声明
1. SmoothNLP通过**云端微服务**提供完整的REST文本解析及相关服务应用. 对于开源爱好者等一般用户, 目前我们提供qps<=5的服务支持; 对于商业用户, 我们提供部不受限制的云端账号或本地部署方案. 
2. 包括:切词,词性标注,依存句法分析等基础NLP任务由java代码实现, 在文件夹`smoothnlp_maven`下. 可通过 `maven`编译打包
3. 如果您寻求商业化的NLP或知识图谱解决方案, 欢迎邮件至 business@smoothnlp.com

### Pro 专业版本
SmoothNLP Pro 支持稳定可靠的企业级用户, [使用文档](https://github.com/smoothnlp/SmoothNLP/tree/master/tutorials/Pro%E4%B8%93%E4%B8%9A%E7%89%88); 如需试用或购买, 请联系 contact@smoothnlp.com


### 常见问题
1.  注意, 在0.2.20版本调整后, 以下基础Pipeline功能仅对字符串长度做出了限制(不超过200). 如对较长corpus进行处理, 请先试用`smoothnlp.split2sentences` 进行切句预处理
2. 知识图谱可视化部分(V0.4版本以前)默认支持字体`SimHei`,大多数环境下的matplotlib不支持中文字体, 我们提供字体包的[下载链接](http://storm.cloud.smoothnlp.com/s/HHM6KkmPymie4RA); 您可以通过运行以下代码, 将`Simhei`字体加载入matplotlib字体库

```python
import matplotlib.pyplot as plt
import matplotlib.font_manager as font_manager
## 设置字体
font_dirs = ['simhei/']
font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
font_list = font_manager.createFontList(font_files)
font_manager.fontManager.ttflist.extend(font_list)
plt.rcParams['font.family'] = "SimHei"
```

## 彩蛋
1. 如果你对本项目, 有任何建议或者想成为联合开发者, 欢迎提交issue或pull request; 作为回赠, 我们会提供数据分享或 [kgexplore](https://github.com/smoothnlp/KGExplore) 的免费数据体验
2. 如果你对NLP相关算法或引用场景感兴趣, 但是却缺少实现数据, 我们提供免费的数据支持, [下载](https://github.com/smoothnlp/FinancialDatasets). 
3. 如果你是高校学生, 寻求`NLP`或`知识图谱`相关的研究素材, 甚至是实习机会. 欢迎邮件到 contact@smoothnlp.com







