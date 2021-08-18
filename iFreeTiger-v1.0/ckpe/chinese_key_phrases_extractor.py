# -*- encoding=utf-8 -*-

import json
import re
from os.path import join, dirname

import numpy as np
import pkuseg


class ChineseKeyPhrasesExtractor(object):
    def __init__(self, ):
        # 词性预处理
        self.pos_name = ['n', 't', 's', 'f', 'm', 'q', 'b', 'r', 'v', 'a', 'z',
                         'd', 'p', 'c', 'u', 'i', 'l', 'j', 'h', 'k', 'g', 'x',
                         'nr', 'ns', 'nt', 'nx', 'nz', 'vd', 'vx', 'ad', 'an']
        self.pos_exception = ['u', 'p', 'c', 'y', 'e', 'o']
        self.stricted_pos_name = ['a', 'n', 'j', 'nr', 'ns', 'nt', 'nx', 'nz',
                                  'ad', 'an', 'vn', 'vd', 'vx']
        self.redundent_strict_pattern = re.compile('[\*\|`\;:丨－\<\>]')  # 有一个字符即抛弃
        self.redundent_loose_pattern = re.compile('[/\d\.\-:=a-z+,%]+')  # 全部是该字符即抛弃
        self.extra_date_ptn = re.compile('\d{1,2}[月|日]')
        self.exception_char_ptn = re.compile(
            '[^ ¥～「」％－＋\n\u3000\u4e00-\u9fa5\u0021-\u007e'
            '\u00b7\u00d7\u2014\u2018\u2019\u201c\u201d\u2026'
            '\u3001\u3002\u300a\u300b\u300e\u300f\u3010\u3011'
            '\uff01\uff08\uff09\uff0c\uff1a\uff1b\uff1f]')
        self._update_parentheses_ptn('{}「」[]【】()（）<>')
        self._gen_redundant_char_ptn(' -\t\n')

        fine_punctuation = '[，。;；…！、：!?？\r\n ]'
        self.puncs_fine_ptn = re.compile(fine_punctuation)
        self.idf_file_path = join(dirname(__file__), "idf.txt")
        self._load_idf()
        self.seg = pkuseg.pkuseg(postag=True)  # 北大分词器

        # 短语长度权重字典，调整绝大多数的短语要位于2~6个词之间
        self.phrases_length_control_dict = {
            1: 1, 2: 5.6, 3: 1.1, 4: 2.0, 5: 0.7, 6: 0.9, 7: 0.48,
            8: 0.43, 9: 0.24, 10: 0.15, 11: 0.07, 12: 0.05}
        self.phrases_length_control_none = 0.01  # 在大于 7 时选取

        # 短语词性组合权重字典
        with open(join(dirname(__file__), 'pos_combine_weights.json'),
                  'r', encoding='utf8') as f:
            self.pos_combine_weights_dict = json.load(f)

        # 读取停用词文件
        with open(join(dirname(__file__), 'stop_word.txt'),
                  'r', encoding='utf8') as f:
            self.stop_words = list(set(f.read().split()))
            if '' in self.stop_words:
                self.stop_words.remove('')
            if '' not in self.stop_words:
                self.stop_words.append('\n')

        self._lda_prob_matrix()

    def _lda_prob_matrix(self):
        """ 读取 lda 模型有关概率分布文件，并计算 unk 词的概率分布 """
        # 读取 p(topic|word) 概率分布文件，由于 lda 模型过大，不方便加载并计算
        # 概率 p(topic|word)，所以未考虑 p(topic|doc) 概率，可能会导致不准
        # 但是，由于默认的 lda 模型 topic_num == 100，事实上，lda 模型是否在
        # 预测的文档上收敛对结果影响不大（topic_num 越多，越不影响）。
        with open(join(dirname(__file__), 'topic_word_weight.json'),
                  'r', encoding='utf8') as f:
            self.topic_word_weight = json.load(f)
        self.word_num = len(self.topic_word_weight)

        # 读取 p(word|topic) 概率分布文件
        with open(join(dirname(__file__), 'word_topic_weight.json'),
                  'r', encoding='utf8') as f:
            self.word_topic_weight = json.load(f)
        self.topic_num = len(self.word_topic_weight)

        self._topic_prominence()  # 预计算主题突出度

    def _load_idf(self):
        with open(self.idf_file_path, 'r', encoding='utf-8') as f:
            idf_list = [line.strip().split(' ') for line in f.readlines()]
        self.idf_dict = dict()
        for item in idf_list:
            self.idf_dict.update({item[0]: float(item[1])})
        self.median_idf = sorted(self.idf_dict.values())[len(self.idf_dict) // 2]

    def _update_parentheses_ptn(self, parentheses):
        ''' 更新括号权重 '''
        length = len(parentheses)
        assert len(parentheses) % 2 == 0

        remove_ptn_list = []
        remove_ptn_format = '{left}[^{left}{right}]*{right}'
        for i in range(0, length, 2):
            left = re.escape(parentheses[i])
            right = re.escape(parentheses[i + 1])
            remove_ptn_list.append(remove_ptn_format.format(left=left, right=right))
        remove_ptn = '|'.join(remove_ptn_list)

        self.remove_parentheses_ptn = re.compile(remove_ptn)
        self.parentheses = parentheses

    def _gen_redundant_char_ptn(self, redundant_char):
        """ 生成 redundant_char 的正则 pattern """
        pattern_list = []
        for char in redundant_char:
            pattern_tmp = '(?<={char}){char}+'.format(char=re.escape(char))
            # pattern_tmp = re.escape(char) + '{2,}'
            pattern_list.append(pattern_tmp)
        pattern = '|'.join(pattern_list)
        self.redundant_char_ptn = re.compile(pattern)

    def _preprocessing_text(self, text):
        """ 使用预处理函数去除文本中的各种杂质 """
        # 去除中文的异常字符
        text = self.exception_char_ptn.sub('', text)
        # 去除中文的冗余字符
        text = self.redundant_char_ptn.sub('', text)
        # 去除文本中的各种括号
        length = len(text)
        while True:
            text = self.remove_parentheses_ptn.sub('', text)
            if len(text) == length:
                break
            length = len(text)

        return text

    def _split_sentences(self, text):
        """ 将文本切分为若干句子 """
        tmp_list = self.puncs_fine_ptn.split(text)
        sentences = [sen for sen in tmp_list if sen != '']
        return sentences

    def extract_keyphrase(self, text, top_k=7, with_weight=False,
                          func_word_num=1, stop_word_num=0,
                          max_phrase_len=25,
                          topic_theta=0.5, allow_pos_weight=True,
                          stricted_pos=True, allow_length_weight=True,
                          allow_topic_weight=True,
                          without_person_name=False,
                          without_location_name=False,
                          remove_phrases_list=None,
                          remove_words_list=None,
                          specified_words=dict(), bias=None):
        try:
            # 配置参数
            if without_location_name:
                if 'ns' in self.stricted_pos_name:
                    self.stricted_pos_name.remove('ns')
                if 'ns' in self.pos_name:
                    self.pos_name.remove('ns')
            else:
                if 'ns' not in self.stricted_pos_name:
                    self.stricted_pos_name.append('ns')
                if 'ns' not in self.pos_name:
                    self.pos_name.append('ns')

            if without_person_name:
                if 'nr' in self.stricted_pos_name:
                    self.stricted_pos_name.remove('nr')
                if 'nr' in self.pos_name:
                    self.pos_name.remove('nr')
            else:
                if 'nr' not in self.stricted_pos_name:
                    self.stricted_pos_name.append('nr')
                if 'nr' not in self.pos_name:
                    self.pos_name.append('nr')

            # step0: 清洗文本，去除杂质
            text = self._preprocessing_text(text)

            # step1: 分句，使用北大的分词器 pkuseg 做分词和词性标注
            sentences_list = self._split_sentences(text)
            sentences_segs_list = list()
            counter_segs_list = list()
            for sen in sentences_list:
                sen_segs = self.seg.cut(sen)
                sentences_segs_list.append(sen_segs)
                counter_segs_list.extend(sen_segs)

            # step2: 计算词频
            total_length = len(counter_segs_list)
            freq_dict = dict()
            for word_pos in counter_segs_list:
                word, pos = word_pos
                if word in freq_dict:
                    freq_dict[word][1] += 1
                else:
                    freq_dict.update({word: [pos, 1]})

            # step3: 计算每一个词的权重
            sentences_segs_weights_list = list()
            for sen, sen_segs in zip(sentences_list, sentences_segs_list):
                sen_segs_weights = list()
                for word_pos in sen_segs:
                    word, pos = word_pos
                    if pos in self.pos_name:  # 虚词权重为 0
                        if word in self.stop_words:  # 停用词权重为 0
                            weight = 0.0
                        else:
                            if word in specified_words:  # 为词计算权重
                                if bias is None:
                                    weight = freq_dict[word][1] * self.idf_dict.get(
                                        word, self.median_idf) / total_length + 1 / specified_words[word]
                                else:
                                    weight = freq_dict[word][1] * self.idf_dict.get(
                                        word, self.median_idf) / total_length + bias
                            else:
                                weight = freq_dict[word][1] * self.idf_dict.get(
                                    word, self.median_idf) / total_length
                    else:
                        weight = 0.0
                    sen_segs_weights.append(weight)
                sentences_segs_weights_list.append(sen_segs_weights)

            # step4: 通过一定规则，找到候选短语集合，以及其权重
            candidate_phrases_dict = dict()
            for sen_segs, sen_segs_weights in zip(
                    sentences_segs_list, sentences_segs_weights_list):
                sen_length = len(sen_segs)

                for n in range(1, sen_length + 1):  # n-grams
                    for i in range(0, sen_length - n + 1):
                        candidate_phrase = sen_segs[i: i + n]

                        # 由于 pkuseg 的缺陷，日期被识别为 n 而非 t，故删除日期
                        res = self.extra_date_ptn.match(candidate_phrase[-1][0])
                        if res is not None:
                            continue

                        # 找短语过程中需要进行过滤，分为严格、宽松规则
                        if not stricted_pos:
                            rule_flag = self._loose_candidate_phrases_rules(
                                candidate_phrase, func_word_num=func_word_num,
                                max_phrase_len=max_phrase_len,
                                stop_word_num=stop_word_num)
                        else:
                            rule_flag = self._stricted_candidate_phrases_rules(
                                candidate_phrase, max_phrase_len=max_phrase_len)
                        if not rule_flag:
                            continue

                        # 由于 pkuseg 的缺陷，会把一些杂质符号识别为 n、v、adj，故须删除
                        redundent_flag = False
                        for item in candidate_phrase:
                            matched = self.redundent_strict_pattern.search(item[0])
                            if matched is not None:
                                redundent_flag = True
                                break
                            matched = self.redundent_loose_pattern.search(item[0])

                            if matched is not None and matched.group() == item[0]:
                                redundent_flag = True
                                break
                        if redundent_flag:
                            continue

                        # 如果短语中包含了某些不想要的词，则跳过
                        if remove_words_list is not None:
                            unwanted_phrase_flag = False
                            for item in candidate_phrase:
                                if item[0] in remove_words_list:
                                    unwanted_phrase_flag = True
                                    break
                            if unwanted_phrase_flag:
                                continue

                        # 如果短语中没有一个 token 存在于指定词汇中，则跳过
                        if specified_words != dict():
                            with_specified_words_flag = False
                            for item in candidate_phrase:
                                if item[0] in specified_words:
                                    with_specified_words_flag = True
                                    break
                            if not with_specified_words_flag:
                                continue

                        # 条件六：短语的权重需要乘上'词性权重'
                        if allow_pos_weight:
                            start_end_pos = None
                            if len(candidate_phrase) == 1:
                                start_end_pos = candidate_phrase[0][1]
                            elif len(candidate_phrase) >= 2:
                                start_end_pos = candidate_phrase[0][1] + '|' + candidate_phrase[-1][1]
                            pos_weight = self.pos_combine_weights_dict.get(start_end_pos, 1.0)
                        else:
                            pos_weight = 1.0

                        # 条件七：短语的权重需要乘上 '长度权重'
                        if allow_length_weight:
                            length_weight = self.phrases_length_control_dict.get(
                                len(sen_segs_weights[i: i + n]),
                                self.phrases_length_control_none)
                        else:
                            length_weight = 1.0

                        # 条件八：短语的权重需要加上`主题突出度权重`
                        if allow_topic_weight:
                            topic_weight = 0.0
                            for item in candidate_phrase:
                                topic_weight += self.topic_prominence_dict.get(
                                    item[0], self.unk_topic_prominence_value)
                            topic_weight = topic_weight / len(candidate_phrase)
                        else:
                            topic_weight = 0.0

                        candidate_phrase_weight = sum(sen_segs_weights[i: i + n])
                        candidate_phrase_weight *= length_weight * pos_weight
                        candidate_phrase_weight += topic_weight * topic_theta

                        candidate_phrase_string = ''.join([tup[0] for tup in candidate_phrase])
                        if remove_phrases_list is not None:
                            if candidate_phrase_string in remove_phrases_list:
                                continue
                        if candidate_phrase_string not in candidate_phrases_dict:
                            candidate_phrases_dict.update(
                                {candidate_phrase_string: [candidate_phrase,
                                                           candidate_phrase_weight]})

            # step5: 将 overlaping 过量的短语进行去重过滤
            # 尝试了依据权重高低，将较短的短语替代重复了的较长的短语，但效果不好，故删去
            candidate_phrases_list = sorted(
                candidate_phrases_dict.items(),
                key=lambda item: len(item[1][0]), reverse=True)

            de_duplication_candidate_phrases_list = list()
            for item in candidate_phrases_list:
                sim_ratio = self._mmr_similarity(
                    item, de_duplication_candidate_phrases_list)
                if sim_ratio != 1:
                    item[1][1] = (1 - sim_ratio) * item[1][1]
                    de_duplication_candidate_phrases_list.append(item)

            # step6: 按重要程度进行排序，选取 top_k 个
            candidate_phrases_list = sorted(de_duplication_candidate_phrases_list,
                                            key=lambda item: item[1][1], reverse=True)

            if with_weight:
                if top_k != -1:
                    final_res = [(item[0], item[1][1]) for item in candidate_phrases_list[:top_k]
                                 if item[1][1] > 0]
                else:
                    final_res = [(item[0], item[1][1]) for item in candidate_phrases_list
                                 if item[1][1] > 0]
            else:
                if top_k != -1:
                    final_res = [item[0] for item in candidate_phrases_list[:top_k]
                                 if item[1][1] > 0]
                else:
                    final_res = [item[0] for item in candidate_phrases_list
                                 if item[1][1] > 0]
            return final_res

        except Exception as e:
            # print('the text is not legal. \n{}'.format(e))
            return []

    def _mmr_similarity(self, candidate_item,
                        de_duplication_candidate_phrases_list):
        """ 计算 mmr 相似度，用于考察信息量 """
        sim_ratio = 0.0
        candidate_info = set([item[0] for item in candidate_item[1][0]])

        for de_du_item in de_duplication_candidate_phrases_list:
            no_info = set([item[0] for item in de_du_item[1][0]])
            common_part = candidate_info & no_info
            if sim_ratio < len(common_part) / len(candidate_info):
                sim_ratio = len(common_part) / len(candidate_info)
        return sim_ratio

    def _loose_candidate_phrases_rules(self, candidate_phrase,
                                       max_phrase_len=25,
                                       func_word_num=1, stop_word_num=0):
        """ 按照宽松规则筛选候选短语，对词性和停用词宽松 """
        # 条件一：一个短语不能超过 12个 token
        if len(candidate_phrase) > 12:
            return False

        # 条件二：一个短语不能超过 25 个 char
        if len(''.join([item[0] for item in candidate_phrase])) > max_phrase_len:
            return False

        # 条件三：一个短语中不能出现超过一个虚词
        more_than_one_func_word_count = 0
        for item in candidate_phrase:
            if item[1] in self.pos_exception:
                more_than_one_func_word_count += 1
        if more_than_one_func_word_count > func_word_num:
            return False

        # 条件四：短语的前后不可以是虚词、停用词，短语末尾不可是动词
        if candidate_phrase[0][1] in self.pos_exception:
            return False
        if candidate_phrase[len(candidate_phrase) - 1][1] in self.pos_exception:
            return False
        if candidate_phrase[len(candidate_phrase) - 1][1] in ['v', 'd']:
            return False
        if candidate_phrase[0][0] in self.stop_words:
            return False
        if candidate_phrase[len(candidate_phrase) - 1][0] in self.stop_words:
            return False

        # 条件五：短语中不可以超过规定个数的停用词
        has_stop_words_count = 0
        for item in candidate_phrase:
            if item[0] in self.stop_words:
                has_stop_words_count += 1
        if has_stop_words_count > stop_word_num:
            return False
        return True

    def _stricted_candidate_phrases_rules(self, candidate_phrase,
                                          max_phrase_len=25):
        """ 按照严格规则筛选候选短语，严格限制在名词短语 """
        # 条件一：一个短语不能超过 12个 token
        if len(candidate_phrase) > 12:
            return False

        # 条件二：一个短语不能超过 25 个 char
        if len(''.join([item[0] for item in candidate_phrase])) > max_phrase_len:
            return False

        # 条件三：短语必须是名词短语，不能有停用词
        for idx, item in enumerate(candidate_phrase):
            if item[1] not in self.stricted_pos_name:
                return False
            if idx == 0:  # 初始词汇不可以是动词
                if item[1] in ['v', 'vd', 'vx']:  # 动名词不算在内
                    return False
            if idx == len(candidate_phrase) - 1:  # 结束词必须是名词
                if item[1] in ['a', 'ad', 'vd', 'vx', 'v']:
                    return False

        # 条件四：短语中不可以有停用词
        # for item in candidate_phrase:
        #    if item[0] in self.stop_words and item[1] not in self.stricted_pos_name:
        #        return False
        return True

    def _topic_prominence(self):
        """ 计算每个词语的主题突出度，并保存在内存 """
        init_prob_distribution = np.array([self.topic_num for i in range(self.topic_num)])

        topic_prominence_dict = dict()
        for word in self.topic_word_weight:
            conditional_prob_list = list()
            for i in range(self.topic_num):
                if str(i) in self.topic_word_weight[word]:
                    conditional_prob_list.append(self.topic_word_weight[word][str(i)])
                else:
                    conditional_prob_list.append(1e-5)
            conditional_prob = np.array(conditional_prob_list)

            tmp_dot_log_res = np.log2(np.multiply(conditional_prob, init_prob_distribution))
            kl_div_sum = np.dot(conditional_prob, tmp_dot_log_res)  # kl divergence
            topic_prominence_dict.update({word: float(kl_div_sum)})

        tmp_list = [i[1] for i in tuple(topic_prominence_dict.items())]
        max_prominence = max(tmp_list)
        min_prominence = min(tmp_list)
        for k, v in topic_prominence_dict.items():
            topic_prominence_dict[k] = (v - min_prominence) / (max_prominence - min_prominence)

        self.topic_prominence_dict = topic_prominence_dict

        # 计算未知词汇的主题突出度，由于停用词已经预先过滤，所以这里不需要再考停用词无突出度
        tmp_prominence_list = [item[1] for item in self.topic_prominence_dict.items()]
        self.unk_topic_prominence_value = sum(tmp_prominence_list) / (2 * len(tmp_prominence_list))
