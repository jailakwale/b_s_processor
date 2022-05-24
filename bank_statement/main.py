import logging
import os
import re
import time

#import cv2
import glob2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tabula
from tqdm import tqdm

from analytics import metrics
from bank_exceptions import errors
from statement import gtbank
from utils import bank_logger, image_processing, io
from dataconf.data_config import BANK_OPERATIONS 
from features.bank_dataset import Dataset_Bank
from analytics.metrics import Metrics2

import time
if __name__=='__main__':

    
    f_name_list = glob2.glob("./data/statement/*.pdf")

    for f_name in tqdm(f_name_list):
        try:
            start = time.time()
            gt_customer1 =  gtbank.GT_BankStatement_no_header(f_name)
            gt_customer1_dataset = Dataset_Bank(gt_customer1.dataset_recombined, BANK_OPERATIONS)
            gt_customer1_metrics = Metrics2(gt_customer1_dataset)
            end = time.time()
            print(f"the process took: {end-start} s")
        except Exception as e:
            print(e, f_name)