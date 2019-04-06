function main( splash,args )
    local example_urls = {'www.baidu.com','www.taobao.com','www.zhihu.com'}
    local urls=args.urls or example_urls
    local results={}
    for i,v in ipairs(example_urls) do
        local ok,reason=splash:go("http://" .. v)
        if ok then
            splash:wait(2)
            results[v]=splash:png()
        end
    end
    return results
end


function main( splash,args )
    local snapshots={}
    local timer=splash:call_later(function()
        snapshots['a']=splash:png()
        splash:wait(1.0)
        snapshots['b']=splash:png()
    end,0.2)
    splash:go("https://www.taobao.com")
    splash:wait(3.0)
    return snapshots
end