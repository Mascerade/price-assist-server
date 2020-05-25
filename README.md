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
* **Rakuten**
* **Target**

# How to Use the API

The API accepts 4 parameters:
 
 * The name of the retailer (string)
 * The price of the product at the retailer (string)
 * The item identifier/item model used to search the product on a variety of retailers (string)
 * The return type, a.k.a whether the data would be represented as a *gui* or *json*
 
Example:
 * http://timeless-apps.com/price-assist/api/network-scrapers?retailer=Amazon&price=$369.99&item_model=BX80684I79700K&title=Intel%20Core%20i7-9700K%20Desktop%20Processor%208%20Cores%20up%20to%204.9%20GHz%20Turbo%20unlocked%20LGA1151%20300%20Series%2095W&return_type=gui
   * Network scrapers scrape off of **Amazon**, **Walmart**, **Newegg**, **Ebay**, **Microcenter**, **Jet**, **Outlet PC**, **Tigerdirect**, **SuperBiiz**, **B&H**
 * http://timeless-apps.com/price-assist/api/process-scrapers?retailer=Amazon&price=$369.99&item_model=BX80684I79700K&title=Intel%20Core%20i7-9700K%20Desktop%20Processor%208%20Cores%20up%20to%204.9%20GHz%20Turbo%20unlocked%20LGA1151%20300%20Series%2095W&return_type=gui
   * Process scrapers scrape off of **BestBuy**, **Rakuten**, **Target**
# Goals

* Create a very modular design which allows the addition of retailers to be swift ✅
* Support a wide range of retailers ✅
* Generate the HTML for the information for the Price Assist GUI ✅
* Be able to get the same exact product on different retailers (working on algorithms for this) ❌
 
# Notes

* Amazon seems to have blocked almost all of the US tor exit nodes
   * Going to try to use other countries' tor exit nodes

* When getting prices and product addresses from Amazon, be sure to first get the "card" and then retrieve the product price and address from that card
   * What can happen is that some products listed will not have a price attributed to it, so it will just skip them
   * This could mean inaccurate products are sent

* Certain item models actually have a mf-ing space in them, so we might not be able to replace the spaces in them with nothing

