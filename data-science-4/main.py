#!/usr/bin/env python
# coding: utf-8

# # Desafio 6
# 
# Neste desafio, vamos praticar _feature engineering_, um dos processos mais importantes e trabalhosos de ML. Utilizaremos o _data set_ [Countries of the world](https://www.kaggle.com/fernandol/countries-of-the-world), que contém dados sobre os 227 países do mundo com informações sobre tamanho da população, área, imigração e setores de produção.
# 
# > Obs.: Por favor, não modifique o nome das funções de resposta.

# ## _Setup_ geral

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import sklearn as sk
from sklearn.preprocessing import KBinsDiscretizer,StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.datasets import load_digits, fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer


# In[2]:


# Algumas configurações para o matplotlib.
#%matplotlib inline

#from IPython.core.pylabtools import figsize


#figsize(12, 8)

#sns.set()


# In[3]:


countries = pd.read_csv("countries.csv")


# In[4]:


new_column_names = [
    "Country", "Region", "Population", "Area", "Pop_density", "Coastline_ratio",
    "Net_migration", "Infant_mortality", "GDP", "Literacy", "Phones_per_1000",
    "Arable", "Crops", "Other", "Climate", "Birthrate", "Deathrate", "Agriculture",
    "Industry", "Service"
]

countries.columns = new_column_names

countries.head(5)


# ## Observações
# 
# Esse _data set_ ainda precisa de alguns ajustes iniciais. Primeiro, note que as variáveis numéricas estão usando vírgula como separador decimal e estão codificadas como strings. Corrija isso antes de continuar: transforme essas variáveis em numéricas adequadamente.
# 
# Além disso, as variáveis `Country` e `Region` possuem espaços a mais no começo e no final da string. Você pode utilizar o método `str.strip()` para remover esses espaços.

# ## Inicia sua análise a partir daqui

# In[5]:


# Sua análise começa aqui.
countries.info()


# In[6]:


# Informações sobre o dataframe:
info = pd.DataFrame({'type': countries.dtypes,
                            'amount': countries.isna().sum(),
                            'percentage': (countries.isna().sum() / countries.shape[0]) * 100,
                            'unique values': countries.nunique()})
                            

info


# In[7]:


countries['Country'] = countries['Country'].str.strip()


# In[8]:


countries['Region'] = countries['Region'].str.strip()


# In[9]:


for column in countries.columns:
    if countries[column].dtype == np.dtype('O'):
        countries[column] = countries[column].str.replace(',', '.')
        try:
            countries[column] = pd.to_numeric(countries[column])
        except:
            pass
countries.head()


# In[10]:


countries.shape


# ## Questão 1
# 
# Quais são as regiões (variável `Region`) presentes no _data set_? Retorne uma lista com as regiões únicas do _data set_ com os espaços à frente e atrás da string removidos (mas mantenha pontuação: ponto, hífen etc) e ordenadas em ordem alfabética.

# In[11]:


def q1():
    return sorted(countries['Region'].unique())
q1()


# ## Questão 2
# 
# Discretizando a variável `Pop_density` em 10 intervalos com `KBinsDiscretizer`, seguindo o encode `ordinal` e estratégia `quantile`, quantos países se encontram acima do 90º percentil? Responda como um único escalar inteiro.

# In[12]:


def q2():
    discretizer = KBinsDiscretizer(n_bins=10, encode='ordinal', strategy='quantile')
    pop_density_bins = discretizer.fit_transform(countries[['Pop_density']])
    return int(sum(pop_density_bins[:,0] == 9))


# In[13]:


q2()


# # Questão 3
# 
# Se codificarmos as variáveis `Region` e `Climate` usando _one-hot encoding_, quantos novos atributos seriam criados? Responda como um único escalar.

# In[14]:


def q3():
    one_hot_encoder = OneHotEncoder(sparse=False, dtype=np.int)
    region_climate_encoded = one_hot_encoder.fit_transform(countries[["Region", "Climate"]].fillna(0))
    return region_climate_encoded.shape[1]
q3()


# ## Questão 4
# 
# Aplique o seguinte _pipeline_:
# 
# 1. Preencha as variáveis do tipo `int64` e `float64` com suas respectivas medianas.
# 2. Padronize essas variáveis.
# 
# Após aplicado o _pipeline_ descrito acima aos dados (somente nas variáveis dos tipos especificados), aplique o mesmo _pipeline_ (ou `ColumnTransformer`) ao dado abaixo. Qual o valor da variável `Arable` após o _pipeline_? Responda como um único float arredondado para três casas decimais.

