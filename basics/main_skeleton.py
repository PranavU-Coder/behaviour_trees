from skeleton_behaviour import Foo
import py_trees

foo_behavior = Foo("My Foo Behavior")

foo_behavior.setup()

for i in range(5):
    print(f"\n--- Tick {i+1} ---")
    
    if foo_behavior.status != py_trees.common.Status.RUNNING:
        foo_behavior.initialise()
    
    status = foo_behavior.update()
    
    print(f"Status: {status}")
    print(f"Feedback: {foo_behavior.feedback_message}")
        
    if status != py_trees.common.Status.RUNNING:
        foo_behavior.terminate(status)
