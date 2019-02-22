from newegg_scraper.newegg_scraper import NeweggProduct
from bestbuy_scraper.bestbuy_scraper import BestBuy
from walmart_scraper.walmart_scraper import Walmart
from bandh_scraper.bandh_scraper import BandH
from ebay_scraper.ebay_scraper import Ebay
from tigerdirect_scraper.tigerdirect_scraper import TigerDirect
from microcenter_scraper.microcenter_scraper import Microcenter
from target_scraper.target_scraper import TargetScraper
from rakuten_scraper.rakuten_scraper import Rakuten
from jet_scraper.jet_scraper import Jet
from outletpc_scraper.outletpc_scraper import OutletPC


class ScraperHelpers:
    def __init__(self):
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

    @staticmethod
    def retrieve_newegg_data(item_model):
        newegg = NeweggProduct(item_model)
        newegg.retrieve_product_address()
        newegg.retrieve_product_price()
        global newegg_data
        newegg_data.append("Newegg")
        newegg_data.append(newegg.price)
        newegg_data.append(newegg.product_address)
        newegg.get_elapsed_time()
        return

    @staticmethod
    def retrieve_bestbuy_data(item_model):
        bestbuy = BestBuy(item_model)
        bestbuy.retrieve_product_address()
        bestbuy.retrieve_product_price()
        global bestbuy_data
        bestbuy_data.append("BestBuy")
        bestbuy_data.append(bestbuy.price)
        bestbuy_data.append(bestbuy.product_address)
        bestbuy.get_elapsed_time()
        return

    @staticmethod
    def retrieve_walmart_data(item_model):
        walmart = Walmart(item_model)
        walmart.retrieve_product_address()
        walmart.retrieve_product_price()
        global walmart_data
        walmart_data.append("Walmart")
        walmart_data.append(walmart.price)
        walmart_data.append(walmart.product_address)
        walmart.get_elapsed_time()
        return

    @staticmethod
    def retrieve_bandh_data(item_model):
        bandh = BandH(item_model)
        bandh.retrieve_product_address()
        bandh.retrieve_product_price()
        global bandh_data
        bandh_data.append("B&H")
        bandh_data.append(bandh.price)
        bandh_data.append(bandh.product_address)
        bandh.get_elapsed_time()
        return

    @staticmethod
    def retrieve_ebay_data(item_model):
        ebay = Ebay(item_model)
        ebay.retrieve_product_price()
        global ebay_data
        ebay_data.append("Ebay")
        ebay_data.append(ebay.price)
        ebay_data.append(ebay.product_address)
        ebay.get_elapsed_time()
        return

    @staticmethod
    def retrieve_tiger_direct_data(item_model):
        tiger = TigerDirect(item_model)
        tiger.retrieve_product_address()
        tiger.retrieve_product_price()
        global tiger_direct_data
        tiger_direct_data.append("Tiger Direct")
        tiger_direct_data.append(tiger.price)
        tiger_direct_data.append(tiger.product_address)
        tiger.get_elapsed_time()
        return

    @staticmethod
    def retrieve_microcenter_price(item_model):
        micro = Microcenter(item_model)
        micro.retrieve_product_address()
        micro.retrieve_product_price()
        global microcenter_data
        microcenter_data.append("Microcenter")
        microcenter_data.append(micro.price)
        microcenter_data.append(micro.product_address)
        micro.get_elapsed_time()
        return

    @staticmethod
    def retrieve_target_price(item_model):
        target = TargetScraper(item_model)
        target.retrieve_product_price()
        global target_data
        target_data.append("Target")
        target_data.append(target.price)
        target_data.append(target.product_address)
        return

    @staticmethod
    def retrieve_rakuten_price(item_model):
        rakuten = Rakuten(item_model)
        rakuten.retrieve_product_address()
        rakuten.retrieve_product_price()
        global rakuten_data
        rakuten_data.append("Rakuten")
        rakuten_data.append(rakuten.price)
        rakuten_data.append(rakuten.product_address)
        rakuten.get_elapsed_time()
        return

    @staticmethod
    def retrieve_jet_price(item_model):
        jet = Jet(item_model)
        jet.retrieve_product_address()
        jet.retrieve_product_price()
        global jet_data
        jet_data.append("Jet")
        jet_data.append(jet.price)
        jet_data.append(jet.product_address)
        jet.get_elapsed_time()
        return

    @staticmethod
    def retrieve_outletpc_price(item_model):
        outletpc = OutletPC(item_model)
        outletpc.retrieve_product_address()
        outletpc.retrieve_product_price()
        global outletpc_data
        outletpc_data.append("OutletPC")
        outletpc_data.append(outletpc.price)
        outletpc_data.append(outletpc.product_address)
        outletpc.get_elapsed_time()
        return
