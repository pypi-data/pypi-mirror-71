import numpy as np
import distance as Dist


def is_similarity(vec1, vec2, dist_choise=2, tolerance=0.3):
    '''
    input
    -----
        dist_choise: 选择哪种距离, 1:P1范数(曼哈顿距离), 2: P2范数(欧氏距离), 3: P_inf范数(切比雪夫距离)
        tolerance: 相似度小于该值时会被判断为同类别
    return
    ------
        bool
    '''
    if dist_choise == 1:
        distance = Dist.manhattan_dist
    elif dist_choise == 2:
        distance = Dist.euclidean_dist
    elif dist_choise == 3:
        distance = Dist.chebyshev_dist
    else:
        raise ValueError('dist_choise is a bad number')

    # 判断相似度:
    if distance(vec1, vec2) < tolerance:
        return True
    else:
        return False


def find_simil_idx(Vec_list, VEC, dist_choise=2, tolerance=0.3):

    IDX = []
    for idx, vec in enumerate(Vec_list):
        if is_similarity(vec, VEC, dist_choise, tolerance):
            IDX.append(idx)
    return IDX


def simil_score(V1, w1, V2, w2, dist_choise=2, lamb=5, sigma=1):
    '''
    V1,w1对应Key color
    V2,w2对应待分类color
    可调节参数:
    lamb: 取值建议1~10,值越大表示颜色百分比所占权重越大
    sigma: 取值建议0~1.7, 值越小表示相似距离变大(小)时，相似度权重下降(上升)越快, 它的取值与 dist_choise相关:P1(0~3),P2(0~1.7),P3(0~1)
    output: 0~1之间的相似分数
    '''
    if dist_choise == 1:
        distance = Dist.manhattan_dist
    elif dist_choise == 2:
        distance = Dist.euclidean_dist
    elif dist_choise == 3:
        distance = Dist.chebyshev_dist
    else:
        raise 'dist_choise is a bad number'
    dis = 0
    Dis = 0
    for i1, v1 in enumerate(V1):
        for i2, v2 in enumerate(V2):
            dis_weight = 2.2 * gaussian(distance(v1, v2), sigma=sigma, miu=0)
            # if i1 == 0 and i2 == 0:
            #      print(f'第一个色块的相似度为{dis_weight}')

            W1, W2 = np.exp(lamb * w1[i1]), np.exp(lamb * w2[i2])
            dis += (W1 * W2) * dis_weight

            Dis_weight = 2.2 * gaussian(distance(v1, v1), sigma=sigma,
                                        miu=0)  # v1是key_color
            Dis += (W1 * W2) * Dis_weight
    #     m = (i1+1)*(i2+1)
    #     print(dis, Dis)
    return dis / Dis


def is_Centers_same(V1,
                    w1,
                    V2,
                    w2,
                    yourScore=0.75,
                    dist_choise=2,
                    lamb=5,
                    sigma=1,
                    **dic):
    '''
    V1,w1对应Key color, V通常是一个多Center的列表
    V2,w2对应待分类color
    可调节参数:
    lamb: 取值建议1~10,值越大表示颜色百分比所占权重越大
    sigma: 取值建议0~1.7, 值越小表示相似距离变大(小)时，相似度权重下降(上升)越快, 它的取值与 dist_choise相关:P1(0~3),P2(0~1.7),P3(0~1)
    output: 达到分数返回True 否则返回False
    '''
    # default Para
    printScore = 0

    if 'printScore' in dic:
        printSore = dic['printScore']

    score = simil_score(V1,
                        w1,
                        V2,
                        w2,
                        dist_choise=dist_choise,
                        lamb=lamb,
                        sigma=sigma)
    if printSore == 1:
        print(score)

    if score >= yourScore:
        return True
    else:
        return False


def find_centers_simil_idx(Centers1,
                           Centers2,
                           yourScore=0.75,
                           dist_choise=2,
                           lamb=5,
                           sigma=1,
                           **dic):
    '''
    Centers1将与每一个Centers2向量比较, 最后返回所有与Centers2相似向量下标列表
    '''
    # default Para
    printScore = 0

    if 'printScore' in dic:
        printScore = dic['printScore']

    V1, w1 = Centers1[0], Centers1[1]
    IDX = []
    for idx, centers in enumerate(Centers2):
        V2, w2 = centers[0], centers[1]
        if is_Centers_same(V1,
                           w1,
                           V2,
                           w2,
                           yourScore=yourScore,
                           dist_choise=dist_choise,
                           lamb=lamb,
                           sigma=sigma,
                           printScore=printScore):
            IDX.append(idx)
    return IDX
