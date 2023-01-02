import gopy
import json


def install_chart(chart_dir, release_name, values, client, flags=None):
    """Installs a Helm chart to a Kubernetes cluster.

    Arguments:
    chart_dir -- the directory containing the chart files
    release_name -- the name of the release
    values -- a dictionary of chart values
    client -- a Helm client
    flags -- a list of flags to pass to the Install function (default: None)

    """
    # Convert the chart values to a JSON string
    values_json = json.dumps(values)

    # Create a Go string containing the chart values
    values_go = gopy.gostring(values_json)

    # Install the chart
    install_args = [client, "InstallRelease", chart_dir, release_name,
                    helm.ValueOverrides(values_go)]
    if flags is not None:
        for flag in flags:
            flag_args = [flag[0]]
            flag_args.extend(flag[1:])
            install_args.extend(flag_args)
    _, err = gopy.run(*install_args)
    if err is not None:
        raise err


def uninstall_chart(release_name, client, flags=None):
    """Uninstalls a Helm chart from a Kubernetes cluster.

    Arguments:
    release_name -- the name of the release
    client -- a Helm client
    flags -- a list of flags to pass to the Delete function (default: None)

    """
    # Uninstall the chart
    delete_args = [client, "DeleteRelease", release_name]
    if flags is not None:
        for flag in flags:
            flag_args = [flag[0]]
            flag_args.extend(flag[1:])
            delete_args.extend(flag_args)
    _, err = gopy.run(*delete_args)
    if err is not None:
        raise err


def create_client():
    """Creates a client for interacting with the Tiller server."""
    return gopy.run("helm.NewClient", helm.Host("localhost:44134"))
