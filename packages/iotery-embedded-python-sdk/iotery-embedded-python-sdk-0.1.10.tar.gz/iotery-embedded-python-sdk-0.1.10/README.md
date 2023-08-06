# iotery.io Embedded Python SDK

The python iotery.io SDK is intended to be used on your embedded device to interact with the itoery.io IoT Platform. The SDK is a fully featured wrapper for the [REST API](https://iotery.io/docs/embedded).

## Getting Started

Setup your free account on [iotery.io](https://dashboard.iotery.io) and go to your [dashboard](https://iotery.io/devices) get started with creating device types and devices.

After you get your key, install the SDK:

```bash
pip install iotery-embedded-python-sdk
```

> Note: Make sure you are using Python 3.5+!

And finally, some simple example usage:

```python
from iotery_embedded_python_sdk import Iotery
TEAM_ID="265fcb74-8889-11f9-8452-d283610663ec" # team ID found on the dashboard: https://iotery.io/system
iotery = Iotery()
d = iotery.getDeviceTokenBasic(data={"key": "thermal_sensor_001",
                                     "serial": "THERMAL_SENSOR_001", "secret": "thermal_sensor_001_secret", "teamUuid": TEAM_ID})
iotery.set_token(d["token"])
me = iotery.getMe()

print(me["name"])

```

## API

This SDK simply wraps the [REST API](https://iotery.io/docs/embedded), so more information and specifics can be found there. Since the API is a wrapper around the REST API, the syntax is standard for each of the Create, Read, Update, and Delete operations on iotery.io resources. All methods return a dictonary containing the API response. If there is an error, the method will `raise` an expection.

### Creating Resources

The generalized syntax for creating resources in iotery.io python sdk looks like:

```python
iotery.methodName(inputParameter="parameter", data={ "data": "variables" })
```

For example, to create a device, the python would look like

```python
createDeviceCommandInstanceEmbedded(
  deviceUuid="a-valid-device-type-uuid",
  commandTypeUuid="a-valid-command-type-uuid",
  data={}
)
```

where `createDeviceCommandInstanceEmbedded` maps to `methodName`, `deviceUuid` maps to `inputParameter`, and `data={}` and maps to the dictonary `{data : "variables"}` in the generalized form given above.

The available resource creation (POST) methods are

|            `methodName`             |                                                                                  `input`                                                                                  |                                                                link                                                                |              `description`              |
| :---------------------------------: | :-----------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :--------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------: |
|         getDeviceTokenBasic         |          `` | [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1basic~1get-token/post) | Get token for device via key, serial, and secret.           |
|    reportAlreadyExecutedCommands    | `` | [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1command-instances~1executed/post) | Report an already executed set of commands to the server. |
| createDeviceCommandInstanceEmbedded |                                                                      `deviceUuid`,`commandTypeUuid`                                                                       | [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1devices~1:deviceUuid~1command-types~1:commandTypeUuid/post) | Create a command instance via a device. |
|              postData               |                                                                               `deviceUuid`                                                                                |              [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1devices~1:deviceUuid~1data/post)               |         Post data to the cloud.         |
|        upsertDeviceSettings         |                                                                               `deviceUuid`                                                                                |            [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1devices~1:deviceUuid~1settings/post)             |      Upsert settings for a device.      |
|          uploadDeviceLogs           |                                                                               `deviceUuid`                                                                                |         [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1devices~1:deviceUuid~1upload-log-file/post)         |     Upload zip file of device logs.     |
|      getDeviceTokenAsymmetric       |          `` | [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1token~1asymmetric/post) | Get device token based on encrypted credentials.           |

### Reading Resources

The generalized syntax for reading (getting) resources in iotery.io python sdk looks like:

```python
iotery.methodName(inputParameter="parameter", opts={"query":"parameter"})
```

For example, to get a device by it's unique identifier `uuid`, the python would look like

```python
getDeviceTypeFirmwareRecord(
  deviceUuid="a-valid-device-uuid",
  version="valid version",
  opts={ "limit": 1 }
)
```

where `getDeviceTypeFirmwareRecord` maps to `methodName`, `deviceUuid` maps to `inputParameter`, and `{ "limit": 1 }` maps to the dictonary `{"query" : "parameters"}` in the generalized form given above.

> The `limit` option is for instructive purposes only. By definition, a `uuid` is unique and so there will never be more than one device for a given `uuid`.

The available resource creation methods are

|              `methodName`              |                                                                           `input`                                                                           |                                                         link                                                          |                            `description`                            |
| :------------------------------------: | :---------------------------------------------------------------------------------------------------------------------------------------------------------: | :-------------------------------------------------------------------------------------------------------------------: | :-----------------------------------------------------------------: |
|            getBrokerAddress            |               `` | [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1broker-address/get) | Get the MQTT broker address.                |
|       getCommandTypeListEmbedded       |           `` | [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1command-types/get) | Get a list of available command types.           |
|          getCurrentTimestamp           |   `` | [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1current-timestamp/get) | Get the current server time in epoch (unix) time.    |
|        getDataTypeListEmbedded         |              `` | [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1data-types/get) | Get a list of available data types.              |
| getDeviceUnexecutedCommandInstanceList |                                                                        `deviceUuid`                                                                         | [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1devices~1:deviceUuid~1unexecuted-commands/get) |      Get a list of unexecuted command instances for a device.       |
|      getDeviceTypeFirmwareRecord       |                                                                 `deviceTypeUuid`,`version`                                                                  |    [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1firmware~1:deviceTypeUuid~1:version/get)    | Get a desired version of a firmware record for a given device type. |
|           getPublicCloudKey            | `` | [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1key/get) | Get base64 encoded public key from the server for use in RSA scheme. |
|                 getMe                  |                   `` | [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1me/get) | Get information about the device.                   |
|      getNotificationListEmbedded       |           `` | [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1notifications/get) | Get a list of available notifications.           |
|       getSettingTypeListEmbedded       |           `` | [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1setting-types/get) | Get a list of available setting types.           |

### Updating Resources

The generalized syntax for updating resources in iotery.io python sdk looks like:

```python
iotery.methodName(inputParameter="parameter", data={ "data": "variables" })
```

For example, to update a device type, the code would look like

```python
updateDeviceChannel(
  deviceUuid="a-valid-device-type-uuid",
  channelId="1",
  data={}
)
```

where `updateDeviceChannel` maps to `methodName`, `deviceUuid` maps to `inputParameter`, and `{}` maps to the dictonary `{data : "variables"}` in the generalized form given above (if there was a body).

The available resource creation methods are

|             `methodName`             |                                                                                                `input`                                                                                                 | link | `description` |
| :----------------------------------: | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :--: | :-----------: |
| setBatchedCommandInstancesAsExecuted | `` | [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1batch-command-instances~1:batchReferenceUuid~1executed/patch) | Set a collection of batched command instances as executed. |
|     setCommandInstanceAsExecuted     |     `` | [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1command-instances~1:commandInstanceUuid~1executed/patch) | Report that a command has been executed to the server.      |
|         updateDeviceChannel          |                        `` | [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1devices~1:deviceUuid~1channelId~1:channelId/patch) | Update device channel.                         |
|   setNotificationInstanceInactive    |          `` | [link](https://iotery.io/docs/embedded/#tag/Embedded/paths/~1embedded~1notification-instances~1:notificationInstanceUuid~1inactive/patch) | Set notification instance inactive.          |

### Deleting Resources

The generalized syntax for reading (getting) resources in iotery.io python sdk looks like:

```python
iotery.methodName(inputParameter="parameter", opts={"query":"parameter"})
```

For example, to get a device by it's unique identifier `uuid`, the python would look like

```python
deleteDevice(
  deviceUuid="a-valid-device-uuid",
  opts={ "some": "option" }
)
```

where `deleteDevice` maps to `methodName`, `deviceUuid` maps to `inputParameter`, and `{ "some": "option" }` maps to the dictonary `{"query" : "parameters"}` in the generalized form given above.

The available resource creation methods are

| `methodName` | `input` | link | `description` |
| :----------: | :-----: | :--: | :-----------: |


## Contributing

We welcome contributors and PRs! Let us know if you are interested.
