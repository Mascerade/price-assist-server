""" EXTERNAL IMPORTS """
from operator import itemgetter

"""" LOCAL IMPORTS """
from scrapers.amazon_scraper import Amazon
from scrapers.newegg_scraper import NeweggProduct
from scrapers.bestbuy_scraper import BestBuy
from scrapers.walmart_scraper import Walmart
from scrapers.bandh_scraper import BandH
from scrapers.ebay_scraper import Ebay
from scrapers.tigerdirect_scraper import TigerDirect
from scrapers.microcenter_scraper import Microcenter
from scrapers.target_scraper import TargetScraper
from scrapers.rakuten_scraper import Rakuten
from scrapers.jet_scraper import Jet
from scrapers.outletpc_scraper import OutletPC
from scrapers.superbiizz_scraper import SuperBiiz


class ScraperHelpers:
    
    iframe = """
    <div id="iframe-wrapper" style="visibility: visible; width: 100%; display: flex; justify-content: center; 
    align-items: center; transform: translateZ(0px); overflow: hidden; background-color: transparent; 
    z-index: 100000000; border: none;">
        <iframe id="iframe" class="scrollbar scrollbar-primary" style="height: 500px; width: 300px; border: none; border-radius: 10px;">
        </iframe>
    </div>
    """

    heading = """
        <style>
            ::-webkit-scrollbar {
                width: 10;
            }
            
            ::-webkit-scrollbar-track {
                background: #7D7D7D;
            }
            
            ::-webkit-scrollbar-thumb {
                background: #4D4D4D;
            }
            
            ::-webkit-scrollbar-thumb:hover {
                background: #555;
            }
        </style>
        <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons">
        <link rel="stylesheet" href="https://code.getmdl.io/1.3.0/material.indigo-pink.min.css">
        <link href="https://fonts.googleapis.com/css?family=Raleway:400,500" rel="stylesheet"> 
        <link rel="stylesheet" href="https://raw.githack.com/BinaryWiz/Price-Assist/master/css/retailers-popup.css"> 
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootswatch/4.2.1/lux/bootstrap.min.css">
    """

    def __init__(self):
        self.amazon_data = []
        self.newegg_data = []
        self.bestbuy_data = []
        self.walmart_data = []
        self.bandh_data = []
        self.ebay_data = []
        self.tiger_direct_data = []
        self.microcenter_data = []
        self.target_data = []
        self.rakuten_data = []
        self.jet_data = []
        self.outletpc_data = []
        self.biiz_data = []
        self.all_scrapers = []

    def retrieve_amazon_data(self, item_model):
        amazon = Amazon(item_model)
        self.amazon_data = amazon.retrieve_all_information()
        self.all_scrapers.append(self.amazon_data)
        return

    def retrieve_newegg_data(self, item_model):
        newegg = NeweggProduct(item_model)
        self.newegg_data = newegg.retrieve_all_information()
        self.all_scrapers.append(self.newegg_data)
        return

    def retrieve_bestbuy_data(self, item_model):
        bestbuy = BestBuy(item_model)
        self.bestbuy_data = bestbuy.retrieve_all_information()
        self.all_scrapers.append(self.bestbuy_data)
        return

    def retrieve_walmart_data(self, item_model):
        walmart = Walmart(item_model)
        self.walmart_data = walmart.retrieve_all_information()
        self.all_scrapers.append(self.walmart_data)
        return

    def retrieve_bandh_data(self, item_model):
        bandh = BandH(item_model)
        self.bandh_data = bandh.retrieve_all_information()
        self.all_scrapers.append(self.bandh_data)
        return

    def retrieve_ebay_data(self, item_model):
        ebay = Ebay(item_model)
        self.ebay_data = ebay.retrieve_all_information()
        self.all_scrapers.append(self.ebay_data)
        return

    def retrieve_tiger_direct_data(self, item_model):
        tiger = TigerDirect(item_model)
        self.tiger_direct_data = tiger.retrieve_all_information()
        self.all_scrapers.append(self.tiger_direct_data)
        return

    def retrieve_microcenter_price(self, item_model):
        micro = Microcenter(item_model)
        self.microcenter_data = micro.retrieve_all_information()
        self.all_scrapers.append(self.microcenter_data)
        return

    def retrieve_target_price(self, item_model):
        target = TargetScraper(item_model)
        self.target_data = target.retrieve_all_information()
        self.all_scrapers.append(self.target_data)
        return

    def retrieve_rakuten_price(self, item_model):
        rakuten = Rakuten(item_model)
        self.rakuten_data = rakuten.retrieve_all_information()
        self.all_scrapers.append(self.rakuten_data)
        return

    def retrieve_jet_price(self, item_model):
        jet = Jet(item_model)
        self.jet_data = jet.retrieve_all_information()
        self.all_scrapers.append(self.jet_data)
        return

    def retrieve_outletpc_price(self, item_model):
        outletpc = OutletPC(item_model)
        self.outletpc_data = outletpc.retrieve_all_information()
        self.all_scrapers.append(self.outletpc_data)
        return

    def retrieve_super_biiz_price(self, item_model):
        biiz = SuperBiiz(item_model)
        self.biiz_data = biiz.retrieve_all_information()
        self.all_scrapers.append(self.biiz_data)
        return

    def reset_retailer_lists(self):
        self.bestbuy_data = []
        self.newegg_data = []
        self.walmart_data = []
        self.bandh_data = []
        self.ebay_data = []
        self.tiger_direct_data = []
        self.microcenter_data = []
        self.target_data = []
        self.rakuten_data = []
        self.jet_data = []
        self.outletpc_data = []
    
    def add_source_retailer(self, retailer_info):
        self.all_scrapers.insert(0, retailer_info)

    def get_all_scrapers(self):
        return self.all_scrapers

    def remove_extraneous(self):
        """ Removes retailer products that don't have a price (For sorting) """
        length = len(self.all_scrapers)
        index = 0
        while index < length:
            try:
                float(self.all_scrapers[index][1].strip().lower().replace("$", "").replace(",", "")) 
            
            except ValueError:
                del self.all_scrapers[index]
                index = 0
                length -= 1
                continue

            index += 1
    
    def sort_all_scrapers(self):
        self.all_scrapers.sort(key=sort_by)

def sort_by(e):
    parameter = e[1]
    parameter = parameter.replace("$", "")
    parameter = parameter.replace(",", "")
    return float(parameter)
    