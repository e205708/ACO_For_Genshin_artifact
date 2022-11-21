import set_points_information
import random

#配列の添字の関係上、ノード番号は実際の番号-1で表現することにする。

class ant:
    def __init__(self,pheromone_amount=10):
        self.now_node = 15 #現在いるノードの番号
        self.passed_nodes = [self.now_node] #経過したノード
        #self.is_finished = False #回るべきノードを全て回り切ったかどうか
        self.pheromone_amount = pheromone_amount #1サイクルで付着させるフェロモン量

def get_pheromone_affect(fr,pheromone_list,candidate_for_nodes):
    """
    フェロモン効果の値を調べる
    fr : from(int)
    pheromone_list : 現在のフェロモン量のリスト(list)
    candidate_for_nodes : 移動先の候補(list)

    return
    pheromone_affect_values : フェロモン効果の値、移動先の候補と順番が対応している(list)
    """
    edge_pheromones = [] #移動先の候補のフェロモン量を順番に入れる
    pheromone_affect_values = [] #フェロモン効果の量を調べる

    sum_of_pheromone = 0
    for n in candidate_for_nodes:
        phe_amount = pheromone_list[fr][n]
        edge_pheromones.append(phe_amount)
        sum_of_pheromone = sum_of_pheromone + phe_amount
    
    if sum_of_pheromone == 0: #もしどのエッジにもフェロモンがついていない場合、全て同じ値を返す。
        tmp_value = 1/len(candidate_for_nodes)
        for _,_ in enumerate(candidate_for_nodes):
            pheromone_affect_values.append(tmp_value)
    else:
        for p in edge_pheromones:
            pheromone_affect_values.append(p/sum_of_pheromone)
    
    return pheromone_affect_values
    
    

def get_heuristic_value(fr,candidate_for_nodes,passed_times,warp_point,weight_warp_point=20):
    """
    ヒューリスティック値を求める

    ワープポイントへの移動時間は、他のノード間の移動時間より短いため、
    比較的選択されやすい。ワープポイントは必ずしも通過する必要なないため、
    優先度を下げるために、ランダムでヒューリスティック値を下げることにする。

    fr : from(int)
    candidate_for_nodes : 移動先の候補(list)
    passed_times : ノード間の移動時間(list)
    warp_point : ワープポイントへの移動かどうかを調べる(list)

    return
    heuristic_values : 移動先の候補のヒューリスティック値
    """

    heuristic_values = [] #移動先の候補のヒューリスティック値を順番に入れる

    for n in candidate_for_nodes:
        passed_time = passed_times[fr][n]
        if (n not in warp_point): 
            heuristic_values.append(1/passed_time)
        elif n in warp_point:
            #ワープポイントへの移動の際には、ランダムで移動時間を増やす
            heuristic_values.append(1/(passed_time + weight_warp_point ))

    return heuristic_values


