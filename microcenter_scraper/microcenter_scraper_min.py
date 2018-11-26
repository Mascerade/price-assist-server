from bs4 import BeautifulSoup #line:1
import urllib .request #line:2
class Microcenter :#line:5
    def __init__ (OOOOOOO0O000O00O0 ,OO00O0OOO0O0O0OO0 ):#line:6
        OOOOOOO0O000O00O0 .price =""#line:7
        OOOOOOO0O000O00O0 .product_model =OO00O0OOO0O0O0OO0 #line:8
        OOOOOOO0O000O00O0 .product_address ='https://www.microcenter.com/search/' 'search_results.aspx?Ntt={}'.format (OO00O0OOO0O0O0OO0 )#line:10
        OOOOOOO0O000O00O0 .headers ={'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X x.y; rv:42.0) Gecko/20100101 Firefox/42.0',}#line:13
    def retrieve_price (O000OO0OO0OO00O00 ):#line:15
        try :#line:16
            OOO000OO0000O000O =urllib .request .urlopen (O000OO0OO0OO00O00 .product_address )#line:17
            OOO000OO0000O000O =OOO000OO0000O000O .read ()#line:18
            O0OO0OOO00000OOO0 =BeautifulSoup (OOO000OO0000O000O ,"lxml")#line:19
            O000OO0OO0OO00O00 .price =O0OO0OOO00000OOO0 .find ('span',{"itemprop":"price"}).text #line:20
        except AttributeError :#line:22
            O000OO0OO0OO00O00 .price ="Could not find price"
