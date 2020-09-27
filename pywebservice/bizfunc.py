import numpy as np
np.set_printoptions(suppress=True)
import math

import scipy.stats as st

def as_num(x):
    y = '{:.17f}'.format(x)  # .1f 保留1位小数  想为十位就这样写10f
    return y

def dist(val1):
    return st.norm.cdf(val1)  # 标准正态分布在 0 处的累计分布概率值


def inv(val1):
    return st.norm.ppf(val1)  # 标准正态分布在 0.975 处的逆函数值


def npv(val1):
    return np.npv(0.281, [-100, 39, 59, 55, 20])  # 净现值

#𝑷𝑫_𝒇𝒐𝒓𝒘𝒂𝒓𝒅=𝑵((𝑵^(−𝟏) (𝑷𝑫)−𝒁_𝒇𝒐𝒓𝒘𝒂𝒓𝒅 √𝑹)/√(𝟏−𝑹))
def pd_forward(pd,r,z):
    result = as_num(dist((inv(pd)-(z*math.sqrt(r)))/math.sqrt(1-r)))
    # print(as_num(result))
    return result