def cycle_step(ants,time_between_edges,alpha,beta,pheromone_on_edges,nodes_of_warp_point,pheromone_evap_rate):
    """
    一定の回数ノード間の移動を行う、または、回る必要がある全てのノードを回り切るまで、
    アリの経路選択->各エッジのフェロモン更新を行う。

    ants : アリオブジェクトのリスト(list)
    time_between_edges : エッジを移動するためにかかる移動時間
    alpha : フェロモン効果の強度を決める
    beta : ヒューリスティック値の強度を決める
    pheromone_on_edges : エッジ上にあるフェロモンの量
    nodes_of_warp_point : ワープポイントであるノード
    pheromone_evap_rate : フェロモン蒸発率
    """

    limit_step_times = 30 #ノード間を移動できる最大の回数

    finished_ants = [] #全ての回るべき場所を回ったあり
    for _ in range(limit_step_times):
        
        #現在エッジに付着している、フェロモンを蒸発させる
        for row_order,phe in enumerate(pheromone_on_edges):
            for column_order,p in enumerate(phe):
                pheromone_on_edges[row_order][column_order] = p*pheromone_evap_rate

        #アリの経路選択、移動
        for ant in ants:
            nodes_selectable = [] #移動可能なノード先
            select_probability = [] #各ノードが選択される確率

            ant = ant[0] #antはオブジェクトのつもりだったけど要素数1のリスト扱いだったため取り出す

            if len(ants) != 0: #まだ探索し終えていないありが存在する場合
                if ant.now_node in nodes_of_warp_point and False:
                    #ワープポイント->ワープポイントの移動を制限する(2->1->2ときた時に詰むので廃止。)
                    for order,e in enumerate(time_between_edges[ant.now_node]):
                        if e != "None":
                            if (order not in ant.passed_nodes) and order not in nodes_of_warp_point:
                                #これまで通過していないノードを通過する。ワープポイントへの移動を制限する
                                nodes_selectable.append(order)
                else:
                    for order,e in enumerate(time_between_edges[ant.now_node]):
                        if e != "None":
                            if order not in ant.passed_nodes or order in nodes_of_warp_point:
                                #これまで通過していないノードを通過する。しかし、移動先がワープポイントである場合は何度でも通過しても良い
                                nodes_selectable.append(order)

                pheromone_affect_values = get_pheromone_affect(ant.now_node,pheromone_on_edges,nodes_selectable)
                heuristic_values = get_heuristic_value(ant.now_node,nodes_selectable,time_between_edges,nodes_of_warp_point,weight_warp_point=50)

                #それぞれの選択確率を求める
                tmp_pheromone_multiply_heuristic = [] #フェロモン効果とヒューリスティック値を掛け合わせた値
                sum_pheromone_multiply_heuristic = 0
                for num in range(len(nodes_selectable)):
                    tmp = (pheromone_affect_values[num]**alpha)*(heuristic_values[num]**beta)
                    tmp_pheromone_multiply_heuristic.append(tmp)
                    sum_pheromone_multiply_heuristic += tmp
                
                for p_h in tmp_pheromone_multiply_heuristic:
                    select_probability.append(p_h/sum_pheromone_multiply_heuristic)
                
                next_node = random.choices(nodes_selectable,weights=select_probability)[0] #次の移動先を決める

                #フェロモンを付着させる(一斉更新できないため廃止)
                #pheromone_on_edges[ant.now_node][next_node] += ant.pheromone_amount/time_between_edges[ant.now_node][next_node]

                #次の移動先へ移動する
                ant.passed_nodes.append(next_node) 
                ant.now_node = next_node

                """
                #終了条件を満たしているか調べる
                should_passed_node = set(range(25))  - set(nodes_of_warp_point) #通過するべきノード
                if set(ant.passed_nodes) >= should_passed_node:
                    finished_ants.append(ant)
                    ants.remove(ant) #removeの使い方が怪しい・・・これで外せるか・・・？無理そうならenumerateで場所指定で抜く
                """

        #フェロモンの付着を行う
        should_passed_node = set(range(25))  - set(nodes_of_warp_point) #通過するべきノード
        for order,ant in enumerate(ants):
            ant = ant[0]
            #フェロモンを付着させる.ワープポイントへの移動をしづらくする
            ant_from = ant.passed_nodes[-2]
            ant_to = ant.passed_nodes[-1]
            if ant_to in nodes_of_warp_point:
                #ワープポイントへの移動の際に、フェロモンがつきにくくする
                pheromone_on_edges[ant_from][ant_to] += ant.pheromone_amount/(time_between_edges[ant_from][ant_to] + 20)
            else:
                pheromone_on_edges[ant_from][ant_to] += ant.pheromone_amount/time_between_edges[ant_from][ant_to]

            #終了条件を満たしているアリを省く
            if set(ant.passed_nodes) >= should_passed_node:
                    finished_ants.append(ant)
                    ants.pop(order) 

    return (finished_ants,ants)

            
            
def ant_colony_opt(ant_num,cycle_num,alpha = 1,beta = 1,pheromone_evap_rate = 1,print_progress = False):
    """
    アントコロニー最適化を利用し、最適解を見つける

    アリをant_numの数、初期位置に生成し、フェロモンやヒューリスティック値に基づいて、探索をする。
    その際に、フェロモンの更新を行う。
    全てのありが、一定の回数ノード間の移動を行う、または、回る必要がある全てのノードを回り切った時、
    既存のアリを全て消去し、アリをant_numの数、初期位置に生成し、同様の操作を、cycle_num回行う。
    アリを置き換える際、各エッジのフェロモン量は引き継がれる。

    ant_num : アリの数
    cycle_num : 何世代まで、アリを作成するか。
    alpha : フェロモン効果の強度を決める
    beta : ヒューリスティック値の強度を決める
    pheromone_evap_rate : フェロモン蒸発率
    print_progress : 途中経過を出力するかどうか
    """
    pheromone_on_edges = [[0.01]*25 for _ in range(25)]#各エッジのフェロモン量.初期値を1にする
    nodes_of_warp_point = [1,2,5,8,12,15,19,20,23]#ワープポイントであるノードの番号
    time_between_edges = set_points_information.get_list()#各エッジ間を移動する際の時間

    for generation in range(cycle_num):
        ants = [[ant()] for _ in range(ant_num) ]
        ants_result = cycle_step(ants,time_between_edges,alpha,beta,pheromone_on_edges,nodes_of_warp_point,pheromone_evap_rate)
        if (generation == (cycle_num -1)) or print_progress:
            #結果を出力する
            if len(ants_result[0]) != 0: #回るべき全てのエッジを回ることができたありがいた場合
                print("★-★-★-★-★-★-★-★-★-★-★-★-★-★-★-★-★-★-★-★-★-★")
                print(f'第{generation}世代、・・・成功！！、代表の経路:{ants_result[0][0].passed_nodes}')
                #print("★-★-★-★-★-★-★-★-★-★-★-★-★-★-★-★-★-★-★-★-★-★")
            else: #誰も指定回数いないで、全てのエッジを回ることができなかった場合
                print(f'第{generation}世代、・・・失敗！！、代表の経路:{ants_result[1][0][0].passed_nodes}')

ant_colony_opt(ant_num=100,cycle_num=100,alpha=0.3,beta=2,pheromone_evap_rate=0.9,print_progress=True)


    


