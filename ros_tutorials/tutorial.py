#!/home/pranav/Projects/behaviour_trees/.venv/bin/pythonv

# The above line is shebang command in case it was not understood

import random
import typing
import py_trees

def tutorial_create_root() -> py_trees.behaviour.Behaviour:

    """
    Create a basic tree and start a 'Topics2BB' work sequence that
    will become responsible for data gathering behaviours.

    Returns:
        the root of the tree
    """

    root = py_trees.composites.Parallel(

        name="Tutorial One",
        policy=py_trees.common.ParallelPolicy.SuccessOnAll(
            synchronise=False
        )
    )


    topics2bb = py_trees.composites.Sequence(name="Topics2BB", memory=True)

    battery2bb = py_trees_ros.battery.ToBlackboard(
        name="Battery2BB",
        topic_name="/battery/state",
        qos_profile=py_trees_ros.utilities.qos_profile_unlatched(),
        threshold=30.0
    )

    priorities = py_trees.composites.Selector(name="Tasks", memory=False)
    idle = py_trees.behaviours.Running(name="Idle")
    flipper = py_trees.behaviours.Periodic(name="Flip Eggs", n=2)

    root.add_child(topics2bb)
    topics2bb.add_child(battery2bb)
    root.add_child(priorities)
    priorities.add_child(flipper)
    priorities.add_child(idle)

    """
    Create a basic tree with a battery to blackboard writer and a
    battery check that flashes the LEDs on the mock robot if the
    battery level goes low.
    
    Returns:

        the root of the tree

    """

    root = py_trees.composites.Parallel(

        name="Tutorial Two",
        policy=py_trees.common.ParallelPolicy.SuccessOnAll(
            synchronise=False
        )
    )


    topics2bb = py_trees.composites.Sequence(name="Topics2BB", memory=True)

    battery2bb = py_trees_ros.battery.ToBlackboard(
        name="Battery2BB",
        topic_name="/battery/state",
        qos_profile=py_trees_ros.utilities.qos_profile_unlatched(),
        threshold=30.0
    )

    tasks = py_trees.composites.Selector("Tasks", memory=False)

    flash_led_strip = behaviours.FlashLedStrip(
        name="FlashLEDs",
        colour="red"
    )


    def check_battery_low_on_blackboard(blackboard: py_trees.blackboard.Blackboard) -> bool:
        return blackboard.battery_low_warning


    battery_emergency = py_trees.decorators.EternalGuard(
        name="Battery Low?",
        condition=check_battery_low_on_blackboard,
        blackboard_keys={"battery_low_warning"},
        child=flash_led_strip
    )

    idle = py_trees.behaviours.Running(name="Idle")
    root.add_child(topics2bb)
    topics2bb.add_child(battery2bb)
    root.add_child(tasks)
    tasks.add_children([battery_emergency, idle])

    return root