# In[22]:


test_country = [
    'Test Country', 'NEAR EAST', -0.19032480757326514,
    -0.3232636124824411, -0.04421734470810142, -0.27528113360605316,
    0.13255850810281325, -0.8054845935643491, 1.0119784924248225,
    0.6189182532646624, 1.0074863283776458, 0.20239896852403538,
    -0.043678728558593366, -0.13929748680369286, 1.3163604645710438,
    -0.3699637766938669, -0.6149300604558857, -0.854369594993175,
    0.263445277972641, 0.5712416961268142
]


# In[23]:


def q4():
    """Using the pipeline to chain multiple transformation tasks."""

    # Selecionando só as colunas numéricas:
    num_features = countries.select_dtypes(exclude=['object'])

    # Lista de etapas do pipeline:
    pipe = Pipeline(steps=[
        ("imputer", SimpleImputer(strategy="median")), 
        ('scale', StandardScaler())])

    # Aplicando o pipeline somente nas variáveis dos tipos especificados:
    pipe.fit(num_features)

    # Aolicando o mesmo pipeline nos dados test_country:
    pipe_transform = pipe.transform([test_country[2:]])

    # Valor da variável Arable após o pipeline:
    answer = pipe_transform[:, num_features.columns.get_loc("Arable")]
    return np.round(answer.item(), 3)
q4()


# ## Questão 5
# 
# Descubra o número de _outliers_ da variável `Net_migration` segundo o método do _boxplot_, ou seja, usando a lógica:
# 
# $$x \notin [Q1 - 1.5 \times \text{IQR}, Q3 + 1.5 \times \text{IQR}] \Rightarrow x \text{ é outlier}$$
# 
# que se encontram no grupo inferior e no grupo superior.
# 
# Você deveria remover da análise as observações consideradas _outliers_ segundo esse método? Responda como uma tupla de três elementos `(outliers_abaixo, outliers_acima, removeria?)` ((int, int, bool)).

# In[17]:


def q5():
    q1 = countries.Net_migration.quantile(0.25)
    q3 = countries.Net_migration.quantile(0.75)
    iqr = q3 - q1
    lim_max = (countries['Net_migration'] < (q1 - 1.5 * iqr)).sum()
    lim_min = (countries['Net_migration'] > (q3 + 1.5 * iqr)).sum()
    return int(lim_max), int(lim_min),False
q5()
    


# ## Questão 6
# Para as questões 6 e 7 utilize a biblioteca `fetch_20newsgroups` de datasets de test do `sklearn`
# 
# Considere carregar as seguintes categorias e o dataset `newsgroups`:
# 
# ```
# categories = ['sci.electronics', 'comp.graphics', 'rec.motorcycles']
# newsgroup = fetch_20newsgroups(subset="train", categories=categories, shuffle=True, random_state=42)
# ```
# 
# 
# Aplique `CountVectorizer` ao _data set_ `newsgroups` e descubra o número de vezes que a palavra _phone_ aparece no corpus. Responda como um único escalar.

# In[18]:


# Carregando as categorias e o dataset newsgroups:
categories = ['sci.electronics', 'comp.graphics', 'rec.motorcycles']
newsgroup = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=1991)


# In[19]:


def q6():
    count_vectorizer = CountVectorizer()
    newsgroups_counts = count_vectorizer.fit_transform(newsgroup.data)
    
    return int(newsgroups_counts[:, count_vectorizer.vocabulary_['phone']].sum())
q6()


# ## Questão 7
# 
# Aplique `TfidfVectorizer` ao _data set_ `newsgroups` e descubra o TF-IDF da palavra _phone_. Responda como um único escalar arredondado para três casas decimais.

# In[20]:


def q7():
    categories = ['sci.electronics', 'comp.graphics', 'rec.motorcycles']
    newsgroups = fetch_20newsgroups(subset="train", categories=categories, shuffle=True, random_state=42)
    
    count_vectorizer = CountVectorizer()
    newsgroups_counts = count_vectorizer.fit_transform(newsgroups.data)
    words_idx = count_vectorizer.vocabulary_.get('phone')
    
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_vectorizer.fit(newsgroups.data)

    newsgroups_tfidf_vectorized = tfidf_vectorizer.transform(newsgroups.data)
    
    return float(newsgroups_tfidf_vectorized[:, words_idx].toarray().sum().round(3))
q7()


# In[ ]:





# In[ ]:




