#!/usr/bin/python3
# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # #
# Create Time: 2023/9/1317:42
# Fang YJ
# Real-Time Systems Group
# Hunan University HNU
# # # # # # # # # # # # # # # #

from MainHead import *


def LBL_Dag_Generator(_pdag, _oshape):
    if len(_oshape) == 0:
        yield _pdag

    elif len(_oshape) > 0:
        _pdag_nnum = _pdag.number_of_nodes()
        _pl_num = max([_nd[1]['l'] for _nd in _pdag.nodes(data=True)])
        _pl_nodes = set([_nd[0] for _nd in _pdag.nodes(data=True) if _nd[1]['l'] == _pl_num])
        _ll_nodes = [(_pdag_nnum + _i, {'l': _pl_num + 1}) for _i in range(_oshape[0])]
        pn_list = []
        for _pdag_anti_nodes in nx.antichains(_pdag):
            if not _pl_nodes.isdisjoint(_pdag_anti_nodes):
                pn_list.append(_pdag_anti_nodes)
        
        for rpns in combinations_with_replacement(pn_list, _oshape[0]):
            _rdag = copy.deepcopy(_pdag)
            _rdag.add_nodes_from(_ll_nodes)
            _rdag.add_edges_from([(_pn, _ln[0]) for _ps, _ln in zip(rpns, _ll_nodes) for _pn in _ps])
            for _ret in LBL_Dag_Generator(_rdag, _oshape[1:]):
                yield _ret

    else:
        assert False


# 测试代码
if __name__ == "__main__":
    ret = []
    for nnum in range(3, 101):
        st = time.time()
        rdag_num = 0
        for shape in shape_generation(nnum, (1,nnum),(1,nnum)):
            xdag = nx.DiGraph()
            xdag.add_nodes_from([(_nid,{'l': 1}) for _nid in range(shape[0])])
            for rdag in LBL_Dag_Generator(xdag, shape[1:]):  
                rdag_num += 1
        et = time.time()
        print(f"{nnum}_{rdag_num}_{et - st :.2f}")
        ret.append({'Node_Num': nnum, 'Dag_Num': rdag_num, 'Rtime':et - st})
    

