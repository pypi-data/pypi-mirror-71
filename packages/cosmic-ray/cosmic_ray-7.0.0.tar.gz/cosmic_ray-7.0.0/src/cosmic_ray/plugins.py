"""Query and retrieve the various plugins in Cosmic Ray.
"""

import logging

from stevedore import driver, ExtensionManager

log = logging.getLogger()  # pylint: disable=invalid-name


def _log_extension_loading_failure(_mgr, extension_point, err):
    # We have to log at the `error` level here as opposed to, say, `info`
    # because logging isn't configure when we reach here. We need this infor to
    # print with the default logging settings.
    log.error('Operator provider load failure: extension-point="%s", err="%s"',
              extension_point, err)


OPERATOR_PROVIDERS = {
    extension.name: extension.plugin()
    for extension in ExtensionManager(
        'cosmic_ray.operator_providers',
        on_load_failure_callback=_log_extension_loading_failure)
}


def get_operator(name):
    """Get an operator class from a provider plugin.

    Attrs:
        name: The name of the operator class.

    Returns: The operator *class object* (i.e. not an instance).
    """
    sep = name.index('/')
    provider_name = name[:sep]
    operator_name = name[sep + 1:]

    provider = OPERATOR_PROVIDERS[provider_name]
    return provider[operator_name]


def operator_names():
    """Get all operator names.

    Returns: A sequence of operator names.
    """
    return tuple('{}/{}'.format(provider_name, operator_name)
                 for provider_name, provider in OPERATOR_PROVIDERS.items()
                 for operator_name in provider)


def get_execution_engine(name):
    """Get the execution engine by name."""
    manager = driver.DriverManager(
        namespace='cosmic_ray.execution_engines',
        name=name,
        invoke_on_load=True,
        on_load_failure_callback=_log_extension_loading_failure,
    )

    return manager.driver


def execution_engine_names():
    """Get all execution-engine plugin names.

    Returns: A sequence of execution-engine names.
    """
    return ExtensionManager(
        'cosmic_ray.execution_engines',
        on_load_failure_callback=_log_extension_loading_failure,
    ).names()
