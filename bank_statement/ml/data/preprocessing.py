import numpy as np
import pandas as pd
import gensim
import nltk
import glob2
import pickle as pkl
import re
import itertools

def init_package():
    nltk.download('wordnet')
    nltk.download('stopwords')
    np.random.seed (seed=1000)

def get_data_statistics(data_path):
    '''
    get the dataset stats (regarding to the classes present in the dataset)
    '''
    list_xlsx = glob2.glob(f"{data_path}/*")

    stats_list = []
    df_list = []
    for xlsx in list_xlsx:
        xlsx_basename = xlsx.split("/")[-1]
        df_xlsx = pd.read_excel(xlsx)
        df_xlsx["Class"].value_counts()

        stats_list.append(pd.DataFrame(df_xlsx["Class"].value_counts()))
        df_list.append(df_xlsx)
    
    df_dataset = pd.concat(df_list, axis=0).reset_index(drop=True)
    stats_dataset = pd.concat(stats_list, axis=0).groupby(level=0).sum()
    stats_dataset.to_csv("./ml/data/stats.csv", sep=';')
    df_dataset.to_csv("./ml/data/df_total.csv", sep=';')

def get_histogram(csv_in, html_out):
    '''
    generate the plot for the dataset stats (regarding to the classes present in the dataset)
    '''
    pass

def get_words_only(some_text):
    try: 
        pre_res = re.findall(
                pattern=r'\w*\s', 
                string= str(some_text).strip(), 
                flags=re.IGNORECASE)
        res = ('').join(pre_res)
    except:
        res = None
    return res

def closure_get_break_words(key_word='FROM'):
    
    def get_break_words(matchobj):
        m =  matchobj.group(0)
        m = re.sub(key_word, f" {key_word} ", m)
        m = m.upper().replace(key_word, f" {key_word} ").strip()

        return m
    return get_break_words

def get_words_unsticked(some_text, k_word='from'):
    try: 
        my_str = f'[\w|\W]*{k_word}[\w|\W]*\s'
        res = re.sub(
                pattern=my_str, 
                repl=closure_get_break_words(key_word=k_word),
                string= str(some_text.upper()).strip(), 
                flags=re.IGNORECASE)
    except Exception as e:
        print(e)
        res = None
    return res

def master_df_words_only(master_df):
    
    master_df["filtered_description_words_unsticked"] = master_df["filtered_description"].apply(lambda x: get_words_only(x))\
                                                                                        .apply(lambda x: get_words_unsticked(x,'FROM'))\
                                                                                        .apply(lambda x: get_words_unsticked(x,'VIA'))\
                                                                                        .apply(lambda x: get_words_unsticked(x,'BETWEEN'))\
                                                                                        .apply(lambda x: (' ').join([el for el in x.split() if el !='']))
    
    return master_df
    
def lemmatize_dataset(master_df):
    lem = nltk.stem.wordnet.WordNetLemmatizer()
    master_df["filtered_description_words_unsticked"] = master_df["filtered_description_words_unsticked"].\
                        apply(lambda x: (' ').join([lem.lemmatize(word) for word in x.split()]))
    master_df["filtered_description_no_stopwords"] = master_df["filtered_description_words_unsticked"].\
                        apply(lambda x: (' ').join([word for word in x.split() if word.lower() not in nltk.corpus.stopwords.words("english")]))
    return master_df

def get_vocab(master_df):
    res = [el.split(' ') for el in master_df["filtered_description_no_stopwords"].values]
    res = list(itertools.chain(*res))
    uniq_values = np.unique(res)
    return pd.DataFrame(uniq_values)


def split_dataset(master_df):
    idx_list = np.arange(master_df.shape[0])

    np.random.shuffle(idx_list)
    shuffled = master_df.loc[idx_list].reset_index()
    test, train = shuffled.loc[:int(0.8*shuffled.shape[0])], shuffled.loc[int(0.8*shuffled.shape[0]):]

    return test, train

def  create_vectorizer(master_df, mode):

    if mode =='BOW':
        ## Count (classic BoW)
        vectorizer = feature_extraction.text.CountVectorizer(max_features=10000, ngram_range=(1,2))
    elif mode == 'TFIDF':
        ## Tf-Idf (advanced variant of BoW)
        vectorizer = feature_extraction.text.TfidfVectorizer(max_features=10000, ngram_range=(1,2))

    return vectorizer

if __name__=='__main__':
    data_path = './out'
    init_package()
    #get_data_statistics(data_path)
    master_df = pd.read_csv("./ml/data/df_total.csv", sep=';')
    master_df = master_df_words_only(master_df)
    master_df = lemmatize_dataset(master_df)
    master_df.to_csv("./ml/data/master_df_words.csv", sep=';')
    uniq_vals_df = get_vocab(master_df)
    uniq_vals_df.to_csv("./ml/data/uniq_vals_df.csv", sep=';')

    te, tr = split_dataset(master_df)
    te.to_csv("./ml/data/test_df.csv", sep=';')
    tr.to_csv("./ml/data/train_df.csv", sep=';')

    print(te.shape)
    #print(master_df.head())
    #print('between' in nltk.corpus.stopwords.words("english"))