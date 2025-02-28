import igraph
from proof_constructor.graph import Graph

class PlotTrees(object):
    def __init__(self,graph,output_dir):
        self.graph = graph if isinstance(graph,Graph) else None
        self.output_dir = output_dir
        # self.trees = trees

    def plot_trees(self):
        for i in range(self.graph.size()):
            vis_tree = self.plot_tree(i)
            self.show_tree(vis_tree,i)
        return

    def plot_tree(self,vertex_idx):
        proof_tree = self.graph.idx_to_vertex(vertex_idx).proof_tree
        if proof_tree ==None:
            raise ValueError("proof_tree {} is None".format(vertex_idx))
        vis_tree = igraph.Graph()
        vis_tree.add_vertices(len(proof_tree))
        node_list = list(proof_tree.preorder())
        node_list=sorted(node_list, key = lambda u: u.idx)

        clause_list = []
        true_list = []
        for i in range(len(node_list)):
            to_append = str(proof_tree.get_element(node_list[i]))
            clause_list.append(to_append)
            true_list.append(node_list[i].is_true)
        vis_tree.vs['clause'] = clause_list
        vis_tree.vs['is_true'] = true_list

        edge_list = []
        for i in range(len(node_list)):
            children_list = proof_tree.children(node_list[i])
            for j in range(len(children_list)):
                to_append = (i,children_list[j].idx)
                edge_list.append(to_append)
        vis_tree.add_edges(edge_list)
        return vis_tree

    def show_tree(self,vis_tree,vertex_idx):
        if vis_tree==None:
            raise ValueError("vis_tree {} is None".format(vertex_idx))
        layout = vis_tree.layout("tree")
        color_dict = color_dict = {True: "LightSkyBlue", False: "red"}
        visual_style = {}
        visual_style["vertex_order"] =range(len(vis_tree.vs))
        visual_style["vertex_size"] = 50
        visual_style["vertex_color"] = [color_dict[i] for i in vis_tree.vs["is_true"]]
        visual_style["vertex_color"][0] = "LightGreen" if vis_tree.vs["is_true"][0] else "yellow"
        visual_style["vertex_label"] = vis_tree.vs["clause"]
        visual_style["layout"] = layout
        visual_style["bbox"] = (600, 600)
        visual_style["margin"] = 100
        output_filename = "{}tree{}.png".format(self.output_dir,vertex_idx)
        igraph.plot(vis_tree, output_filename,**visual_style)

        




        # self.plotted.vs['goal'] = vertex_goal_list
