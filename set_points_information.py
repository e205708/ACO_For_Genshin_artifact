
import pprint

def get_list():
    """
    Return: 各ポイント間の移動時間をまとめたlist
    """
    time_matrix = [["None"]*25 for _ in range(25)]

    colums = []

    #どの地点からでもワープポイントを利用できるため、全ての移動パターンにワープポイントへの移動時間を持たせる
    warp_points = {2:9,3:9,6:9,9:9,13:9,16:9,20:9,21:9,24:9}

    #要素（ワープポイントor聖遺物)の番号:そこまでの移動時間
    colum_1 = {}
    colum_2 = {1:45}
    colum_3 = {4:22,7:34}
    colum_4 = {5:9,7:35}
    colum_5 = {4:9,7:27}
    colum_6 = {4:26,5:22}
    colum_7 = {4:24,5:27,8:28}
    colum_8 = {7:38}
    colum_9 = {7:30,8:14}
    colum_10 = {6:14,11:23}
    colum_11 = {10:23,12:17,14:25,15:23}
    colum_12 = {11:17,14:10,15:20}
    colum_13 = {10:21,11:28,12:23}
    colum_14 = {11:27,12:13,15:23}
    colum_15 = {11:30,12:20,14:23,17:16}
    colum_16 = {14:20,15:26,17:25,18:29,19:28}
    colum_17 = {15:16}
    colum_18 = {19:10}
    colum_19 = {18:10}
    colum_20 = {17:25}
    colum_21 = {17:25,22:8}
    colum_22 = {23:15}
    colum_23 = {22:26}
    colum_24 = {25:21}
    colum_25 = {}

    colums.append(colum_1)
    colums.append(colum_2)
    colums.append(colum_3)
    colums.append(colum_4)
    colums.append(colum_5)
    colums.append(colum_6)
    colums.append(colum_7)
    colums.append(colum_8)
    colums.append(colum_9)
    colums.append(colum_10)
    colums.append(colum_11)
    colums.append(colum_12)
    colums.append(colum_13)
    colums.append(colum_14)
    colums.append(colum_15)
    colums.append(colum_16)
    colums.append(colum_17)
    colums.append(colum_18)
    colums.append(colum_19)
    colums.append(colum_20)
    colums.append(colum_21)
    colums.append(colum_22)
    colums.append(colum_23)
    colums.append(colum_24)
    colums.append(colum_25)


    for order,col in enumerate(colums):
        
        for object_num in col:
            time_matrix[order][object_num-1] = col.get(object_num)
        
        #ワープポイントへの移動時間
        for warp_points_num in warp_points:
            time_matrix[order][warp_points_num-1] = warp_points.get(warp_points_num)
        
        #自分自身へは移動できない様にする
        time_matrix[order][order] = "None"

    pprint.pprint(time_matrix,width=300)

    return time_matrix

