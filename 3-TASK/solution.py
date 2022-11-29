from typing import List, Iterable, Set, Tuple, Dict
import lzma
import pickle
import pathlib

import torch
from transformers import BertForTokenClassification, AutoTokenizer

with open(pathlib.Path(".", "state.xz"), "rb") as state_f:
    with open(pathlib.Path(".", "config.xz"), "rb") as config_f:
        state_data = state_f.read()
        config_data = config_f.read()

        filters = [
            {"id": lzma.FILTER_LZMA2, "dict_size": 268435456, "preset": 9, "mf": lzma.MF_HC3, "depth": 0, "lc": 3}]
        state_data = lzma.decompress(state_data, format=lzma.FORMAT_RAW, filters=filters)
        config_data = lzma.decompress(config_data, format=lzma.FORMAT_RAW, filters=filters)

        state = pickle.loads(state_data)
        config = pickle.loads(config_data)
        model = BertForTokenClassification.from_pretrained(config=config, state_dict=state,
                                                           pretrained_model_name_or_path=None)

tokenizer = AutoTokenizer.from_pretrained("tokenizer")

with open('token2idx.pkl', 'rb') as f:
    token2idx = pickle.load(f)

with open('idx2label.pkl', 'rb') as f:
    idx2label = pickle.load(f)

def get_tokens(edges, text):
    tokens = []
    for edge in edges:
        token = text[edge[0]:edge[1]]
        tokens.append(token)
    return tokens

class NERDataset(torch.utils.data.Dataset):
    """
    PyTorch Dataset for NER.
    """

    def __init__(
        self,
        token_seq: List[List[str]],
        #label_seq: List[List[str]],
        token2idx: Dict[str, int],
        #label2idx: Dict[str, int],
    ):
        self.token2idx = token2idx
        #self.label2idx = label2idx

        self.token_seq = [self.process_tokens(tokens, token2idx) for tokens in token_seq]
        #self.label_seq = [self.process_labels(labels, label2idx) for labels in label_seq]

    def __len__(self):
        return len(self.token_seq)

    def __getitem__(
        self,
        idx: int,
    ) -> torch.LongTensor:
        # YOUR CODE HERE
        return torch.LongTensor(self.token_seq[idx])

    @staticmethod
    def process_tokens(
        tokens: List[str],
        token2idx: Dict[str, int],
        unk: str = "<UNK>",
    ) -> List[int]:
        """
        Transform list of tokens into list of tokens' indices.
        """
        # YOUR CODE HERE
        result = []
        for token in tokens:
            result += [token2idx.get(token, token2idx.get(unk))]
        return result

    # @staticmethod
    # def process_labels(
    #     labels: List[str],
    #     label2idx: Dict[str, int],
    # ) -> List[int]:
    #     """
    #     Transform list of labels into list of labels' indices.
    #     """
    #     # YOUR CODE HERE
    #     result = []
    #     for label in labels:
    #         result += [label2idx.get(label)]
    #     return result

class NERCollator:
    """
    Collator that handles variable-size sentences.
    """

    def __init__(
        self,
        token_padding_value: int,
        #label_padding_value: int,
    ):
        self.token_padding_value = token_padding_value
        #self.label_padding_value = label_padding_value

    def __call__(
        self,
        batch: List[Tuple[torch.LongTensor, torch.LongTensor]],
    ) -> torch.LongTensor:

        #tokens, labels = zip(*batch)
        tokens = [torch.LongTensor(token) for token in batch]
        tokens = torch.nn.utils.rnn.pad_sequence(tokens,
                                               batch_first=True,
                                               padding_value=self.token_padding_value).long()
        #labels = torch.nn.utils.rnn.pad_sequence(labels,
        #                                        batch_first=True,
        #                                        padding_value=self.label_padding_value)
        return tokens



class Solution:
    def __init__(self):
        pass

    def predict(self, texts: List[str]) -> Iterable[Set[Tuple[int, int, str]]]:
        tokens = []
        spans = []
        for elem in texts:
            edges = tokenizer(elem, return_offsets_mapping = True, add_special_tokens=False)["offset_mapping"]
            spans.append(edges)
            tokens.append(get_tokens(edges, elem))

        dataset = NERDataset(
            token_seq=tokens,
            token2idx=token2idx,
        )

        collator = NERCollator(token_padding_value=tokenizer.pad_token_id)

        dataloader = torch.utils.data.DataLoader(
            dataset,
            batch_size=1,
            shuffle=False,
            collate_fn=collator,
        )

        idx = 0
        result = []
        for data in dataloader:
            outputs_idx = model(data)["logits"].argmax(dim=-1)[0]
            outputs_labels = [idx2label[idx.item()] for idx in outputs_idx]
            jdx = 0
            begin = 0
            end = 0
            postfix = ''
            res_set = set()
            for label in outputs_labels:
                if label == 'O':
                    if begin == 0 and end == 0:
                        continue
                    else:
                        end = spans[idx][jdx][0]-1
                        if begin >= end:
                            continue
                        res_set.add((begin, end, postfix))
                        begin = end = spans[idx][jdx][1]
                        postfix = ''

                else:
                    split_label = label.split('-')
                    if split_label[0] == 'B' and postfix == '':
                        postfix = split_label[1]
                        begin = spans[idx][jdx][0]
                        end = spans[idx][jdx][1]
                    elif split_label[0] == 'B':
                        end = spans[idx][jdx][0] - 1
                        if begin >= end:
                            continue
                        res_set.add((begin, end, postfix))
                        begin = spans[idx][jdx][0]
                        postfix = split_label[1]
                    else:
                        end = spans[idx][jdx][1]
                jdx += 1
            if end > begin:
                res_set.add((begin, end, postfix))
            idx += 1
            result.append(res_set)
        return result


print(Solution().predict(["Василий стал премьер-министром Армении",
                          "Словацкий тренер Жолт Хорняк стал новым главным тренером футбольного клуба 'Бананц' (Ереван). Контракт с 40 летним тренером был подписан по системе '1+1', - сообщает пресс-служба столичного клуба."]))
