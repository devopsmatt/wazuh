from pydantic import BaseModel, FilePath, PositiveInt, PositiveFloat
from wazuh.core.config.models.logging import LoggingConfig


# TODO(#25121): Change the socket path once the Cpp team does it
class EngineClientConfig(BaseModel):
    """Configuration for the Engine client.

    Parameters
    ----------
    api_socket_path : FilePath
        The path to the API socket. Default: "/var/wazuh/queue/engine.sock".
    retries : PositiveInt
        The number of retry attempts. Default: 3.
    timeout : PositiveFloat
        The timeout duration in seconds. Default: 10.0.
    """
    api_socket_path: FilePath = "/var/wazuh/queue/engine.sock"
    retries: PositiveInt = 3
    timeout: PositiveFloat = 10


class EngineConfig(BaseModel):
    """Configuration for the Engine.

    Parameters
    ----------
    tzdv_automatic_update : bool
        Whether to enable automatic updates for TZDV. Default: False.
    client : EngineClientConfig
        Configuration for the Engine client. Default is an instance of EngineClientConfig.
    logging : LoggingConfig
        Configuration for logging. Default is an instance of LoggingConfig.
    """
    tzdv_automatic_update: bool = False
    client: EngineClientConfig() = EngineClientConfig()
    logging: LoggingConfig = LoggingConfig()
