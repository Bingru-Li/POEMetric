# Showcase
<img width="7350" height="2469" alt="showcase-deepseek-r1" src="https://github.com/user-attachments/assets/d9246c6f-3f6a-479e-855d-3e930acde819" />
<p align="center">
  DeepSeek-R1 vs. Human
</p>

# The Evaluation Metrics

<img width="5639" height="1725" alt="evaluation_metrics" src="https://github.com/user-attachments/assets/eadf657f-0608-414c-b550-483c89d601ce" />

We propose 10 dimensions of evaluation for poetry generation, including 1) basic instruction-following abilities in generating poems according to a certain form and theme, 2) advanced abilities such as creativity, lexical diversity, and idiosyncrasy, evoking emotional resonance, and using imagery and literary devices, and 3) general appraisal of the overall poem quality and estimation of authorship. To make the framework more robust, we triangulate LLM-as-a-judge with rule-based algorithm evaluation (codes released in 'POEMetric_rule_based_algorithm.py') and human expert judgments.

# The Human Poem Dataset
<img width="5337" height="2164" alt="dataset" src="https://github.com/user-attachments/assets/b65a22e7-bee3-4662-a052-f191939ed513" />
We collected and screened the poems from two online databases, the Poetry Foundation and the Academy of American Poets, and released the public-domain poems in 'POEMetric_human_poems_annotated.csv'.

# Results
![basic](https://github.com/user-attachments/assets/edad6815-ccdf-4dbf-a15a-20e4e11ba5b3)
![radar](https://github.com/user-attachments/assets/9ec84b83-9d3a-4b08-a5ba-25b95f4c8625)
![overall](https://github.com/user-attachments/assets/abb9bdf6-b343-4de8-b472-84d20777db6d)
![all_models](https://github.com/user-attachments/assets/9072a312-574b-49bd-bb4f-ddc76bb0d6b3)



# Citation
```python
@inproceedings{
li2026poemetric,
title={{POEM}etric: The Last Stanza of Humanity},
author={Bingru Li and Han Wang and Hazel Wilkinson},
booktitle={The Fourteenth International Conference on Learning Representations},
year={2026},
url={https://openreview.net/forum?id=9VkJ058cTa}
}
```
# To be continued...
## How about LLMs' abilities of writing Chinese ancient poems?

We did a few experiments...

### 破阵子·癸卯中秋

by DeepSeek-R1

桂魄初盈碧落，清光已透帘栊。

一室烛花摇寂影，半窗霜色锁孤鸿。云河几万重。

玉镜何曾长缺，人间偏易西东。

小字红笺封复启，深杯绿蚁满还空。清辉不与同。


### 如梦令·春尽

by DeepSeek-R1

谢尽荼蘼春瘦，散乱杨花风骤。

空馆又经年，冷烛倦窥笺旧。

知否，知否？身是雨中残柳。


### 临江仙·咏寒柳

by DeepSeek-R1

曾记西风摇落处，江潭老柳作愁颦。杨花满路似积云。可怜枝上月，空照白头人。

而今剩有伤心色，青娥减尽腰身。哪堪飞雪更纷纷。凄凉别后梦，憔悴病中春。

Aren't they amazing? Follow our future work if you're interested!🤩
