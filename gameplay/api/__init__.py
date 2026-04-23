from tools.loader import load_from_package

raw_initials = load_from_package(__name__, "initial")
raw_resolvers = load_from_package(__name__, "resolve")
domains = load_from_package(__name__, "domain")

initial_state = {}
resolvers = {}
for path_to_file, domain in domains.items():
    if domain in initial_state:
        raise ValueError(f"Duplicate domain '{domain}' found in {path_to_file}")

    initial_state[domain] = raw_initials[path_to_file]
    resolvers[domain] = raw_resolvers[path_to_file]
