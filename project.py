# TODO: Write some tests
import sys
import argparse
import scheduler.io as io
import scheduler.simulation as sim
import scheduler.generation as generation
import scheduler.priority as priority

def handle_command():
    arg_parser = argparse.ArgumentParser(
        description="Simulate dual priority scheduling algorithm"
    )
    subparsers = arg_parser.add_subparsers()
    
    parser_gen = subparsers.add_parser(
        "gen",
        help="Generate a system of random, periodic, asynchronous tasks with implicit deadlines"
    )
    parser_gen.add_argument("tasks_number", type=int)
    parser_gen.add_argument("utilization", type=int)
    parser_gen.add_argument("output_file")
    parser_gen.set_defaults(func=gen_command)

    parser_fdms = subparsers.add_parser(
        "fdms",
        help="Determine promotion deadlines for the given task set"
    )
    parser_fdms.add_argument("task_file")
    parser_fdms.set_defaults(func=fdms_command)

    parser_simulation = subparsers.add_parser(
        "simulation",
        help="Simulate the execution of the given task set"
    )
    parser_simulation.add_argument("task_file")
    parser_simulation.add_argument("end_time", type=int)
    parser_simulation.set_defaults(func=simulation_command)

    parser_simulation_graph = subparsers.add_parser(
        "simulation_graph",
        help="Generate a graph for the simulation of the given task set"
    )
    parser_simulation_graph.add_argument("task_file")
    parser_simulation_graph.add_argument("end_time", type=int)
    parser_simulation_graph.set_defaults(func=simulation_graph_command)
    
    args = arg_parser.parse_args()
    args.func(args)
    
def gen_command(args):
    if (args.tasks_number > args.utilization):
        print("Please set a utilization greater than the number of tasks")
        return
    tasks = generation.gen(args.tasks_number, args.utilization)
    io.write_tasks(args.output_file, tasks)

def fdms_command(args):
    tasks = io.parse_tasks(args.task_file)
    if priority.set_priority(tasks):
        io.print_fdms(tasks)
    else:
        print("UNFEASIBLE")

def simulation_command(args):
    tasks = io.parse_tasks(args.task_file)
    priority.set_priority(tasks) # TODO: Handle case where set_promotion deadlines fails?
    sim_result = sim.simulation(tasks, args.end_time)
    io.print_simulation_result(sim_result, tasks, args.end_time)

def simulation_graph_command(args):
    tasks = io.parse_tasks(args.task_file)
    priority.set_priority(tasks) # TODO: Handle the case where set_promotion deadline fails?
    simulation_result = sim.simulation(tasks, args.end_time)
    io.display_simulation_graph(simulation_result)

if __name__ == '__main__':
    handle_command()
