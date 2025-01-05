#!/usr/bin/python3
# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # #
# Real-Time Systems Group
# Hunan University HNU
# Fang YJ
# # # # # # # # # # # # # # # #

from MainHead import *


# # # # # # # #
#  Connection #
# # # # # # # #
def _rn(_dag, _l, _add_n, _id:int, _od:int, _tl:int=0):
    _pns = [_ni for _ni, _nd in _dag.nodes(data=True) if _nd['d'] == _l and _dag.out_degree(_ni) < _od]
    _ldisk = {_sni: (frozenset(_dag.predecessors(_sni)), frozenset(_dag.successors(_sni))) for _sni in _dag.nodes()}
    for _pnum in range(1, min(len(_pns), _id) + 1):
        __buffa = set()
        for _p_ns in combinations(_pns, _pnum):
            __lab_a = frozenset(Counter([_ldisk[_p_ni] for _p_ni in _p_ns]).items())
            if __lab_a not in __buffa:
                __buffa.add(__lab_a)
                __sub_dag = _dag.subgraph(set(_dag.nodes()) - set(_pns) - set.union(*(set(nx.ancestors(_dag, _p_ni)) for _p_ni in _p_ns)))

                __buffb = set()
                for _a_ns in nx.antichains(__sub_dag):
                    __lab_b = frozenset(Counter([_ldisk[_a_ni] for _a_ni in _a_ns]).items())
                    if __lab_b not in __buffb:
                        __buffb.add(__lab_b)

                        __ret = set(_a_ns) | set(_p_ns)
                        __temp_label = sum(1 << pos for pos in __ret)
                        if len(__ret) <= _id and __temp_label >= _tl and all([_dag.out_degree(__rni) < _od  for __rni in __ret]):

                            __tdag = nx.DiGraph(_dag)
                            __tni = __tdag.number_of_nodes()
                            __tdag.add_node(__tni, d = _l + 1)
                            __tdag.add_edges_from([(__rpni, __tni) for __rpni in __ret])
                            if _add_n > 1:
                                for __rdag in _rn(__tdag, _l, _add_n - 1, _id, _od, __temp_label):
                                    yield __rdag
                            elif _add_n == 1:
                                yield __tdag
                            else:
                                assert False


def Conn(_s:tuple, _id:int=float('Inf'), _od:int=float('Inf'), _jl:int=float('Inf'), _w:int=float('Inf')):
    __t_d = len(_s)
    if __t_d == 1:
        __tdag = nx.DiGraph()
        __tdag.add_nodes_from([(_ni, {'d': __t_d}) for _ni in range(_s[0])])
        yield __tdag
    elif __t_d > 1:
        for _SubD in Conn(_s[:-1]):
            for __tdag in _rn(_SubD, __t_d - 1, _s[-1], sum(_s[:-1]), sum(_s[1:])):
                yield __tdag
    else:
        assert False


if __name__ == "__main__":
    for __n in range(3, 10):
        st = time.time()
        __dnum = 0
        for __c in Comb(__n):
            for __s in Perm(__c):
                # print(__s)
                for __d in Conn(__s):
                    # print(f"\t{__d.edges()}")
                    __dnum += 1
        et = time.time()
        print(f"{__n}_{__dnum}_{et-st:.6f}")

