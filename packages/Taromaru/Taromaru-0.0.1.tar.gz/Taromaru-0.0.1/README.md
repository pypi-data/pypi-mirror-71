#### A package for the Taromaru API.


##### Image Example:

```py
    from taromaru import taromaruInit

    taromaru = taromaruInit()
    taromaru.setapikey("YOUR API KEY HERE")

    results = await taromaru.image(type="kanna")

    print(results)
```

if above does not work, try this
```py
    from taromaru import taromaruInit
    import asyncio

    taromaru = taromaruInit()
    taromaru.setapikey("$2y$10$QsYwpCdEL04W4M6gh7CtOOV7NlUhjbIrGG7GTcx6R.FabclrVuG4m")

    loop = asyncio.get_event_loop()
    results = loop.run_until_complete(taromaru.image(type="kanna"))

    print(results)
```

:>