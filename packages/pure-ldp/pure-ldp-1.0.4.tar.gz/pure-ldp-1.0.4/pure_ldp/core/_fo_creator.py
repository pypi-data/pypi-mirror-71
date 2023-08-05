
def create_fo_client_instance(name, client_params):
    split = name.split("_")
    prefix = (split[0][0] + split[1][0]).upper() # Get prefix of method name i.e if passed "local_hashing" get "LH" as prefix
    if prefix == "HR":
        prefix = "HadamardResponse"

    client_constructor = globals().get(prefix + "Client")

    if client_constructor is None:
        raise ValueError("Must provide valid frequency oracle name")

    return client_constructor(**client_params)


def create_fo_server_instance(name, server_params):
    split = name.split("_")
    prefix = (split[0][0] + split[1][0]).upper()
    server_constructor = globals().get(prefix + "Server")

    if prefix == "HR":
        prefix = "HadamardResponse"

    if server_constructor is None:
        raise ValueError("Must provide valid frequency oracle name")

    return server_constructor(**server_params)
