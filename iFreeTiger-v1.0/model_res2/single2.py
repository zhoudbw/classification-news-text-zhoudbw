import torch
from transformers import (
    InputExample,
    BertForSequenceClassification,  # Bert分类模型
    BertTokenizer,
    glue_convert_examples_to_features,
)
import numpy
from torch.utils.data import TensorDataset, DataLoader
import time

# 导入该模块忽略警告
import warnings

warnings.filterwarnings('ignore')

# 使用CPU
device = torch.device("cpu")

# 将classes里面存储的类别，存储到label_types列表中
file_classes = open("model_res2/classes.txt", "r", encoding="utf-8")
line_all = file_classes.read()
label_types = line_all.split("\n")[0:10]
# print(label_types)


def get_example(line):
    # 将传递进来的lines中的元素都变成InputExample对象，并返回出去
    guid = "%s-%s" % ('single', 666)  # 示例的唯一id。
    test_single_one_example = InputExample(guid=guid, text_a=line, text_b=None, label=None)
    # 将test_single_example存入列表，成为一个迭代器
    test_single_example = [test_single_one_example]
    # print('test_single_example:', test_single_example)
    return test_single_example


def get_features(test_single_example):
    # 选择 bert-base-chinese 预训练模型
    # print('加载 BERT tokenizer...')
    tokenizer = BertTokenizer.from_pretrained('model_res2')
    # print("start input features")
    test_single_example_features = glue_convert_examples_to_features(
        examples=test_single_example,
        tokenizer=tokenizer,
        max_length=64,
        task=None,
        label_list=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        output_mode="classification",
    )
    # print('test_single_example_features:\n', test_single_example_features)
    # print('len(test_single_example_features)', len(test_single_example_features))
    # print("finish train_features.....")
    return test_single_example_features


# 设计dataset
# 根据上面的打印我们可以知道InputFeatures的字段，
# 这个方法就是为了将这些属性拿出来，存在对应的列表中，然后转成我们可以使用的数据
def build_dataset(features):
    # print('len(build_dataset-(features))', len(features))
    input_ids = []
    attention_mask = []
    token_type_ids = []
    labels = []
    for feature in features:
        input_ids.append(feature.input_ids)
        attention_mask.append(feature.attention_mask)
        token_type_ids.append(feature.token_type_ids)
        labels.append(feature.label)
    # dataset使用的是64位的长整型，通过numpy数组形式转为torch然后转变为long类型
    input_ids = torch.from_numpy(numpy.array(input_ids)).long()
    # print('input_ids:', input_ids)
    attention_mask = torch.from_numpy(numpy.array(attention_mask)).long()
    # print('attention_mask:', attention_mask)
    token_type_ids = torch.from_numpy(numpy.array(token_type_ids)).long()
    # print('token_type_ids:', token_type_ids)
    dataset = TensorDataset(input_ids, attention_mask, token_type_ids)
    # print('build_dataset-(dataset)', len(dataset))
    # print('dataset:', dataset)
    return dataset


def get_dataloader_model(line):
    test_single_example = get_example(line)
    test_single_example_features = get_features(test_single_example)
    # 获取dataset,通过dataset获取dataloader
    # 把features 放入dataset中，就是上面的方法的调用，得到对应的dataset
    test_single_example_dataset = build_dataset(test_single_example_features)
    # 把dataset 装入dataloader中
    test_single_example_dataloader = DataLoader(test_single_example_dataset, batch_size=1)
    bert_model = BertForSequenceClassification.from_pretrained(
        "model_res2",
        num_labels=10,
        output_attentions=False,
        output_hidden_states=False,
    )
    return test_single_example_dataloader, bert_model


# 预测函数
def main(line):
    test_single_example_dataloader, model = get_dataloader_model(line)
    model.eval()
    possible_list2 = []  # 存储结果集
    for batch in test_single_example_dataloader:
        b_input_ids = batch[0].to(device)
        b_input_mask = batch[1].to(device)

        # 预测阶段，不更新权值，不改变计算图
        with torch.no_grad():
            time_start = time.time()
            print('加载预测模型...')
            out = model(b_input_ids,
                        token_type_ids=None,
                        attention_mask=b_input_mask,
                        labels=None)
            print('加载预测模型结束...')
            logits = out[0]
            time_end = time.time()
            # print('logits:', logits)
            num_max = torch.argmax(logits, 1)
            # print('num_max:', num_max)
            possible = label_types[int(num_max)]
            print("新闻类型：", possible)
            possible_list2.append(possible)
            time_end2 = time.time()
            model_time = time_end - time_start  # 模型加载时间
            run_time = time_end2 - time_end  # 模型运行时间
    return model_time, run_time, possible_list2


# 在测试集合上预测
if __name__ == '__main__':
    line = '宝贝梦网国战在即 号召各国招兵买马'
    model_time, run_time, possible_list2 = main(line)
    print('类别：', possible_list2)
    print('模型加载时间：', model_time, '秒')
    print('模型运行时间：', run_time, '秒')