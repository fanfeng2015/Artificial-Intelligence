from step import Step
from condition import Condition
from link import Link

steps=[]
steps.append(Step(0,"start",[],[Condition(True,"on b table0"),Condition(True,"on a b"),Condition(True,"clear a"),Condition(True,"clear table1"),Condition(True,"on c table2"),Condition(True,"clear c"),Condition(True,"on d table3"),Condition(True,"on e d"),Condition(True,"clear e"),Condition(True,"clear table4")]))
steps.append(Step(1,"finish",[Condition(True,"on b table2"),Condition(True,"on c b"),Condition(True,"on d c"),Condition(True,"on e a")],[]))
steps.append(Step(2,"move c table2 table4",[Condition(True,"clear c"),Condition(True,"on c table2"),Condition(True,"clear table4")],[Condition(True,"clear table2"),Condition(False,"clear table4"),Condition(True,"on c table4")]))
steps.append(Step(3,"move a b table1",[Condition(True,"on a b"),Condition(True,"clear a"),Condition(True,"clear table1"),],[Condition(True,"clear b"),Condition(False,"clear table1"),Condition(True,"on a table1")]))
steps.append(Step(4,"move e d a",[Condition(True,"clear e"),Condition(True,"clear a"),Condition(True,"on e d")],[Condition(False,"clear a"),Condition(True,"on e a"),Condition(False,"on e d"),Condition(True,"clear d")]))
steps.append(Step(5,"move c table4 b",[Condition(True,"on c table4"),Condition(True,"clear b"),Condition(True,"clear c")],[Condition(False,"clear b"),Condition(True,"on c b"),Condition(True,"clear table4")]))
steps.append(Step(6,"move b table0 table2 ",[Condition(True,"clear b"),Condition(True,"on b table0"),Condition(True,"clear table2")],[Condition(True,"on b table2"),Condition(False,"clear table2"),Condition(True,"clear table0")]))
steps.append(Step(7,"move d table3 c",[Condition(True,"on d table3"),Condition(True,"clear c"),Condition(True,"clear d")],[Condition(False,"clear c"),Condition(True,"on d c"),Condition(True,"clear table3")]))

ordering_constraints=[]
ordering_constraints.append([0,7,6,5,4,3,2,1])
ordering_constraints.append([3,7,6,5,4,2,1])
ordering_constraints.append([2,7,6,5,4,1])
ordering_constraints.append([4,7,6,5,1])
ordering_constraints.append([5,7,1])
ordering_constraints.append([6,7,5,1])
ordering_constraints.append([7,1])

causal_links=[]
causal_links.append(Link(0,2,Condition(True,"on a b")))
causal_links.append(Link(0,2,Condition(True,"clear a")))
causal_links.append(Link(0,2,Condition(True,"clear table1")))
causal_links.append(Link(0,3,Condition(True,"on c table2")))
causal_links.append(Link(0,3,Condition(True,"clear c")))
causal_links.append(Link(0,3,Condition(True,"clear table4")))
causal_links.append(Link(0,4,Condition(True,"clear e")))
causal_links.append(Link(0,4,Condition(True,"clear a")))
causal_links.append(Link(0,4,Condition(True,"on e d")))
causal_links.append(Link(0,5,Condition(True,"on b table0")))
causal_links.append(Link(0,7,Condition(True,"clear c")))
causal_links.append(Link(0,6,Condition(True,"on d table3")))
causal_links.append(Link(0,6,Condition(True,"clear c")))
causal_links.append(Link(4,6,Condition(True,"clear d")))
causal_links.append(Link(2,5,Condition(True,"clear b")))
causal_links.append(Link(3,5,Condition(True,"clear table2")))
causal_links.append(Link(2,7,Condition(True,"clear b")))
causal_links.append(Link(3,7,Condition(True,"on c table4")))
causal_links.append(Link(4,7,Condition(True,"clear table4")))
causal_links.append(Link(5,1,Condition(True,"on b table2")))
causal_links.append(Link(7,1,Condition(True,"on c b")))
causal_links.append(Link(6,1,Condition(True,"on d c")))
causal_links.append(Link(4,1,Condition(True,"on e a")))

