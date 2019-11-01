# -*- coding: utf-8 -*-

# 正则包
import re
# 自然语言处理包
import jieba
import jieba.analyse
# html 包
import html
# 数据集处理包
from datasketch import MinHash


class MinHashSimilarity(object):
    """
    MinHash
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

        # MinHash计算
        m1, m2 = MinHash(), MinHash()
        # 提取关键词
        s1 = self.extract_keyword(self.s1)
        s2 = self.extract_keyword(self.s2)

        for data in s1:
            m1.update(data.encode('utf8'))
        for data in s2:
            m2.update(data.encode('utf8'))

        return m1.jaccard(m2)


# 测试
if __name__ == '__main__':
    with open('./files/sample_x.txt', 'r') as x, open('./files/sample_y.txt', 'r') as y:
        content_x = x.read()
        content_y = y.read()
        similarity = MinHashSimilarity(content_x, content_y)
        similarity = similarity.main()
        print('相似度: %.2f%%' % (similarity*100))
