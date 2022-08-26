https://docs.djangoproject.com/

https://v4.bootcss.com/

https://v4.bootcss.com/docs/examples/floating-labels/

python manage.py runserver

python manage.py makemigrations

python manage.py migrate


``` python
a = [i for i in range(10)]
print(a)
```
## dd
# d

``` plantuml
@startmindmap
<style>
mindmapDiagram {
    node {
        BackgroundColor lightGreen
    }
    :depth(1){
        BackgroundColor white
    }
    :depth(3){
        BackgroundColor white
    }
}
</style>

* 数据结构
** 线性表
*** 链式存储
*** 顺序存储
** 树
*** 哈夫曼树
*** 二叉线索树
** 图
*** 有向图
**** 有环
**** 无环
*** 无向图
-- 算法
--- 动态规划
--- 贪心
--- 分治


@endmindmap

```
``` plantuml
@startuml
(*) --> "Initialization"

if "Some Test" then
  -->[true] "Some Activity"
  --> "Another activity"
  -right-> (*)
else
  ->[false] "Something else"
  -->[Ending process] (*)
endif
@enduml
```

``` plantuml
@startuml
robust "Web 浏览器" as WB
concise "Web 用户" as WU

@0
WU is 空闲
WB is 空闲

@100
WU is 等待中
WB is 处理中

@300
WB is 等待中
@enduml
```
