#!/usr/bin/env python3
import copy

from condition import Condition
from link import Link
from plan import Plan
from step import Step
import student_tests
from ordered_set import Set

class Planner(object):
    # 
    # 	 * Note that there can be many correct sequences- your algorithm need only
    # 	 * provide one of them. Make sure to pay attention to each piece of data included in a 'plan'
    #
    
    """
    =============================================================================
    Helper functions (start)
    """
    def getDirectPrecursors(self, step, plan):
        """
        given a step and a plan, return a set of steps who are the director precursors (parent if in a graph) of the target step.
        a director precursor is the step that has to immediately occur before the target step
	"""
        precursors = Set()
        
        # Any step that has a link form this step, must follow it
        for link in plan.getCausalLinks():
            if link.getSecondId() == step.getId():
                step_to_add = plan.getStep(link.getFirstId())
                if step_to_add:
                    precursors.add(step_to_add)
        
        # Add all the steps that proceeds us in a precondition condition.
        for order in plan.getOrderingConstraints():
            is_post_name = False
            for constraint_id in order[1:]:
                if constraint_id == step.getId():
                    is_post_name = True
            # if we got here this must precede us
            if is_post_name:
                step_to_add = plan.getStep(order[0])
                if step_to_add:
                    precursors.add(step_to_add)
        
        return precursors
    
    def getAllPrecursors(self, step, plan):
        """
        given a step and a plan, return a set of steps who are the precursors (antecedent if in a graph) of the target step.
        a precursor is any step that has to occur before the target step, regardless whether it is immediate or not.
	"""        
        # The set of precursors we already added
        precursors = Set()
        
        # The list of steps we have already processed and that we need to add the precursors of
        # Initially we only add the precursors of the first step, not the first step itself. Thus, if the first step ends up being added, then there is a loop
        to_add_precursers = [step, ]
        
        while len(to_add_precursers) != 0:
            current_step = to_add_precursers.pop(0)
            direct_precursors = self.getDirectPrecursors(current_step, plan)
            
            # Remove all steps we already processed (to prevent infinite loops)
            direct_precursors = direct_precursors - precursors
            
            for precursor in direct_precursors:
                precursors.add(precursor)
                to_add_precursers.append(precursor)
        
        return precursors
    
    def get_parameters(self, file_name):
        """
        given the file_name(either test1 or test1.py) in student_tests, return the steps, ordering_constraints, causal_links defined in that test case
	"""
        attribute_name = file_name.split(".")[0]
        module = __import__("student_tests." + attribute_name).__dict__[attribute_name]
        steps = module.steps
        ordering_constraints = module.ordering_constraints
        causal_links = module.causal_links
        
        return copy.deepcopy(steps), copy.deepcopy(ordering_constraints), copy.deepcopy(causal_links)
    
    def run_test(self, steps, ordering_constraints, causal_links, test_name=""):
        """
        given the steps, ordering_constraints, causal_links, return whether it is complete, consistent, a solution and list the linearization
        the test_name is optional which is the name of the currently test running, so that it is convenient which test results is which when run in bulk
	"""
        p = Plan(steps, ordering_constraints, causal_links)
        
        complete = self.isComplete(p)
        consistent = self.isConsistent(p)
        solution = self.isSolution(p)
        linearizations = []
        if solution:
            linearizations = self.createLinearization(p)
        
        print("=======================================================")
        print("This plan is: ", test_name)
        print("Complete: ", complete)
        print("Consistent: ", consistent)
        print("Solution: ", solution)
        if solution:
            print("Linearization: ")
            for linearization in linearizations:
                print("\t", linearization)
        
        return complete, consistent, solution, linearizations

    """
    =============================================================================
    Helper functions (end)
    """    
    
    def createLinearization(self, plan):
        """
        create the linearization of a plan. It is a list of strings.
        For more information on completeness, please refer to the handout.
	"""
        output = []
        steps_to_process = Set(plan.getSteps())
        
        last_steps_num = -1
        
        while steps_to_process and len(steps_to_process) != last_steps_num:
            # if we get to a loop, then we will not be able to add any more places, and this is not a complete plan
            last_steps_num = len(steps_to_process)
            this_level = Set()
            
            for step in steps_to_process:
                to_add = True
                for precursor in self.getDirectPrecursors(step, plan):
                    # if we need a prerequisite we did not add yet
                    if precursor in steps_to_process:
                        # do not add this
                        # TODO START
                        to_add = False
                        # TODO END
                
                if to_add:
                    # add this one to this_level and output
                    #TODO START
                    this_level.add(step)
                    output.append(step.getOperator())
                    #TODO END

            # delete the step that has been processed in steps_to_process
            # TODO START
            steps_to_process = steps_to_process - this_level
            # TODO END
                
        if not steps_to_process:
            return output

        return None

    def isComplete(self, plan):
        """
        given a plan, return whether the plan is complete (boolean). For more information on completeness, please refer to the handout.
	"""
        for step in plan.getSteps():
            for precondition in step.getPrecondition():
                satisfied = False   # no open precondition
                for link in plan.getCausalLinks():
                    # check if there is a causal link that links from other steps to this step, and other steps can result in this condition
                    # TODO START
                    effect = link.getEffect()   # override __eq__( ... ) in condition.py or compare attribute by attribute
                    if link.getSecondId() == step.getId() and effect.getState() == precondition.getState() and effect.getPredicate() == precondition.getPredicate():
                        satisfied = True
                    # TODO END
                if not satisfied:
                    return False

        return True

    def isConsistent(self, plan):
        """
        given a plan, return whether the plan is consistent (boolean). For more information on consistency, please refer to the handout.
	"""        
        # Get a dictionary of precursors for all the steps, with the id to be the key, and the list of all precursors as the value
        precursor_dict = {}
        
        for step in plan.getSteps():
            precursors = self.getAllPrecursors(step, plan)
            precursor_dict[step.getId()] = precursors
            # check if there are cycles in the ordering constraints
            #  TODO START
            for precursor in precursors:
                if precursor.getId() in precursor_dict and step in precursor_dict[precursor.getId()]:
                    return False
            #  TODO END
        
        # check if there are conflicts with the causal links
        for link in plan.getCausalLinks():
            first_step_precursor = precursor_dict[link.getFirstId()]
            end_step = plan.getStep(link.getSecondId())
            
            # see if there is a step that can appear between these two steps that conflicts with it
            for step in plan.getSteps():
                if step.getId() != link.getFirstId() and step.getId() != link.getSecondId() and step not in first_step_precursor and end_step not in precursor_dict[step.getId()]:
                    # now step is in between, check if there are conflicting states
                    # TODO START
                    effect = link.getEffect()
                    for postcondition in step.getEffect():
                        if postcondition.getPredicate() == effect.getPredicate() and postcondition.getState() != effect.getState():
                            return False
                    # TODO END
                
        return True

    def isSolution(self, plan):
        """
        given a plan, return whether the plan has a solution.
        It is a solution if and only if it is both complete and consistent
	"""        
        return self.isComplete(plan) and self.isConsistent(plan)

    def run_test1_steps(self):
        """
        Complete: True
        Consistent: True
        Solution: True
        Linearization:
	 start
	 move b a table2
	 move c d table3
	 move c table3 b
	 move a table0 table3
	 move d table6 table0
	 finish
        
        """
        steps, ordering_constraints, causal_links = self.get_parameters("test2")
        
        # TODO
        # fill in missing steps, e.g., steps.append(.....)
        steps.append(Step(2, "move c d table3", [Condition(True,"clear c"), Condition(True,"on d c"), Condition(True,"clear table3")], [Condition(True,"on c table3"), Condition(True,"clear d")]))
        steps.append(Step(3, "move c table3 b", [Condition(True,"on c table3"), Condition(True,"clear c"), Condition(True,"clear b")], [Condition(True,"on c b"), Condition(True,"clear table3")]))
        steps.append(Step(4, "move a table0 table3", [Condition(True,"clear table3"), Condition(True,"on a table0"), Condition(True,"clear a")], [Condition(True,"on a table3"), Condition(True,"clear table0")]))
        steps.append(Step(5, "move d table6 table0", [Condition(True,"clear table0"), Condition(True,"on d table6"), Condition(True,"clear d")], [Condition(True,"on d table0"), Condition(True,"clear table6")]))
        steps.append(Step(6, "move b a table2", [Condition(True,"clear b"), Condition(True,"on b a"), Condition(True,"clear table2")], [Condition(True,"on b table2"), Condition(True,"clear a")]))
        
        return steps, ordering_constraints, causal_links
    
    def run_test2_steps(self):
        """
        Complete: True
        Consistent: True
        Solution: True
        Linearization :
	 start
	 move b a table2
	 move a table0 table1
	 move d c table0
	 move c table4 table3
	 finish        
        
        """
        steps, ordering_constraints, causal_links = self.get_parameters("test8")
        
        # TODO
        # fill in missing steps, e.g., steps.append(.....)
        steps.append(Step(2, "move b a table2", [Condition(True, "clear table2"), Condition(True, "on b a"), Condition(True, "clear b")], [Condition(True, "on b table2"), Condition(True, "clear a")]))
        steps.append(Step(3, "move c table4 table3", [Condition(True, "clear table3"), Condition(True, "on c table4"), Condition(True, "clear c")], [Condition(True, "on c table3"), Condition(True, "clear table4")]))
        steps.append(Step(4, "move d c table0", [Condition(True, "on d c"), Condition(True, "clear d"), Condition(True, "clear table0")], [Condition(True, "on d table0"), Condition(True, "clear c")]))
        steps.append(Step(5, "move a table0 table1", [Condition(True, "clear table1"), Condition(True, "clear a")], [Condition(True, "on a table1"), Condition(True, "clear table0")]))
        
        return steps, ordering_constraints, causal_links
    
    def run_test1_ordering_constraints(self):
        """
        Complete: True
        Consistent: True
        Solution: True
        Linearization:
	 start
	 move b table1 table2
	 move c a table1
	 move b table2 c
	 move a table0 b
	 finish
        
        """
        steps, ordering_constraints, causal_links = self.get_parameters("test7")
        
        # TODO
        # fill in missing ordering_constraints, e.g., ordering_constraints.append(.....)
        ordering_constraints.append([0, 1, 2, 3, 4, 5])
        ordering_constraints.append([5, 1, 3, 4])
        ordering_constraints.append([3, 1])
        ordering_constraints.append([4, 1, 3])
        ordering_constraints.append([2, 1, 4, 5])        
        
        return steps, ordering_constraints, causal_links
            
    def run_test2_ordering_constraints(self):
        """
        Complete: True
        Consistent: True
        Solution: True
        Linearization:
	 start
	 move a b table2
	 move d c table3
	 move c table1 d
	 move b table0 c
	 move a table2 b
	 finish
        
        """
        steps, ordering_constraints, causal_links = self.get_parameters("test11")
        
        # TODO
        # fill in missing ordering_constraints, e.g., ordering_constraints.append(.....)     
        ordering_constraints.append([0, 1, 2, 3, 4, 5, 6])
        ordering_constraints.append([2, 1, 3, 4])
        ordering_constraints.append([5, 1, 3, 6])
        ordering_constraints.append([6, 1, 3])
        ordering_constraints.append([3, 1, 4])
        ordering_constraints.append([4, 1])    

        return steps, ordering_constraints, causal_links
    
    def run_test1_causal_links(self):
        """
        Complete: True
        Consistent: True
        Solution: True
        Linearization:
	 Start
	 move a b table1
	 move b table0 a
	 Finish
        
        """
        steps, ordering_constraints, causal_links = self.get_parameters("test3")
        
        # TODO
        # fill in missing causal_links, e.g., causal_links.append(.....)
        causal_links.append(Link(0, 3, Condition(True, "on b table0")))
        causal_links.append(Link(0, 3, Condition(True, "clear a")))
        causal_links.append(Link(0, 2, Condition(True, "on a b")))
        causal_links.append(Link(0, 2, Condition(True, "clear a")))
        causal_links.append(Link(0, 2, Condition(True, "clear table1")))
        causal_links.append(Link(2, 3, Condition(True, "on b table0")))
        causal_links.append(Link(2, 3, Condition(True, "clear a")))
        causal_links.append(Link(2, 3, Condition(True, "clear b")))
        causal_links.append(Link(2, 1, Condition(True, "clear b")))
        causal_links.append(Link(3, 1, Condition(True, "on b a")))
        causal_links.append(Link(3, 1, Condition(True, "clear b")))    
        
        return steps, ordering_constraints, causal_links
            
    def run_test2_causal_links(self):
        """
        Complete: True
        Consistent: True
        Solution: True
        Linearization:
	 start
	 move a b table2
	 move b table0 c
	 move a table2 b
	 finish
        
        """
        steps, ordering_constraints, causal_links = self.get_parameters("test19")
        
        # TODO
        # fill in missing causal_links, e.g., causal_links.append(.....)
        causal_links.append(Link(0, 3, Condition(True, "on a b")))
        causal_links.append(Link(0, 3, Condition(True, "clear a")))
        causal_links.append(Link(0, 3, Condition(True, "clear table2")))
        causal_links.append(Link(0, 4, Condition(True, "on b table0")))
        causal_links.append(Link(0, 4, Condition(True, "clear c")))
        causal_links.append(Link(3, 4, Condition(True, "clear b")))
        causal_links.append(Link(3, 5, Condition(True, "on a table2")))
        causal_links.append(Link(3, 5, Condition(True, "clear b")))
        causal_links.append(Link(0, 1, Condition(True, "on c d")))
        causal_links.append(Link(0, 1, Condition(True, "on d table1")))
        causal_links.append(Link(0, 1, Condition(True, "clear a")))
        causal_links.append(Link(4, 1, Condition(True, "on b c")))
        causal_links.append(Link(4, 1, Condition(True, "clear table0")))
        causal_links.append(Link(5, 1, Condition(True, "on a b")))
        causal_links.append(Link(5, 1, Condition(True, "clear table2")))

        return steps, ordering_constraints, causal_links

