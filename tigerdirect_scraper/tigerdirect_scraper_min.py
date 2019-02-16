from bs4 import BeautifulSoup #line:1
import urllib .request #line:2
class TigerDirect :#line:5
    def __init__ (OO000O00000O0000O ,OOO00OO0O0OO0000O ):#line:6
        OO000O00000O0000O .price =""#line:7
        OO000O00000O0000O .product_model =OOO00OO0O0OO0000O #line:8
        OO000O00000O0000O .product_address ='http://www.tigerdirect.com/applications/SearchTools/search.asp?keywords={}'.format (OOO00OO0O0OO0000O )#line:9
        OO000O00000O0000O .headers ={'User-Agent':'Googlebot/2.1 (+http://www.google.com/bot.html)'}#line:12
    def retrieve_price (O0000OOO00OO00O0O ):#line:14
        try :#line:16
            OO0000O0OO00O0OOO =urllib .request .Request (O0000OOO00OO00O0O .product_address ,headers =O0000OOO00OO00O0O .headers )#line:17
            OO0000O0OO00O0OOO =urllib .request .urlopen (OO0000O0OO00O0OOO ).read ()#line:18
            OOOO00OOO0000O00O =BeautifulSoup (OO0000O0OO00O0OOO ,"html.parser")#line:19
            O0000OOO00OO00O0O .price =OOOO00OOO0000O00O .find ('div','salePrice').text #line:20
            OOO0O00OOOOOO0O0O =OOOO00OOO0000O00O .find ('span','oldPrice').text #line:21
            O0000OOO00OO00O0O .price =O0000OOO00OO00O0O .price .replace (OOO0O00OOOOOO0O0O ,'')#line:22
        except AttributeError as O00000O0OOOO000O0 :#line:24
            O0000OOO00OO00O0O .price ="Could not find price"#line:25
