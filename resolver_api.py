from collections import defaultdict

import ui_api


def resolve_intents(gs):
    grouped_intents = defaultdict(list)
    for intent in gs["intents"]:
        grouped_intents[intent["type"]].append(intent)
    ui_api.log("Raw Intents: ", dict(grouped_intents), log_type="resolver")
    for intent_type, intents in grouped_intents.items():
        resolver_name = f"resolve_{intent_type}s"
        if resolver_name in globals():
            globals()[resolver_name](gs, intents)
        else:
            raise NotImplementedError(
                f"No resolver implemented for intent type '{intent_type}'"
            )
    gs["intents"].clear()


def resolve_generic(gs, intents, gs_key, set_fn=max, mod_fn=sum, clamp_fn=lambda x: x):
    grouped_intents = defaultdict(lambda: {"mod": [], "set": []})
    for intent in intents:
        grouped_intents[intent["target"]][intent["op"]].append(intent)
    for target, grouped in grouped_intents.items():
        if grouped["set"]:
            value = set_fn([i["value"] for i in grouped["set"]])
        else:
            value = gs[gs_key][target]
        value += mod_fn([i["value"] for i in grouped["mod"]])
        value = clamp_fn(value)
        ui_api.log(f"{target} {gs[gs_key][target]} -> {value}", log_type="resolver")
        gs[gs_key][target] = value


def resolve_vitals(gs, intents):
    resolve_generic(
        gs,
        intents,
        "vitals",
        set_fn=max,
        mod_fn=sum,
        clamp_fn=lambda v: max(0, min(100, v)),
    )


def resolve_stats(gs, intents):
    resolve_generic(
        gs,
        intents,
        "stats",
        set_fn=min,
        mod_fn=sum,
        clamp_fn=lambda v: max(0, v),
    )


def resolve_flags(gs, intents):
    resolve_generic(
        gs,
        intents,
        "flags",
        set_fn=any,
        clamp_fn=lambda v: v,
    )
