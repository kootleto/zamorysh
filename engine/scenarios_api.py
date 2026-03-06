import inspect
from . import gs_api
from tools import logger


def base_scenario(transitions=None, start_node=0):
    return {
        "start_node": start_node,
        "transitions": transitions,
    }


def base_transition(node_from, node_to, trigger, effect):
    return {
        "from": node_from,
        "to": node_to,
        "trigger": trigger,
        "effect": effect,
    }


def get_start_node(scenario):
    return scenario["start_node"]


def get_transitions(scenario):
    return scenario["transitions"]


def get_node_from(transition):
    return transition["from"]


def get_node_to(transition):
    return transition["to"]


def check_trigger(gs, transition):
    return transition["trigger"](gs)


def apply_effect(gs, transition):
    transition["effect"](gs)


def set_node(entry, node):
    entry["node"] = node


def get_node(entry):
    return entry["node"]


def start_scenario(gs, definitions, scenario_entry):
    scenario = configure_scenario(definitions, scenario_entry)
    set_node(scenario_entry, get_start_node(scenario))
    entry_with_id = gs_api.with_id(gs, scenario_entry)
    gs["scenario_entries"].append(entry_with_id)


def create_scenario_entry(definition):
    scenario_name = f"{definition.__module__}.{definition.__name__}"

    sig = inspect.signature(definition)
    state = None
    if "state" in sig.parameters:
        state = {}

    return {
        "scenario_name": scenario_name,
        "node": None,
        "state": state,
    }


def configure_scenario(definitions, entry):
    logger.log(f"Scenario entry: {entry}", log_type="config")

    definition = definitions[entry["scenario_name"]]
    state = entry["state"]

    sig = inspect.signature(definition)

    kwargs = {}
    if "state" in sig.parameters:
        kwargs["state"] = state

    return definition(**kwargs)


def start_all_scenarios(gs, definitions):
    for definition in definitions.values():
        entry = create_scenario_entry(definition)
        start_scenario(gs, definitions, entry)


def init_fn(state, fn):
    # Этот метод инициализации подходит, если изначальный state вычисляется на основе параметра
    # Он позволяет вызывать логику инициализации только в том случае, если state еще не инициализирован
    if state is None:
        return fn()
    elif state == {}:
        state.update(fn())
    return state
