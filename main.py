import spacy
nlp = spacy.load('pt_core_news_lg')

entities_file = open('entities.txt', 'r')
entities = [entity.replace(' ', '-') for entity in entities_file.read().split('\n')]
entities_file.close()

target_file = open('target.txt', 'r')
targets = [target.replace(' ', '-') for target in target_file.read().split('\n')]
target_file.close()

all_entities_str = ' '.join(targets + entities)
doc = nlp(all_entities_str)
tokens = [token for token in doc]

entity_mapping = {} # entity -> target
target_groupping = {} # target -> array of entities
for target in targets:
    target_groupping[target] = []
unmapped_entities = []

num_of_targets = len(targets)
for i in range(num_of_targets, num_of_targets + len(entities)):
    target = ''
    biggest_similarity = 0
    for j in range(num_of_targets):
        similarity = tokens[i].similarity(tokens[j])
        if similarity > biggest_similarity:
            biggest_similarity = similarity
            target = tokens[j]
    if target == '':
        unmapped_entities.append(tokens[i])
    else:
        entity_mapping[str(tokens[i])] = target
        target_groupping[str(target)].append(tokens[i])

mapping_file = open('results/mapping.txt', 'w')
for entity in entity_mapping:
    mapping_file.write(f'{entity}: {entity_mapping[entity]}\n')
mapping_file.close()

unmapped_entities_file = open('results/unmapped.txt', 'w')
for entity in unmapped_entities:
    unmapped_entities_file.write(f'{entity}\n')
unmapped_entities_file.close()

for target in target_groupping:
    target_group_file = open(f'results/target_groups/{target}.txt', 'w')
    for entity in target_groupping[target]:
        target_group_file.write(f'{entity}\n')
    target_group_file.close()

print(len(unmapped_entities))