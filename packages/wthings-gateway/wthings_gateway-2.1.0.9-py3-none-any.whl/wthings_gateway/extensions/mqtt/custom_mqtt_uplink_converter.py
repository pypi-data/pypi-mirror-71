from simplejson import dumps
from wthings_gateway.connectors.mqtt.mqtt_uplink_converter import MqttUplinkConverter, log


class CustomMqttUplinkConverter(MqttUplinkConverter):
    def __init__(self, config):
        self.__config = config.get('converter')
        self.dict_result = {}

    def convert(self, topic, body):
        try:
            '''  getting device name from topic, next line will get all data after last '/' symbol 
             in this case: if topic = 'devices/temperature/sensor1' device name will be 'sensor1'.'''
            self.dict_result["deviceName"] = topic.split("/")[-1]
            self.dict_result["deviceType"] = "Thermostat"  # just hardcode this
            self.dict_result["telemetry"] = []  # template for telemetry array
            bytes_to_read = body.replace("0x", "")  # Replacing the 0x (if '0x' in body), needs for converting to bytearray
            converted_bytes = bytearray.fromhex(bytes_to_read)  # Converting incoming data to bytearray
            if self.__config.get("extension-config") is not None:
                for telemetry_key in self.__config["extension-config"]:  # Processing every telemetry key in config for extension
                    value = 0
                    for current_byte_position in range(self.__config["extension-config"][telemetry_key]):  # reading every value with value length from config
                        value = value*256 + converted_bytes.pop(0)  # process and remove byte from processing
                    telemetry_to_send = {telemetry_key.replace("Bytes", ""): value}  # creating telemetry data for sending into WThings
                    self.dict_result["telemetry"].append(telemetry_to_send)  # adding data to telemetry array
            else:
                self.dict_result["telemetry"] = {"data": int(body, 0)}  # if no specific configuration in config file - just send data which received
            return self.dict_result

        except Exception as e:
            log.exception('Error in converter, for config: \n%s\n and message: \n%s\n', dumps(self.__config), body)
            log.error(e)
