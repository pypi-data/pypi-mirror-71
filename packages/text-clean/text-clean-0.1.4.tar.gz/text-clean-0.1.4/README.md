#text-clean
Process text for NLP.


## how to use
```python
from text_clean import TextClean


tc = TextClean()

_str = "繁 體 字是smasd ❶ ❷ ❸ ❹ 艹艹艹艹 艹艹艹艹nm 夶彩呗我 幹什麼 □ ■ ◇ ◆ − ++++++++ ⑪ ⑫ ⑬  ⒍ ⒎ ⒏ ⒐ W,X  asd鬼东 西錯 鍼٩(๑ᵒ̴̶͈᷄ᗨᵒ̴̶͈᷅)و q🕓🕛"

print(tc.clean(_str))

# output
# 繁体字是smasd1234艹艹艹nm大大彩呗我干什么+++1112136789wxasd鬼东西错针q
```