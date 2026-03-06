# Abstract

Large Language Models (LLMs) can compose poetry, but how far are they from human poets? In this paper, we introduce POEMetric, the first comprehensive framework for poetry evaluation, examining 1) basic instruction-following abilities in generating poems according to a certain form and theme, 2) advanced abilities of showing creativity, lexical diversity, and idiosyncrasy, evoking emotional resonance, and using imagery and literary devices, and 3) general appraisal of the overall poem quality and estimation of authorship. We curated a human poem dataset - 203 English poems of 7 fixed forms annotated with meter, rhyme patterns and themes - and experimented with 30 LLMs for poetry generation based on the same forms and themes of the human data, totaling 6,090 LLM poems. Based on POEMetric, we assessed the performance of both human poets and LLMs through rule-based evaluation and LLM-as-a-judge, whose results were validated by human experts. Results show that, though the top model achieved high form accuracy (4.26 out of 5.00, with Gemini-2.5-Pro as a judge; same below) and theme alignment (4.99), all models failed to reach the same level of advanced abilities as human poets, who achieved unparalleled creativity (4.02), idiosyncrasy (3.95), emotional resonance (4.06), and skillful use of imagery (4.49) and literary devices (4.67). Humans also defeated the best-performing LLM in overall poem quality (4.22 vs. 3.20). As such, poetry generation remains a formidable challenge for LLMs.

# POEMetric: The Evaluation Metrics

<img width="5639" height="1725" alt="evaluation_metrics" src="https://github.com/user-attachments/assets/eadf657f-0608-414c-b550-483c89d601ce" />

To make the framework more robust, we triangulate LLM-as-a-judge with rule-based quantitative evaluation and human expert judgments, as detailed below.

**Rule-based automated evaluation** We applied a handcrafted, rule-based algorithm to automatically detect the meter and rhyme patterns in each poem in order to gauge the overall accuracy of each author. A flowchart of the algorithm can be found in Appendix B, and the script is released in 'POEMetric_rule_based_algorithm.py'. For both human and LLM poems, lexical diversity was calculated with Moving Average Type-Token Ratio (MATTR) averaged across poems for each author, and creativity was quantified as the ratio of repetition of words in an LLM poem compared to the original human work, which was also averaged across poems for each author. 

**LLM-as-a-judge automated evaluation and human validation** We designed a prompting template (Li & Wang, 2024) for LLM-as-a-judge and a survey for human judges based on POEMetric, asking them to answer questions after reading the generation prompt and the poem written in response to the prompt. The questions comprised 10 multiple-choice questions (in line with the 10 metrics in POEMetric) using a 5-point Likert scale, asking the evaluators to score from 1 (Strongly Disagree) to 5 (Strongly Agree), and 3 open-ended questions where the evaluators could comment on why they gave that score in the previous question. The template of the survey for human experts and the evaluation prompt for the LLM judge can be found in Appendix C.

# The Human Poem Dataset
<img width="5337" height="2164" alt="dataset" src="https://github.com/user-attachments/assets/b65a22e7-bee3-4662-a052-f191939ed513" />
We collected and screened the poems from two online databases, the Poetry Foundation and the Academy of American Poets, and released the public-domain poems in 'POEMetric_human_poems_annotated.csv'.


# Showcases
<img width="7350" height="2469" alt="showcase-deepseek-r1" src="https://github.com/user-attachments/assets/d9246c6f-3f6a-479e-855d-3e930acde819" />
<p align="center">
  DeepSeek-R1 vs. Human
</p>

<img width="7350" height="2469" alt="showcase-Claude-3 7-Sonnet" src="https://github.com/user-attachments/assets/994988b8-5d46-4f5d-a532-5fb31be4e66d" />
<p align="center">
Claude-3.7-Sonnet vs. Human
</p>

<img width="7350" height="2469" alt="showcase-Gemini-2 5-Pro" src="https://github.com/user-attachments/assets/fba715c8-9bfa-44d8-b6a1-5e328e49a992" />
<p align="center">
Gemini-2.5-Pro vs. Human
</p>


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
