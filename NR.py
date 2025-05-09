#!/usr/bin/python3
# -*- coding: utf-8 -*-

from MainHead import *

def Node_Enu(subdag, nnum):
    new_id = subdag.number_of_nodes()
    for op_nx in nx.antichains(subdag):
        new_sub_dag = copy.deepcopy(subdag)
        new_sub_dag.add_node(new_id)            # (1) 加结点
        for prex in op_nx:
            new_sub_dag.add_edge(prex, new_id)  # (2) 加边
        if nnum == 1:
            yield new_sub_dag
        else:
            for _ret_dag in Node_Enu(new_sub_dag, nnum - 1):
                yield _ret_dag


if __name__ == "__main__":
    for nnum in range(1, 5):
        print(f"node_num:{nnum + 1}:", end='\t')
        gx = nx.DiGraph()
        gx.add_nodes_from([0])
        dag_num = 0
        for tx in Node_Enu(gx, nnum):
            # print(tx.nodes())
            # print(tx.edges())
            dag_num += 1
        print(f"{nnum + 1}:{dag_num}")
