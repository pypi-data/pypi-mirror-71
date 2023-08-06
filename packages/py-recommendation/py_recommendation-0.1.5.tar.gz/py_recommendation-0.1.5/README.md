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
itemsInitialise = prc.ItemData()
```
Configure Data
```python
# Reffer from sample data given below:
sample_items_data = {"title":['Place-A','Place-B','Place-C','Place-D','Place-E','Place-F','Place-G'],
            "tags":[
                'party & dance, nightlife, food, bar & restaurant, enjoy family',
                'Historic old monument, landmarks & enjoy$ beautiful',
                'Beach party, bar & nightlife @water, Beautiful',
                'Old Historic Temple, peaceful & rest, Family vacation',
                'Nature waterfall & green, beauty water',
                'Beautiful Himalaya hills, nature snow, water & peace',
                'Sights & Landmarks, Monuments & Statues'
            ]
           }
itemData = itemsInitialise.setData(
    data = sample_items_data,
    itemNameField = 'title',
    itemTagField = 'tags',
    )
```

Or else set data from file,
```python
itemData = itemsInitialise.setData_file(
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
# Reffer from sample data given below:
sample_users_data = {"names":['Professor','Lisbon','Berlin','Nairobi','Helsinki','Rio'],
            "visited":[
                ['Place-B','Place-D'],
                ['Place-D','Place-E'],
                ['Place-B'],
                ['Place-C','Place-E'],
                ['Place-F'],
                ['Place-A', 'Place-F']
            ]
           }

usersData = usersInitialise.setData(
    data = sample_users_data,
    userNameField = 'names',
    triedItemField = 'visited',
    )
```

## Recommeder based on Similar Items
This is used to find other items similar to the given item based on the features.

```python
similarItemInit = prc.SimilarItem(itemData)
recommendation = similarItemInit.similarItem('Place-D')
```

## Content-based Recommeder for specific users based on items tried
```python
contentRecommendInit = prc.UserContent(itemData=itemData, usersData=usersData)
recommendation = contentRecommendInit.contentRecomend('Lisbon')
```


* **recommendation** carries a list with each recommended items and their recommendation score on 100.
* **recommendation** might have items with negative score which implies the item is already tried. This scenario occurs only if you have less number of items in 'ItemData'



