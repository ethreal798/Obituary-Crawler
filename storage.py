import os
import pandas as pd

class CSVStorage:
    def __init__(self,filename):
        self.filename = filename

    def save_batch(self,data_list):
        """追加一批数据到CSV"""
        df = pd.DataFrame(data_list)
        if not os.path.exists(self.filename):
            df.to_csv(self.filename,index=False,encoding='utf-8-sig')
        else:
            df.to_csv(self.filename,mode='a',header=False,index=False,encoding='utf-8-sig')