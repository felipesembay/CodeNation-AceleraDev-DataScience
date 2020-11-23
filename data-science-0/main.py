#!/usr/bin/env python
# coding: utf-8

# # Desafio 1
# 
# Para esse desafio, vamos trabalhar com o data set [Black Friday](https://www.kaggle.com/mehdidag/black-friday), que reúne dados sobre transações de compras em uma loja de varejo.
# 
# Vamos utilizá-lo para praticar a exploração de data sets utilizando pandas. Você pode fazer toda análise neste mesmo notebook, mas as resposta devem estar nos locais indicados.
# 
# > Obs.: Por favor, não modifique o nome das funções de resposta.

# ## _Set up_ da análise

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


black_friday = pd.read_csv("black_friday.csv")


# ## Inicie sua análise a partir daqui

# In[3]:


black_friday


# In[4]:


bfe = pd.DataFrame({'type': black_friday.dtypes,
                            'amount': black_friday.isna().sum(),
                            'percentage': (black_friday.isna().sum() / black_friday.shape[0]) * 100})
                            

bfe


# ## Questão 1
# 
# Quantas observações e quantas colunas há no dataset? Responda no formato de uma tuple `(n_observacoes, n_colunas)`.

# In[5]:


def q1():
    return (black_friday.shape)
    pass


# ## Questão 2
# 
# Há quantas mulheres com idade entre 26 e 35 anos no dataset? Responda como um único escalar.

# In[6]:


def q2():
    return len(black_friday[(black_friday['Gender'] == 'F') & (black_friday['Age'] == '26-35')])
    pass


# ## Questão 3
# 
# Quantos usuários únicos há no dataset? Responda como um único escalar.

# In[7]:


def q3():
    return black_friday['User_ID'].nunique()
    pass


# ## Questão 4
# 
# Quantos tipos de dados diferentes existem no dataset? Responda como um único escalar.

# In[8]:


def q4():
    return black_friday.dtypes.nunique()
    pass


# ## Questão 5
# 
# Qual porcentagem dos registros possui ao menos um valor null (`None`, `ǸaN` etc)? Responda como um único escalar entre 0 e 1.

# In[9]:


def q5():
    return float(black_friday[black_friday.isna().any(axis=1) == True].shape[0]/black_friday.shape[0])
    pass


# ## Questão 6
# 
# Quantos valores null existem na variável (coluna) com o maior número de null? Responda como um único escalar.

# In[10]:


def q6():
    df_na_values = black_friday.isna()
    df_na_count = df_na_values.apply(pd.Series.value_counts).loc[True]
    return int(df_na_count.max())
    pass


# ## Questão 7
# 
# Qual o valor mais frequente (sem contar nulls) em `Product_Category_3`? Responda como um único escalar.

# In[11]:


def q7():
    return int(black_friday['Product_Category_3'].dropna().mode())
    pass


# ## Questão 8
# 
# Qual a nova média da variável (coluna) `Purchase` após sua normalização? Responda como um único escalar.

# In[12]:


def q8():
    df = black_friday['Purchase']
    normalized =(df-df.min())/(df.max()-df.min())
    return float(normalized.mean())
    pass


# ## Questão 9
# 
# Quantas ocorrências entre -1 e 1 inclusive existem da variáel `Purchase` após sua padronização? Responda como um único escalar.

# In[13]:


def q9():
    df_purchase = black_friday['Purchase']
    df_purchase_zscore = (df_purchase - df_purchase.mean())/df_purchase.std(ddof=0)
    return int(len(df_purchase_zscore[(df_purchase_zscore > -1) & (df_purchase_zscore < 1)]))
    pass


# ## Questão 10
# 
# Podemos afirmar que se uma observação é null em `Product_Category_2` ela também o é em `Product_Category_3`? Responda com um bool (`True`, `False`).

# In[14]:


def q10():
    df = black_friday[['Product_Category_2', 'Product_Category_3']]
    df = df[df['Product_Category_2'].isna()]
    return df['Product_Category_2'].equals(df['Product_Category_3'])
    pass


# In[ ]:




