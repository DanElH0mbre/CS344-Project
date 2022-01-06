import sys, importlib, animator

class GraphInput:
    def __init__(self):
        #A dictionary to map the algorithm name to the directory and filename
        algorithms = {"fractional1": ["../fractional_matching_1", "fractionalalgo1"], "fractional2": ["../fractional_matching_2", "fractionalalgo2"], "integral1": ["../integral_matching_1", "integralalgo1"], "integral2": ["../integral_matching_2", "integralalgo2"]}


        path = algorithms[sys.argv[1]][0]
        fname = algorithms[sys.argv[1]][1]
        sys.path.append(path)
        alg = importlib.import_module(fname)

        # Corrects the formatting of the text file so that it is ready for use.
        # Retrieves the values of n and epsilon, which were specified when the graph was generated.
        file = open(sys.argv[2], "r")
        str_file = []
        for line in file:
            line = line.strip("\n")
            line = line.split(" ")
            str_file.append(line)

        epsilon = float(str_file[0][0])
        n = int(str_file[0][1])
        bip_cut = 0
        is_integral = "integral" in fname
        if is_integral:
            bip_cut = int(str_file[0][2])
        self.vis = animator.Animator(n)
        Graph = alg.Algorithm(epsilon, n) if not is_integral else alg.Algorithm(epsilon, n, bip_cut)
        
        # We apply each update to both the algorithm and the animator
        for update in str_file[1:]:
            operation = update[0]
            u = int(update[1])
            v = int(update[2])
            if operation == "ins":
                Graph.insert(u, v)
                self.vis.insert(u, v)
            elif operation == "del":
                Graph.delete(u, v)
                self.vis.delete(v, u)
        Graph.toString()

        #This should be edited once future algorithms are added, since not all of them compute a vertex cover.
        #vc = Graph.vertex_cover()
        #self.vis.highlight_vc(vc)
        if is_integral:
            matching = Graph.matching
            self.vis.highlight_matching(matching)
        else:
            vc = Graph.vertex_cover()
            self.vis.highlight_vc(vc)
        
        

g = GraphInput()
g.vis.window.mainloop() #Keeps the window running after animation is complete