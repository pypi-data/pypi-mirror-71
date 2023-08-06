# Introduction
This library provides a pure Python interface for a Generalized Recommendation system.

## Recommender Systems
Recommender Systems are algorithms aimed at suggesting relevant items to users (items being products to buy, movies to watch, text to read or anything else depending on industries). There exist two major categories of methods 
1. Content based methods
2. Collaborative filtering methods

#### Content Based Recommendation
Content based approaches use additional information about users and/or items. The major idea of content based methods is to try to build a model, based on the available “features”, that explain the observed user-item interactions.

#### Collaborative Filtering Methods
Collaborative methods for recommender systems are methods that are based solely on the past interactions recorded between users and items in order to produce new recommendations. 



# Installing

> pip install py-recommendation




# Usage



## Module Import

```python
import py_recommendation as prc
```



## Fetch the Input Data
Generate input data object which can be used for various types of recommendations available


#### Items Data
```python
itemsInitialise = prc.InputData()
```
Configure Data
```python
ItemData = itemsInitialise.setData(
    data = 'variable carrying items data as either of dict, list of dicts or a pandas dataframe ',
    itemNameField = 'field name in data variable, carrying the item name/id',
    itemTagField = 'field name in data variable, carrying the item features',
    )
```

Or else set data from file,
```python
ItemData = itemsInitialise.setData_file(
    filePath = 'path to the data file',
    itemName_col = 'column name carrying the item name/id',
    itemTag_col = 'column name carrying the item features',
    fileType = 'type of file (xlsx/csv)'
    )
```

#### Users Data
```python
usersInitialise = prc.UsersData()
```
Configure Data
```python
UsersData = usersInitialise.setData(
    data = 'variable carrying users data as either of dict, list of dicts or a pandas dataframe ',
    userNameField = 'field name in data variable, carrying the user name/id',
    triedItemField = 'field name in data variable, carrying the list of items tried by the user',
    )
```

## Recommeder based on Similar Items
This is used to find other items similar to the given item based on the features.

```python
similarItemInit = prc.SimilarItem(ItemData)
recommendation = similarItemInit.similarItem('Item name/id')
```

## Content-based Recommeder for specific users based on items tried
```python
contentRecommendInit = prc.UserContent(itemData=ItemData, usersData=UsersData)
recommendation = contentRecommendInit.contentRecomend('name/id of a specific user (present in UsersData)')
```


**recommendation** carries a list with each recommended items and their recommendation score on 100
NB: * **recommendation** might have items with negative score which implies the item is already tried. This scenario occurs only if you have less number of items in 'ItemData'*



