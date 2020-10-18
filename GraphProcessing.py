import networkx as nx
import os
import time
import matplotlib.pyplot as plt


class GraphPorcessing:

    def __init__(self, data_addr, regenerate=True, verbose=False):
        """
        read data from data file
        :param data_addr: parent directory of *.edge files
        :param verbose:
        """
        self.data_addr = data_addr
        self.verbose = verbose
        self.graph = None
        self.line_graph = None

        if regenerate:
            print("start generating graph...")
            self.generate_graph()
            self.genereate_line_graph()
        else:
            cach_list = os.listdir("cache")
            if "graph.gpickle" in cach_list and "line_graph.gpickle" in cach_list:
                print("find graph.gpickle and line_graph.gpicle in cache. Skip regenerate.")
                self.graph = nx.read_gpickle(os.path.join("cache", "graph.gpickle"))
                self.line_graph = nx.read_gpickle(os.path.join("cache", "line_graph.gpickle"))
            else:
                print("doesn't find graph.gpickle and line_graph.gpicle in cache. process regenerate...")
                self.generate_graph()
                self.genereate_line_graph()


    def generate_graph(self):
        start_time = time.time()
        graph = nx.Graph()
        data_list = os.listdir(self.data_addr)
        for i, data_file in enumerate(data_list):
            if data_file.endswith(".edges"):
                ego_center = data_file.split('.')[0]
                edge_file = open(os.path.join(self.data_addr, data_file))
                edges_list = []
                neighbor_vertex_set = set()
                for line in edge_file.readlines():
                    # if len(line) < 4:
                    #     continue
                    vertex1, vertex2 = tuple(line.strip('\n').split(' '))
                    neighbor_vertex_set.add(vertex1)
                    neighbor_vertex_set.add(vertex2)
                    edges_list.append((vertex1, vertex2))

                for vertex in neighbor_vertex_set:
                    edges_list.append((ego_center, vertex))
                graph.add_edges_from(edges_list)
            print("\rgenerating graph {:.2f}%".format((1+i)*100/len(data_list)), end='')
        print()
        self.graph = graph
        nx.write_gpickle(self.graph, os.path.join("cache","graph.gpickle"))
        if self.verbose:
            print("write graph in cache, using time", time.time() - start_time)


    def genereate_line_graph(self):
        start_time = time.time()
        print("start generating line graph...")
        self.line_graph = nx.line_graph(self.graph)
        nx.write_gpickle(self.line_graph, os.path.join("cache", "line_graph.gpickle"))
        if self.verbose:
            print("write line_graph in cache, using time", time.time() - start_time)

    def get_graph(self):
        return self.graph

    def get_line_graph(self):
        return self.line_graph

    def describe_graph(self, figname="graph"):
        print("nodes:", self.graph.nodes())
        print("edges:", self.graph.edges())
        if self.verbose:
            print("number of edges:", self.graph.number_of_edges())
            print("number of nodes:", self.graph.number_of_nodes())
        nx.draw(self.graph)
        plt.savefig(figname)
        plt.show()

    def describe_line_graph(self, figname="line_graph"):
        if self.verbose:
            print(sorted(map(sorted, self.line_graph.edges())))
        nx.draw(self.line_graph)
        plt.savefig(figname)
        plt.show()



if __name__ == '__main__':
    # data_addr = "testData"
    data_addr = ".\\data\\twitter"
    gp = GraphPorcessing(data_addr,verbose=True, regenerate=True)
    gp.describe_graph()
    gp.describe_line_graph()

