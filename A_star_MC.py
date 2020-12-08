# coding:utf-8
"""
人工智能A实验2 使用A*算法解决MC问题
荀镕基 1819660230
2020.12.8
"""
import operator
__metaclass__ = type

#状态空间的启发式搜索》》用状态+操作来表示
class State:    #左岸状态
    def __init__(self, m, c, b):
        self.m = m  #missionaries
        self.c = c  #cannibals
        self.b = b  # 左岸船的数量b=1
        # A*算法 f(n)不断增大,h(n)不断减小
        self.g = 0  # 实际代价
        self.h =0   # 启发式函数
        self.f =0  # 估计函数值
        self.father = None  #父节点指针
        self.node = [m, c, b]   #状态的列表


def safe(s):
    if s.m > M or s.m < 0 or s.c > C or s.c < 0 or\
            (s.m != 0 and s.m < s.c) or (s.m != M and M - s.m < C - s.c):   #修道士人数《野人
        return False
    else:
        return True

# 启发式函数
def h_qifa(s):   #m+c-2b
    return s.m + s.c - K * s.b

def equal(a, b):
    if a.node == b.node:
        return True

def back(new, s):  # 判断s.father是否与new重复
    if s.father is None:
        return False
    return equal(new, s.father)


def open_sort(l):
    the_key = operator.attrgetter('f')  # 指定属性排序的key
    l.sort(key=the_key)


# 扩展节点时在open表和closed表中找原来是否存在相同mcb属性的节点
def in_list(new, l):
    for item in l:
        if new.node == item.node:
            return True, item
    return False, None


def A_star(s,K,goal_list):
    """
    A*算法：对A算法加限制》》f(子节点)>=f(父节点） and h(子节点)<=h(父节点）
    :param s:  初始结点
    :param K:  一条船最大载人数
    :param goal_list:   目标节点所有情况的列表》》当boat=1,只有（0，0，0）
    :return:
    """
    M,C,B=s.m,s.c,s.b

    global open_list, closed_list
    """1.初始结点s存入Open未扩展表"""
    open_list = [s]
    closed_list = []    #初始化Closed表，已经扩展结点

    g_cost=0; #代价值：step
    """2.若Open表空，无解退出"""
    while open_list:
        get=open_list[0]; """3.取出open表第一个元素get,放入Close表"""
        get.g=g_cost    #计算结点估计函数f，启发式函数值h
        get.h=h_qifa(get)
        if get.h<0: #启发式函数一定要大于0
            get.h=0
        get.f=get.g+get.h
        open_list.remove(get)  # 将get从open表移出
        closed_list.append(get)
        for goal in goal_list:
            """4.判断是否为目标节点》》若是目标点，直接返回"""
            if get.node == goal.node:
                return get

        """扩展结点get  判断”条件“是否放入openlist"""
        """选择上船的人，遍历所有可能之后用条件来筛选！！！！   若满足条件》》可以为下一个状态  注：当每条船最大人数可变》》需要考虑船上是否会被吃掉！！！"""
        ss=[]    #存放该层扩展的结点
        for i in range(M+1):  # 上船传教士
            for j in range(C+1):  # 上船野人
                if i + j == 0 or i + j > K*B:
                    continue
                if get.b == 1 and i<=get.m and j<=get.c:  # 船在左岸
                    new = State(get.m - i, get.c - j, 0)    #new为get状态下一个状态 >>先放入ss列表后再判断
                    print(new.node)
                    ss.append(new)
                elif get.b==0 and i<=M-get.m and j<=M-get.c:  # 船在右岸
                    new = State(get.m + i, get.c + j, 1)
                    ss.append(new)
                else:continue
                """5.扩展的子节点一定要满足：
                1.安全 2.估计函数f一定要>=f父节点 3.启发函数h一定要<=h父节点！！！"""
                new.father = get    #连接父节点
                new.g = get.g + 1
                new.h=h_qifa(new)
                new.f = new.g + new.h  # f = g + h
                if not safe(new or back(new, get))\
                        or not(new.f>=get.f and new.h<=get.h):  # 刚生成的new状态非法或new折返了>>从暂存的扩展列表删去
                    print(new)
                    ss.pop()

        if ss==[]:  #该层无扩展结点
            continue
        open_list.extend(ss)    #先全部加入open>>检查是否有(m,c,b)相同而f不同的》》取f最小的那个
        for new in ss:
            # 如果new在open表中(只关注m,c,b的值)，若当前的f更小，取最小的f
            if in_list(new, open_list)[0]:  #(0,0,0)执行？
                old = in_list(new, open_list)[1]
                if new.f < old.f:  # new的f<open表相同状态的f
                    open_list.remove(old)
                    open_list.append(new)
                    open_sort(open_list)    #可省去》》后面有排序
                else:
                    pass

        open_list = sorted(open_list, key=lambda Node: Node.f, reverse=False)  # 按估计函数值从小到大排序》》保证下次选的fmin
        g_cost+=1

def printPath(f):
    if f is None:
        return
    printPath(f.father)
    print("->"+str(f.node),end=" ")



if __name__ == '__main__':
    exp_note="""实验要求：1.共一条船,船一次最大运两个人;  2.任意输入M,C值 """
    print("Exp:使用A*算法实现MC问题~\n{}".format(exp_note))
    B, K = 1,2  #船数B=1，每船最大人数K=2
    M,C=eval(input("输入初始Missionary,Cannibal人数(','分割）：M,C="))

    init = State(M, C, B)  # 初始节点M,C,B》》左岸船数
    goal_list=[]    #【注】：当有多条船可能有多种目标点，但本实验中船数=1,goal只有一个(0,0,0)
    for b in range(B):#只要所有人过岸即可
        goal_list.append(State(0, 0, b))  # 目标
    final = A_star(init,K,goal_list)    #初始结点(M,C,b)=(3,3,1)
    if final:
        print('有解~!解为：')
        printPath(final)
    else:
        print('无解')