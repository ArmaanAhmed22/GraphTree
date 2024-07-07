import re
import networkx as nx
import matplotlib.pyplot as plt
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

class GraphV:
    def __init__(self,edge_list,default_size=0,all_sizes=None,empty_node_size=10,color="black"):
        self.G=nx.DiGraph()
        self.edge_list_symb=edge_list
        self.ID_list={}
        self.ID_list_rev={}
        self.pos={}
        cur_id=0
        for edge in edge_list:
            if edge[0] in self.ID_list and edge[1] in self.ID_list:
                continue
            else:
                if edge[0] not in self.ID_list:
                    self.ID_list[edge[0]]=cur_id
                    self.ID_list_rev[cur_id]=edge[0]
                    cur_id+=1
                if edge[1] not in self.ID_list:
                    self.ID_list[edge[1]]=cur_id
                    self.ID_list_rev[cur_id]=edge[1]
                    cur_id+=1
        self.node_sizes={}
        
        self.sizes = {}
        for sym_id,num_id in self.ID_list.items():
            if all_sizes is not None and sym_id in all_sizes:
                self.sizes[num_id]=all_sizes[sym_id]
            else:
                self.sizes[num_id]=default_size
        self.empty_node_size=empty_node_size
        self.color=color
        
                
    
    def increase_breadth_below(self,node):
        i=0
        while i<len(self.edge_list_symb):
            cur_edge=self.edge_list_symb[i]
            #ADD EDGE (node,"TEMP") before
            if cur_edge[0]==node:
                self.edge_list_symb.insert(i,(node,"TEMP"))
                i+=1
            i+=1
        self.edge_list_symb.append((node,"TEMP"))
        print(self.edge_list_symb)
        
    def generate_position(self):
        edge_list=[]
        
        temp_id=len(self.edge_list_symb)
        for cur_edge in self.edge_list_symb:
            if cur_edge[1]=="TEMP":
                second_pos=temp_id
                temp_id-=1
            else:
                second_pos=self.ID_list[cur_edge[1]]
            first_pos=self.ID_list[cur_edge[0]]
            edge_list.append((first_pos,second_pos))
        self.G.add_edges_from(edge_list)
        self.pos=graphviz_layout(self.G, prog='dot')
        for cur_temp_id in range(temp_id+1,len(self.edge_list_symb)+1):
            #Delete
            pass#del self.pos[cur_temp_id]
            #self.G.remove_node(cur_temp_id)
        print(self.pos)
        
    def move_node_preserve_relative(self,node,move_x,move_y):
        x,y=self.pos[self.ID_list[node]]
        self.pos[self.ID_list[node]]=(x+move_x,y+move_y)
        #Update others
        for cur_edge in self.edge_list_symb:
            if cur_edge[0]==node:
                self.move_node_preserve_relative(cur_edge[1],move_x,move_y)
                
    def decrease_edge_percent(self,node,percent):
        for cur_edge in self.edge_list_symb:
            if cur_edge[1]==node:
                first_node=cur_edge[0]
                first_x,first_y=self.pos[self.ID_list[first_node]]
                second_x,second_y=self.pos[self.ID_list[node]]
                break
        move_x=-percent*(second_x-first_x)
        move_y=-percent*(second_y-first_y)
        self.move_node_preserve_relative(node,move_x,move_y)
        
    def decrease_edge_percent_regex(self,node_pattern,percent):
        for k in self.ID_list.keys():
            if re.match(node_pattern,k):
                #print(k)
                self.decrease_edge_percent(k,percent)
            
    def draw(self,ax=None):
        node_size_list=[]
        ordered_nodes=list(self.G)
        colors=[]
        for node in ordered_nodes:
            cur_size=self.sizes[node]
            if cur_size==0:
                node_size_list.append(self.empty_node_size)
                colors.append("white")
            else:
                node_size_list.append(self.sizes[node])
                colors.append(self.color)
        edge_colors=[self.color for _ in ordered_nodes]
        if ax is None:
            fig,ax=plt.subplots()
        nx.draw_networkx(self.G,self.pos,with_labels=False,arrows=False,node_size=node_size_list,node_color=colors,edgecolors=edge_colors,ax=ax)
        return ax
        
    def show(self,ax=None):
        self.draw(ax)
        plt.show()
    
    def save(self,filename,ax=None):
        self.draw(ax)
        plt.savefig(filename,dpi=300)
            