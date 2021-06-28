#!/usr/bin/env python
# coding: utf-8

# # 0. Импорт библиотек

# In[1]:


import pandas as pd


# # 1. Загрузка данных

# In[2]:


df_titanic = pd.read_csv('train.csv')


# In[3]:


df_titanic


# # 2. Предобработка данных - поиск и обработка NaN значений

# ### 2.1. Поиск NaN значений:

# In[4]:


df_titanic.isnull().sum()


# #### Видим, что NaN значения встречаются в столбцах "Age", "Cabin" и "Embarked". Чтобы не нарушить смысл и качество данных, заменим NaN значения в столбце "Age" на среднее значение возраста для женщин и среднее значение возраста для мужчин. 
# 
# #### Что касается кабин, то данный столбец никак не влияет на решение данной задачи, поэтому просто заменим NaN значение столбца "Cabin" на слово "неизвестно".
# 
# #### Для столбца "Embarked" пойдем через поиск самого популярного значения, и заменим этим значением NaN-значения.

# ### 2.2. Обработка NaN значений:

# ### 2.2.1. Ищем средний возраст женщин и мужчин:

# In[5]:


# средний возраст женщин:
AvgAgeFemale = df_titanic[df_titanic['Sex'] == 'female']['Age'].mean()
print('Средний возраст женщин:',round(AvgAgeFemale,2))

# средний возраст мужчин:
AvgAgeMale = df_titanic[df_titanic['Sex'] == 'male']['Age'].mean()
print('Средний возраст мужчин:', round (AvgAgeMale, 2))


# ### Производим замену NaN значений в столбце "Age" для женщин на средний возраст женщин и для мужчин на средний возраст для мужчин:

# In[6]:


df_without_NaN  = df_titanic.copy()
df_without_NaN['Age'] = df_without_NaN['Age'].fillna((df_without_NaN[df_without_NaN['Sex'] == 'female']['Age'].mean()))
df_without_NaN['Age'] = df_without_NaN['Age'].fillna((df_without_NaN[df_without_NaN['Sex'] == 'male']['Age'].mean()))
df_without_NaN


# ### 2.2.2. Заменим NaN значения для столбца "Cabin" на слово "неизвестно":

# In[7]:


df_without_NaN['Cabin'] = df_without_NaN['Cabin'].fillna('неизвестно') 
df_without_NaN


# ### 2.2.3. Найдем самый популярный Embarked:

# In[8]:


df_without_NaN['Embarked'].value_counts()


# ### Заменим NaN на S (это самый популярный Embarked):

# In[9]:


df_without_NaN['Embarked'] = df_without_NaN['Embarked'].fillna('S') 
df_without_NaN


# ### 2.3. Проверяем, что NaN значения удалены:

# In[10]:


df_without_NaN.isnull().sum()


# # 3. Фильтрация данных

# ### Добавление столбца для группировки по возрасту:

# In[11]:


dfg = df_without_NaN


# In[12]:


dfAg = dfg.copy()
dfAg['age_group'] = dfg['Age'].apply(lambda x: '<=30' if x<=30 else '>30')
dfAg


# ### Группировка людей по полу и возрасту. Определение доли выживших в каждой группе:

# In[13]:


df_plot = dfAg.groupby(['Sex','age_group']).Survived.mean()
df_plot


# # 4. Визуализация данных

# In[14]:


df_plot.plot.bar()


# # 5. Выводы:

# ### Выживаемость выше среди женщин. Как видим на графике, больше всего выжило женщин старше 30 лет. Второе место по числу выживаемости заняли женщины 30 и младше лет. Чем это можно объяснить? Вероятнее всего, тем, что женщин и детей пытались спасти в первую очередь. Для более глубокого анализа можно построить и другие графики. Например, число выживших в зависимости от класса.
