import json
import networkx as nx
import matplotlib.pyplot as plt
import re
def load_data(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        file_content = file.read()
        # 将单引号转换为双引号
        file_content = file_content.replace("'", '"')
        return json.loads(file_content)
def format_json(raw_file, output_file):
    try:
        with open(raw_file, 'r', encoding='utf-8') as file:
            raw_content = file.read()

        # 将单引号转换为双引号，但避免更改字符串内容中的单引号
        formatted_content = re.sub(r"(\W)'|'(\W)", r'\1"\2', raw_content)

        # 将所有独立的 JSON 对象包装在一个数组中
        formatted_content = f'[{formatted_content}]'

        # 修复对象之间可能缺少的逗号
        formatted_content = re.sub(r"\}\s*\{", "},{", formatted_content)

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(formatted_content)
        return True
    except Exception as e:
        print(f"Error occurred: {e}")
        return False

# 转换文件
raw_file = 'result.json'  # 原始数据文件的路径
output_file = 'result.json'  # 输出 JSON 文件的路径

# if format_json(raw_file, output_file):
#     print("Data formatted successfully.")
# else:
#     print("Data formatting failed.")

# 加载数据
data = load_data("result.json")

# 创建一个空的图
G = nx.Graph()

# 解析数据并构建图
for item in data:
    for trigger_dict in item:  # item 是一个字典
        trigger_list = trigger_dict.get('触发词', [])
        for trigger in trigger_list:
            trigger_word = trigger.get('text')
            relations = trigger.get('relations', {})

            for relation_type, entities in relations.items():
                for entity in entities:
                    entity_text = entity.get('text')
                    # 添加节点
                    G.add_node(entity_text, type=relation_type)
                    # 添加带权重的边
                    G.add_edge(trigger_word, entity_text, weight=entity.get('probability'),relation=relation_type)
#设置字体为楷体
# plt.rcParams['font.sans-serif'] = ['KaiTi']

# # 绘制图表
# pos = nx.spring_layout(G)  # 使用Spring布局
# nx.draw(G, pos, with_labels=True, font_weight='bold')

# 显示图表
# plt.show()
def analyze_sentence(sentence, graph):
    entities = graph.nodes
    relations = nx.get_edge_attributes(graph, 'relation')

    found_entities = [entity for entity in entities if entity in sentence]
    found_relations = {k: v for k, v in relations.items() if k[0] in found_entities and k[1] in found_entities}

    return found_entities, found_relations

# 示例使用
while True:
    sentence = input("请输入一个句子：")
    if sentence == '退出':
        break
    entities, relations = analyze_sentence(sentence, G)

    print("在句子中找到的实体:", entities)
    print("在句子中找到的关系:", relations)