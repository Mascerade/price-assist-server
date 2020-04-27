# Track Prices

This is a project that tracks the prices of products over time. Once a user visits a product page, the item model is added to this database. There are two parts to this project:

## Item Model Database 
This part of the project stores the item model of a product as the key and the title of the product as the value <br>
It is a **Plyvel** database instead of being part of the SQL database simply because I prefer it to making queries to a SQL database for simply key-value storage like this

### Usage
`GET` http://localhost:5003/item_model_data
* This returns a JSON where the key is the item model and the value is the title of the product
   * Example: `GET` http://localhost:5003/item_model_data
   * Return: `{item_model_1: title1, item_model_2: title2 ...}`

<hr>

`GET` http://localhost:5003/search_item_models?search='query'
* This returns a 3-part JSON:
   * First key is `sorted_similarity`
      * This is a dictionary of the item model as the key and the score returned by the cosine-similarity sorted highest to lowest
   * Second key is `title_to_item_model`
      * This is a dictionary of the titles of the products to the item model of the product
      * This is used on the front-end for Track Prices
   * Third key is `item_model_data`
      * This is the same output as `GET` http://localhost:5003/item_model_data
      * Again, it is need on the front-end for Track Prices

<hr>

`PUT` http://localhost:5003/item_model_data
* This allows for putting an item model associated with a title
* It expects a JSON that is `{item_model: ITEM_MODEL, title: TITLE}`

<hr>

`DELETE` http://localhost:5003/item_model_data
* THIS SHOULD **NEVER** BE USED IN PRODUCTION
* This is just a good testing tool
* Expects a JSON that is `{item_model:  ITEM_MODEL}`
* Will delete it from the Plyvel database of item models and titles

## SQL Database
This database is the one that actually stores the retailer data. Each table uses an item model to identify it and its values are each retailer supported by Price Assist, along with the date. <br>
The date is used for the x-axis of the graph for the Track Prices front-end

### Usage

`GET` http://localhost:5003/item_model=ITEM_MODEL
* Returns a list of dictionaries where there is the data and each retailer along with the price (as a number).
* The last value of the list is just the title.

`PUT` http://localhost:5003/
* The data should be in the form:
```
{
  'item_model': ITEM_MODEL
  'data': {
    'amazon_data': price1,
    'newegg_data': price2,
    'walmart_data': price3,
    ...
  }
}
```
* Essentially, the 'data' part of the JSON is just the output from the Price Assist server
* It puts the data into the SQL database, and also adds the date to the data

`DELETE` http://localhost:5003/item_model=ITEM_MODEL
* Deletes the table in the SQL database with the item model as the name
* Also deletes the item model from the Plyvel database