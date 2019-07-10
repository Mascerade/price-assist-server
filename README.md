# Price Assist Server

The goal of this server is to scrape retailers in order to get information about the price of product equivalent to the product identifier put into it. For example, if you put in a product from Newegg, it will get the equivalent product prices from retailers supported.

The retailers supported are:
* **Amazon**
* **Walmart**
* **BestBuy**
* **Newegg**
* **Ebay**
* **Microcenter**
* **Jet**
* **Outlet PC**
* **TigerDirect**
* **SuperBiiz**
* **B&H**
* **Rakuten** (Coming soon. Requires a caching system to be efficient because it requires to be scraped using Selenium)
* **Target** (Coming soon. Requires a caching system to be efficient because it requires to be scraped using Selenium)

# How to Use the API

The API accepts 4 parameters:
 
 * The name of the retailer (string)
 * The price of the product at the retailer (string)
 * The item identifier/item model used to search the product on a variety of retailers (string)
 * The return type, a.k.a whether the data would be represented as a *gui* or *json*
 
Example:
 * http://timeless-apps.com/api/query?retailer=Newegg&price=525&item_model=BX80684I99900K&return_type=gui
 
# Goals

* Create a very modular design which allows the addition of retailers to be swift ✅
* Support a wide range of retailers ✅
* Generate the HTML for the information for the Price Assist GUI ✅
* Be able to get the same exact product on different retailers (working on algorithms for this) ❌
 
