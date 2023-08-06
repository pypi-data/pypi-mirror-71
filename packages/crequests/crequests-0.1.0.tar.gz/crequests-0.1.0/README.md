# A python library for caching data while scraping using the famous requests-module

Often when scraping, something goes wrong. In order to minimize the burden on the website you are scraping, its a good idea to cache the data. This library does all this transparently. 

With this module you create an instance of Crequests (which inherits from requests.Session). With this instance you can use all the standard methods of requests.Session. In the background all the magic caching happens, while you use all the wellknown methods of the request library

Have a look in the examples folder, to see how easy it is to use.