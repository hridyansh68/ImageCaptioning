def load_doc(filename):
    file = open(filename,'r')
    text = file.read()
    file.close()
    return text

def load_set(filename):
    doc = load_doc(filename)
    dataset = list()
    for line in doc.split('\n'):
        if len(line)<1:
            continue
        identifier = line.split('.')[0]
        dataset.append(identifier)
    return(set(dataset))
    
def load_clean_descriptions(filename,dataset):
    doc = load_doc(filename)
    descriptions = dict()
    for line in doc.split("\n"):
        tokens = line.split()
        image_id,image_desc = tokens[0],tokens[1:]
        if image_id in dataset:
            if image_id not in descriptions:
                descriptions[image_id] = list()
            desc = 'startseq ' + ' '.join(image_desc) + ' endseq'
            descriptions[image_id].append(desc)
    return(descriptions)

from pickle import load
    
def load_photo_features(filename,dataset):
    all_features = load(open(filename,'rb'))
    features = {k: all_features[k] for k in dataset}
    return features


filename = 'Flickr8k_text/Flickr_8k.trainImages.txt'
train = load_set(filename)
print('Dataset: %d' % len(train))

train_descriptions = load_clean_descriptions('descriptions.txt', train)
print('Descriptions: train=%d' % len(train_descriptions))

train_features = load_photo_features('features.pkl', train)
print('Photos: train=%d' % len(train_features))

from keras.preprocessing.text import Tokenizer

def to_lines(descriptions):
	all_desc = list()
	for key in descriptions.keys():
		[all_desc.append(d) for d in descriptions[key]]
	return all_desc


def create_tokenizer(descriptions):
	lines = to_lines(descriptions)
	tokenizer = Tokenizer()
	tokenizer.fit_on_texts(lines)
	return tokenizer

tokenizer = create_tokenizer(train_descriptions)
vocab_size = len(tokenizer.word_index) + 1
print('Vocabulary Size: %d' % vocab_size)