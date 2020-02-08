from . import InputExample
import csv
import gzip
import os
import pandas as pd
class QuoraDataReader:
    """
    Reads in the STS dataset. Each line contains two sentences (s1_col_idx, s2_col_idx) and one label (score_col_idx)
    """
    def __init__(self, dataset_folder, s1_col_idx=3, s2_col_idx=4, score_col_idx=5, delimiter="\t",
                 quoting=csv.QUOTE_NONE, normalize_scores=True, min_score=0, max_score=1):
        self.dataset_folder = dataset_folder
        self.score_col_idx = score_col_idx
        self.s1_col_idx = s1_col_idx
        self.s2_col_idx = s2_col_idx
        self.delimiter = delimiter
        self.quoting = quoting
        self.normalize_scores = normalize_scores
        self.min_score = min_score
        self.max_score = max_score

    def get_examples(self, filename, max_examples=0):
        """
        filename specified which data split to use (train.csv, dev.csv, test.csv).
        """
        data = csv.reader(open(os.path.join(self.dataset_folder, filename), encoding="utf-8"),
                          delimiter=self.delimiter, quoting=self.quoting)
        df =pd.read_csv(os.path.join(self.dataset_folder, filename), header =None)
        df[self.s1_col_idx] = df[self.s1_col_idx].astype(str)
        df[self.s2_col_idx] = df[self.s2_col_idx].astype(str)
        examples = []
        
        for id,row in df.iterrows():
            score =int(row[self.score_col_idx])
            if self.normalize_scores:  # Normalize to a 0...1 value
                score = (score - self.min_score) / (self.max_score - self.min_score)

            s1 = row[self.s1_col_idx]
            s2 = row[self.s2_col_idx]
            examples.append(InputExample(guid=filename+str(id), texts=[s1, s2], label=score))

            if max_examples > 0 and len(examples) >= max_examples:
                break

        return examples
    
#         for id, row in enumerate(data):
#             print(id, row)
#             print(int(self.score_col_idx))
#             print(len(row))
#             score = int(row[self.score_col_idx])
#             if self.normalize_scores:  # Normalize to a 0...1 value
#                 score = (score - self.min_score) / (self.max_score - self.min_score)

#             s1 = row[self.s1_col_idx]
#             s2 = row[self.s2_col_idx]
#             examples.append(InputExample(guid=filename+str(id), texts=[s1, s2], label=score))

#             if max_examples > 0 and len(examples) >= max_examples:
#                 break

#         return examples
