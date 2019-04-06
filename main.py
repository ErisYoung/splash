import requests as rq
from urllib.parse import quote

lua="""
function main( splash,args )
    local treat=require("treat")
    splash:go("http://quotes.toscrape.com/")
    splash:wait(0.5)
    items=splash:select_all(".quote .text")
    results={}
    for i,v in ipairs(items) do
        results[i]=v.node.innerHTML
    end
    return treat.as_array(results)
end
"""

url="http://192.168.99.100:8050/"
res=rq.get(url+"execute?lua_source="+quote(lua))
print(res.text)