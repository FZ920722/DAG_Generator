#!/usr/bin/python3
# -*- coding: utf-8 -*-

# # # # # # # # # # # # # # # #
# Real-Time Systems Group
# Hunan University HNU
# Fang YJ
# # # # # # # # # # # # # # # #

from MainHead import *


# # # # # # # # # # # # # # # #
# connection
# # # # # # # # # # # # # # # #
def gen_mine_new(shape_num_list):
    # for shape_num_list in all_shape_list:
    shape_list = shape_list_trance(shape_num_list)
    dag_list = [nx.DiGraph()]
    for level_id, self_node_list in enumerate(shape_list):
        if (level_id + 1) == len(shape_list):
            for dag_x in dag_list:
                p_nodes = [nodex for nodex in dag_x.nodes() if len(list(dag_x.successors(nodex))) == 0]
                dag_x.add_nodes_from([(self_node_list[0], {'level_num': level_id})])
                for p_node_x in p_nodes:
                    dag_x.add_edge(p_node_x, self_node_list[0])
        else:
            temp_dag_list = []
            for dag_x in dag_list:
                for __rdx in shape_dag_generator(dag_x, self_node_list, level_id):
                    temp_dag_list.append(__rdx)
            dag_list = temp_dag_list
    for ret_dagx in dag_list:
        yield ret_dagx

def shape_list_trance(shape_num_list):
    node_num = sum(shape_num_list)
    node_id_list = list(range(node_num))
    ret_shape_list = []
    for shape_num_x in shape_num_list:
        ret_shape_list.append(node_id_list[:shape_num_x])
        del node_id_list[:shape_num_x]
    return ret_shape_list

def shape_dag_generator(dag_x, self_node_list, level_num):
    for level_id in range(level_num):
        if level_id == level_num - 1:
            up_same_level_node_iso_label_comput(dag_x, level_id)
        down_same_level_node_iso_label_comput(dag_x, level_id)

    total_label_dict = {}
    for node_x in dag_x.nodes(data=True):
        node_x_label = (node_x[1]['level_num'], node_x[1]['up_iso_label'],node_x[1]['down_iso_label'])
        if node_x_label in total_label_dict:
            total_label_dict[node_x_label].append(node_x[0])
        else:
            total_label_dict[node_x_label] = [node_x[0]]

    last_level_node_list = [node_x[0] for node_x in dag_x.nodes(data=True) if node_x[1]['level_num'] == level_num - 1]

    last_level_node_id_enumerate_list = []
    for sn_num in range(len(last_level_node_list)):
        temp_id_enumerate_list_1 = list(itertools.combinations(last_level_node_list, sn_num + 1))
        temp_label_enumerate_list = list(set([tuple([(dag_x.nodes[temp_id_x]['level_num'], dag_x.nodes[temp_id_x]['up_iso_label'],dag_x.nodes[temp_id_x]['down_iso_label']) for temp_id_x in temp_id_list])
                                            for temp_id_list in temp_id_enumerate_list_1]))
        temp_id_enumerate_list_2 = []
        for temp_label_list in temp_label_enumerate_list:
            temp_total_label_dict = copy.deepcopy(total_label_dict)
            temp_id_enumerate_list_2.append([temp_total_label_dict[temp_label_x].pop(0) for temp_label_x in temp_label_list])
        last_level_node_id_enumerate_list += temp_id_enumerate_list_2

    pnode_list_enumerate = []
    for last_level_node_enumerate_x in last_level_node_id_enumerate_list:
        sample_dag = copy.deepcopy(dag_x)
        rem_set = set(last_level_node_list)
        for last_level_node_x in last_level_node_enumerate_x:
            rem_set.update(nx.ancestors(sample_dag, last_level_node_x))
        sample_dag.remove_nodes_from(rem_set)
        pred_node_opt_list = list(nx.antichains(sample_dag, topo_order=None))
        for pred_node_opt_x in pred_node_opt_list:
            pred_node_opt_x += last_level_node_enumerate_x
        pnode_list_enumerate += pred_node_opt_list
    temp_dag_x = copy.deepcopy(dag_x)
    temp_dag_x.add_nodes_from([(self_node_x, {'level_num':level_num}) for self_node_x in self_node_list])
    if len(pnode_list_enumerate) == 0:
        yield temp_dag_x
    else:
        edge_p_list = list(itertools.combinations_with_replacement(pnode_list_enumerate, len(self_node_list))) # 从可行解法中抽取 len(sn)个
        for edge_p_list_x in edge_p_list:
            temp_dag_list_x = copy.deepcopy(temp_dag_x)
            for self_node_id, edges_p_x in enumerate(edge_p_list_x):
                for edge_p_x in edges_p_x:
                    temp_dag_list_x.add_edge(edge_p_x, self_node_list[self_node_id])
            yield temp_dag_list_x


