from step import Step
from condition import Condition
from link import Link

steps = []
steps.append(Step(0, "start", [], [Condition(True, "on b table0"), Condition(True, "on a b"), Condition(True, "clear a"), Condition(True, "clear table1"), Condition(True, "on c table2"), Condition(True, "clear c"), Condition(True, "on d table3"), Condition(True, "clear d")]))
steps.append(Step(1, "finish", [Condition(True, "on a table1"), Condition(True, "on b a"), Condition(True, "on c b"), Condition(True, "on d c"), Condition(True, "clear table0"), Condition(True, "clear table2"), Condition(True, "clear table3")], []))
steps.append(Step(2, "move a b table1", [Condition(True, "clear a"), Condition(True, "on a b"), Condition(True, "clear table1")], [Condition(True, "on a table1"), Condition(True, "clear b")]))
steps.append(Step(3, "move b table0 a", [Condition(True, "clear b"), Condition(True, "on b table0"), Condition(True, "clear a")], [Condition(True, "on b a"), Condition(True, "clear table0")]))
steps.append(Step(4, "move c table2 b", [Condition(True, "clear c"), Condition(True, "on c table2"), Condition(True, "clear b")], [Condition(True, "on c b"), Condition(True, "clear table2")]))
steps.append(Step(5, "move d table3 c", [Condition(True, "clear d"), Condition(True, "on d table3"), Condition(True, "clear c")], [Condition(True, "on d c"), Condition(True, "clear table3")]))

ordering_constraints = []
ordering_constraints.append([0, 1, 2, 3, 4, 5])
ordering_constraints.append([2, 1, 3, 4, 5])
ordering_constraints.append([3, 1, 4, 5])
ordering_constraints.append([4, 1, 5])
ordering_constraints.append([5, 1])

causal_links = []
causal_links.append(Link(0, 2, Condition(True, "clear a")))
causal_links.append(Link(0, 2, Condition(True, "on a b")))
causal_links.append(Link(0, 2, Condition(True, "clear table1")))
causal_links.append(Link(0, 3, Condition(True, "on b table0")))
causal_links.append(Link(0, 3, Condition(True, "clear a")))
causal_links.append(Link(0, 4, Condition(True, "clear c")))
causal_links.append(Link(0, 4, Condition(True, "on c table2")))
causal_links.append(Link(0, 5, Condition(True, "clear d")))
causal_links.append(Link(0, 5, Condition(True, "on d table3")))
causal_links.append(Link(0, 5, Condition(True, "clear c")))
causal_links.append(Link(2, 3, Condition(True, "clear b")))
causal_links.append(Link(2, 4, Condition(True, "clear b")))
causal_links.append(Link(5, 1, Condition(True, "on d c")))
causal_links.append(Link(5, 1, Condition(True, "clear table3")))
causal_links.append(Link(4, 1, Condition(True, "on c b")))
causal_links.append(Link(4, 1, Condition(True, "clear table2")))
causal_links.append(Link(3, 1, Condition(True, "on b a")))
causal_links.append(Link(3, 1, Condition(True, "clear table0")))
causal_links.append(Link(2, 1, Condition(True, "on a table1")))

