# -Missionary-Cannibal
Python_使用A*搜索算法实现MC问题
人工智能实验：
实验内容：在河的左岸有三个修道士，三个野人和一条船，修道士想用这条船把所有的人都运到河对岸,但要受到以下条件限制：修道士都会划船，但船一次只能装运两个人。在任何岸边野人数不能超过修道士，否则修道士会被野人吃掉。

1.启发式搜索A*算法，其可利用搜索过程中的中间信息来引导搜索过程向最优方向发展。

状态空间的启发式搜索
1.启发式信息 ：h(n)启发式函数
2.估价函数 f(n)=g(n)+h(n)

#全局择优搜索算法搜索过程：
1.初始结点放入Open表
2.Open表为空》无解，退出
3.取Open表第一个结N点放入Closed（已经排好序，是f(x)最小值）
4.考察N是否为目标结点
5.1)扩展结点N，计算子节点估价函数值f(n)>>指向父节点的指针，放入Open表
扩展的子节点一定要满足：1.安全 2.估计函数f一定要>=f父节点 
3.启发函数h一定要<=h父节点！！！
2)若结点N不可扩展》》转到2
6.Open表按f(n)从小到大排序