def up_same_level_node_iso_label_comput(dag_x, level_id):
    self_level_node_list = [node_x[0] for node_x in dag_x.nodes(data=True) if node_x[1]['level_num'] == level_id]
    up_iso_node_list = [[self_level_node_list.pop()]]
    for node_x in self_level_node_list:
        t_step = True
        sn_subg = dag_x.subgraph(list(nx.ancestors(dag_x, node_x)) + [node_x])
        for node_id_list in up_iso_node_list:
            tsn_subg = dag_x.subgraph(list(nx.ancestors(dag_x, node_id_list[0])) + [node_id_list[0]] )
            if nx.isomorphism.GraphMatcher(sn_subg, tsn_subg).is_isomorphic():
                node_id_list.append(node_x)
                t_step = False
                break
        if t_step:
            up_iso_node_list.append([node_x])
    for up_iso_label, node_list in enumerate(up_iso_node_list):
        for node_x in node_list:
            dag_x.nodes[node_x]['up_iso_label'] = up_iso_label


def down_same_level_node_iso_label_comput(dag_x, level_id):
    self_level_node_list = [node_x[0] for node_x in dag_x.nodes(data=True) if node_x[1]['level_num'] == level_id]
    down_iso_node_list = [[self_level_node_list.pop(0)]]
    for node_x in self_level_node_list:
        t_step = True
        sn_subg = dag_x.subgraph(list(dag_x.successors(node_x)) + [node_x])

        for node_id_list in down_iso_node_list:
            tsn_subg = dag_x.subgraph(list(dag_x.successors(node_id_list[0])) + [node_id_list[0]] )
            if nx.isomorphism.GraphMatcher(sn_subg, tsn_subg).is_isomorphic():
                node_id_list.append(node_x)
                t_step = False
                break
        if t_step:
            down_iso_node_list.append([node_x])
    for down_iso_label, node_list in enumerate(down_iso_node_list):
        for node_x in node_list:
            dag_x.nodes[node_x]['down_iso_label'] = down_iso_label


if __name__ == "__main__":
    for nnum in range(3, 10):
        dag_num = 0
        st = time.time()
        for _c in Comb(nnum - 2):
            for _s in Perm(_c):
                for dagx in gen_mine_new((1,) + _s + (1,)):
                    dag_num += 1
        et = time.time()
        print(f"{nnum}_{dag_num}_{et - st :.2f}")


# ######################################################################## #
# node_num:3_ time1:0.0_ time2:0.0_list1-length = 1; list2-length = 1; list3-length = 1
# ######################################################################## #
# node_num:4_ time1:0.0_ time2:0.0_list1-length = 2; list2-length = 2; list3-length = 2
# ######################################################################## #
# node_num:5_ time1:0.0_ time2:0.002043008804321289_list1-length = 3; list2-length = 4; list3-length = 5
# ######################################################################## #
# node_num:6_ time1:0.0_ time2:0.0065233707427978516_list1-length = 5; list2-length = 8; list3-length = 15
# ######################################################################## #
# node_num:7_ time1:0.0_ time2:0.019937515258789062_list1-length = 7; list2-length = 16; list3-length = 55
# ######################################################################## #
# node_num:8_ time1:0.0_ time2:0.08110785484313965_list1-length = 11; list2-length = 32; list3-length = 252
# ######################################################################## #
# node_num:9_ time1:0.0_ time2:0.44913721084594727_list1-length = 15; list2-length = 64; list3-length = 1464
# ######################################################################## #
# node_num:10_ time1:0.0020112991333007812_ time2:2.9970197677612305_list1-length = 22; list2-length = 128; list3-length = 10859
# ######################################################################## #
# node_num:11_ time1:0.018213748931884766_ time2:26.864338874816895_list1-length = 30; list2-length = 256; list3-length = 103141
# ######################################################################## #
# node_num:12_ time1:0.1936030387878418_ time2:505.52682876586914_list1-length = 42; list2-length = 512; list3-length = 1256764
# ######################################################################## #