def main():
    planner = Planner()
    
    """ Here you can add any code you want (start) """
    steps, ordering_constraints, causal_links  = planner.run_test1_steps()
    planner.run_test(steps, ordering_constraints, causal_links, "test_1_steps")
    
    steps, ordering_constraints, causal_links  = planner.run_test2_steps()
    planner.run_test(steps, ordering_constraints, causal_links, "test_2_steps")
    
    steps, ordering_constraints, causal_links  = planner.run_test1_ordering_constraints()
    planner.run_test(steps, ordering_constraints, causal_links, "test_1_ordering_constraints")
    
    steps, ordering_constraints, causal_links  = planner.run_test2_ordering_constraints()
    planner.run_test(steps, ordering_constraints, causal_links, "test_2_ordering_constraints")    
    
    steps, ordering_constraints, causal_links  = planner.run_test1_causal_links()
    planner.run_test(steps, ordering_constraints, causal_links, "test_1_causal_links")    
    
    steps, ordering_constraints, causal_links  = planner.run_test2_causal_links()
    planner.run_test(steps, ordering_constraints, causal_links, "test_2_causal_links")
    
    test_cases = [x for x in range(1, 23)]
    to_remove = [2, 3, 7, 8, 11, 19]
    
    for i in test_cases:
        if i not in to_remove:
            steps, ordering_constraints, causal_links  = planner.get_parameters("test" + str(i))
            planner.run_test(steps, ordering_constraints, causal_links, "test" + str(i))

    # steps, ordering_constraints, causal_links  = planner.get_parameters("student_test_case")
    # planner.run_test(steps, ordering_constraints, causal_links, "student_test_case")
    """ Here you can add any code you want (end) """
    
if __name__ == '__main__':
    main()


