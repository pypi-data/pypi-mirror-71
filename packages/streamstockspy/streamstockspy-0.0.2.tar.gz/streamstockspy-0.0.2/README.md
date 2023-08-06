Hello and thank you for downloading Stocks library.
This library is open source and allow users to get live and historical data.
# Installation

For install it: 
	
	pip install streamstockspy
	
For import it:

	from streamstockspy import stocks
	
	
# How that function?

The code will just stream website as yahoofinance for get data in realtime. For historical part i used the library yfinance. 

## First step:

The first think is to define a Stocks object. For example: MyFirtsStocks = stocks.Stocks()

## Second step:

The next step is to choose a company. For that, two options:

1.First option:
 
 - Use internal data: in the library i give some companys inside the library. You can have an access to them using tab. 

2.Second option:

 - If you want to add an other company or if the default website have latences and you prefer use an other reference website for stream you can use the method add as follow: MyFirstsStocks.add("NameOfTheCompany"*,"UrlOfTheLiveWebSite"*,"UrlOfYahooPageOfCompanyForHistoric","TheDivClass",[FirstPosition,LastPosition]) where all argument with * are obligatory and other without * are obtional. 
			
- NameOfTheCompany is the name that you want to give to the company.
- UrlOfTheLiveWebSite is the url of the website where appear the value. for example: https://finance.yahoo.com/quote/AAPL?p=AAPL
- UrlOfYahooPageOfCompanyForHistoric is the Url of the yahoo finance page of your company. for apple it's still https://finance.yahoo.com/quote/AAPL?p=AAPL
 For TheDivClass, it's, when you go on an other website (here i will continue with yahoo example), if you use chrome (that function also with other navigators but i dont know the exact command), you can right click on the value and select inspect (ctrl+maj+i).  
			  Now you are a able to see the source code of the page center on the value of the company. You have to search a <div class => which englobe your <span ...= value> and you have to copy past the name of the div class and give it to TheDivClass.
			  let's see for our apple example on yahoo finance. (https://finance.yahoo.com/quote/AAPL?p=AAPL) So write click and inspect on the value that we are looking for.
			  search a div class which englobe the span value. we can for example choose <div class="My(6px) Pos(r) smartphone_Mt(6px)" data-reactid="29>. so you have to set TheDivClass = "My(6px) Pos(r) smartphone_Mt(6px)"
			- position is a list. For some website they will not just have one value but maybe a string element like "campany name - value". Position allow you to select just value inside this string.


**Let's see an example an example**  which take into account all parameters:  	


	MyFirstStocks.add('Airbus','https://www.boursier.com/actions/cours/airbus-group-ex-eads-NL0000235190,FR.html','https://finance.yahoo.com/quote/AIR.PA/','col col-12', [-7,-1])

For understand what happen in this example, i invite you, in the first time to add it without the position list and to write:

	MyFirstStocks.Airbus['RealTime'].value(print_disable = False)
	
You will see what the code get from the website. After that readd Airbus and add the position list and do the test again. 

## Thrid step:

Play with the labrary! Now you have your company. You can choose the live in writing MyFirstStocks.Airbus['RealTime'] or historical data in writing MyFirstStocks.Airbus['Historic'] but of course if you just do that, you will see nothing. You should add a method depending to what you want to do. For example if you want the actual value of Airbus, you have to write: MyFirstStocks.Airbus['RealTime'].value()
		
### All methods available:	
				
1.RealTime:
				
 - value() for get value.  
 - plot() for plot.
 - set_alert(Lower_limit,Higher_limit) for set limit and have a notification if one limit is break.
 - stop_alert() stop the alert routine.

2.Historic:
			
 - ID() for get the ID of the company (Fore Apple its AAPL)
 - plot() for have an interactive plot on your browser.


Note that all the library is do for work in background. by the way, that allow you to launch an alert or a live plot without block your python console. you still can use your python and let this code work in background. 

Do not hesitate if you find some issus. I will do my best for correct them. 
 			  

			