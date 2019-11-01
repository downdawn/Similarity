# -*- coding: utf-8 -*-

# 正则包
import re
# html 包
import html
# 自然语言处理包
import jieba
import jieba.analyse
# 编辑距离包
import Levenshtein


class LevenshteinSimilarity(object):
    """
    编辑距离
    """
    def __init__(self, content_x1, content_y2):
        self.s1 = content_x1
        self.s2 = content_y2

    @staticmethod
    def extract_keyword(content):  # 提取关键词
        # 正则过滤 html 标签
        re_exp = re.compile(r'(<style>.*?</style>)|(<[^>]+>)', re.S)
        content = re_exp.sub(' ', content)
        # html 转义符实体化
        content = html.unescape(content)
        # 切割
        seg = [i for i in jieba.cut(content, cut_all=True) if i != '']
        # 提取关键词
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=200, withWeight=False)
        return keywords

    def main(self):
        # 去除停用词
        jieba.analyse.set_stop_words('./files/stopwords.txt')

        # 提取关键词
        keywords1 = ', '.join(self.extract_keyword(self.s1))
        keywords2 = ', '.join(self.extract_keyword(self.s2))

        # ratio计算2个字符串的相似度，它是基于最小编辑距离
        distances = Levenshtein.ratio(keywords1, keywords2)
        return distances


# 测试
if __name__ == '__main__':
    with open('./files/sample_x.txt', 'r') as x, open('./files/sample_y.txt', 'r') as y:
        content_x = x.read()
        content_y = y.read()
        distance = LevenshteinSimilarity(content_x, content_y)
        distance = distance.main()
        print('相似度: %.2f%%' % (distance * 100))
