from __future__ import print_function
from game import sd_peers, sd_spots, sd_domain_num, init_domains, \
    restrict_domain, SD_DIM, SD_SIZE
import random, copy

class AI:
    def __init__(self):
        pass

    def solve(self, problem):

        # this contains all of the domains of each spot 
        # EX: (0,0) : [1,2,3,4,5,6,7,8,9] (0,1) : [9]
        domains = init_domains()
        restrict_domain(domains, problem) 
        # TODO: implement backtracking search. 
        # constraints:
        # sd_peers -> the peers around the square block
        # print("what is this", sd_peers)
        # x -> grab all of the rows
        # y -> grab all of the cols
        #
        # sd_domain_num -> the domain of each box
        # print("what is this", sd_domain_num)
        #
        # conflict in assignment ---- (-1,-1) = -1
        
        # assigment[spot] = #
        assignments = {}
        # tutple stack (assignment, decision spot, domain)
        stack = []
        while True:
            # propagate using arc-consistency *****needs to be checked
            # (assignments,domains)
            self.propagate(assignments, domains)
            # check if there is a conflict or not
            if (-1,-1) not in assignments:
                # check if all spot on the board is assigned
                # should have 81 assigned variables
                if len(assignments) == len(sd_spots):  
                    return domains
                else:
                    # assign value to an unassigned spot ***** needs to be checked
                    # (assignments, element)
                    decision = self.makeDecision(assignments, domains)
                    # push a backtrack point
                    assignments = decision[0]
                    element = decision[1]
                    stack.append((copy.deepcopy(assignments), element, copy.deepcopy(domains)))
            else:
                # remove the conflict from assignment
                # assignments.pop((-1,-1))
                if len(stack) == 0:
                    return None
                else:
                    #reset assignement state and domain state
                    assignments,domains = self.backtrack(stack)
        
        # TODO: delete this block ->
        # Note that the display and test functions in the main file take domains as inputs. 
        #   So when returning the final solution, make sure to take your assignment function 
        #   and turn the value into a single element list and return them as a domain map. 
        # for spot in sd_spots:
        #    domains[spot] = [1]
        # return domains
        # <- TODO: delete this block

    # TODO: add any supporting function you need
    def propagate(self, assignments, domain):
        # TODO
        while True:
            count = 0
            # assign spot of domain becomes a singleton
            for key in sd_spots:
                if len(domain[key]) == 1 and (key not in assignments):
                    assignments[key] = domain[key][0]
            # spot is assigned to a value, update domain to a singleton
            for key in assignments:
                if len(domain[key]) > 1:
                    domain[key] = [assignments[key]]
            # checks if there are any conflicts
            for key in sd_spots:
                #print(key, domain[key])
                if len(domain[key]) == 0:
                    assignments[(-1,-1)] = -1
                    return (assignments, domain)
            # remove any everything from 
            for key in assignments:
                for coord in sd_peers[key]:
                    if assignments[key] in domain[coord]:
                        count+=1
                        domain[coord].remove(assignments[key])
            if count == 0:
                return (assignments, domain)

    def makeDecision(self, assignments, domain):
        # TODO
        # grab all of the availible spots for choosing
        available = [item for item in domain if len(domain[item]) > 1]
        if len(available) > 0:
            a = available[0]
            assignments[a] = domain[a][0]
        return (assignments, a)

    def backtrack(self,stack):
        # TODO
        assignment,spot,domain = stack.pop()
        # remove element from assignment
        del_value = assignment.pop(spot)
        if del_value in domain[spot]:
            domain[spot].remove(del_value)
        return (assignment,domain)

    #### The following templates are only useful for the EC part #####

    # EC: parses "problem" into a SAT problem
    # of input form to the program 'picoSAT';
    # returns a string usable as input to picoSAT
    # (do not write to file)
    def sat_encode(self, problem):
        text = ""

        # TODO: write CNF specifications to 'text'

        return text

    # EC: takes as input the dictionary mapping 
    # from variables to T/F assignments solved for by picoSAT;
    # returns a domain dictionary of the same form 
    # as returned by solve()
    def sat_decode(self, assignments):
        # TODO: decode 'assignments' into domains
        
        # TODO: delete this ->
        domains = {}
        for spot in sd_spots:
            domains[spot] = [1]
        return domains
        # <- TODO: delete this
