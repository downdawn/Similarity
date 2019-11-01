# -*- coding: utf-8 -*-

# 正则
import re
# html 包
import html
# 数学包
import math
# 自然语言处理包
import jieba
import jieba.analyse


class SimHashSimilarity(object):
    """
    SimHash
    """
    def __init__(self, content_x1, content_y2):
        self.s1 = content_x1
        self.s2 = content_y2

    @staticmethod
    def get_bin_str(source):  # 字符串转二进制
        if source == "":
            return 0
        else:
            t = ord(source[0]) << 7
            m = 1000003
            mask = 2 ** 128 - 1
            for c in source:
                t = ((t * m) ^ ord(c)) & mask
            t ^= len(source)
            if t == -1:
                t = -2
            t = bin(t).replace('0b', '').zfill(64)[-64:]
            return str(t)

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
        keywords = jieba.analyse.extract_tags("|".join(seg), topK=200, withWeight=True)
        return keywords

    def run(self, keywords):
        ret = []
        for keyword, weight in keywords:
            bin_str = self.get_bin_str(keyword)
            key_list = []
            for c in bin_str:
                weight = math.ceil(weight)
                if c == "1":
                    key_list.append(int(weight))
                else:
                    key_list.append(-int(weight))
            ret.append(key_list)
        # 对列表进行"降维"
        rows = len(ret)
        cols = len(ret[0])
        result = []
        for i in range(cols):
            tmp = 0
            for j in range(rows):
                tmp += int(ret[j][i])
            if tmp > 0:
                tmp = "1"
            elif tmp <= 0:
                tmp = "0"
            result.append(tmp)
        return "".join(result)

    def main(self):
        # 去除停用词
        jieba.analyse.set_stop_words('./files/stopwords.txt')

        # 提取关键词
        s1 = self.extract_keyword(self.s1)
        s2 = self.extract_keyword(self.s2)

        sim_hash1 = self.run(s1)
        sim_hash2 = self.run(s2)
        # print(f'相似哈希指纹1: {sim_hash1}\n相似哈希指纹2: {sim_hash2}')
        length = 0
        for index, char in enumerate(sim_hash1):
            if char == sim_hash2[index]:
                continue
            else:
                length += 1
        return length


# 测试
if __name__ == '__main__':
    with open('./files/sample_x.txt', 'r') as x, open('./files/sample_y.txt', 'r') as y:
        content_x = x.read()
        content_y = y.read()

        similarity = SimHashSimilarity(content_x, content_y)
        similarity = similarity.main()
        # 阀值
        threshold = 3
        print(f'海明距离：{similarity} 判定距离：{threshold} 是否相似：{similarity <= threshold}')
