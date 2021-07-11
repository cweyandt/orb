"""Tutorial for using pandas and the InfluxDB client."""
# !pip install --upgrade influxdb
from influxdb import DataFrameClient
# from Influx_Dataframe_Client import Influx_Dataframe_Client
import yaml

database = 'wifi'
measurement = 'wifi_count'
fields = ["max(connected_devices)"]
tags_list = ['building']
values_list = ['67']
group_list=['ap_name']
group_time=['5m']

client = Influx_Dataframe_Client('./cloudserver.ini')


"""
read config file
"""
config_file = 'influx_host.ini'

if not os.path.exists("./" + config_file):
    self.logger.error("cannot find config_file=%s" % self.config_file)
    raise Exception("config file not found")

with open(self.project_path + "/" + self.config_file, "r") as fp:
    self.config = yaml.safe_load(fp)
self.logger.info("successfully loaded config_file=%s" % self.config_file)

try:
    snmp_cfg = self.config[self.snmp_section]
    self.input_from_file = snmp_cfg.get("input_from_file", False)
    self.input_file_name = snmp_cfg.get("input_file_name", None)

    if self.input_file_name:
        if self.input_file_name is None:
            raise Exception("Missing configuration parameter: input_file_name")

    self.community = str(snmp_cfg.get("community"))
    self.controller_ip = str(snmp_cfg.get("controller_ip"))
    self.oid = str(snmp_cfg.get("count_oid"))
    if not self.oid.startswith('.'):
        self.oid = '.'+self.oid
    if self.oid.endswith('.'):
        self.oid = self.oid[:-1]
except Exception as e:
    self.logger.error(
        "unexpected error while setting configuration from config_file=%s, section=%s, error=%s" % (
        self.config_file, self.snmp_section, str(e)))
    raise e



client2 = DataFrameClient(client.host, client.port, client.username, client.password, client.database, ssl=True, verify_ssl=True)

query_auto = """SELECT "connected_devices" FROM "wifi_count" WHERE time > '2020-01-01 00:00:00' AND time < '2020-05-01 00:00:00' AND "building" = '91'"""

qa1 = client2.query(query_auto)
qa2 = client2.query(query_auto, data_frame_index=["time"])
qa2['wifi_count'].plot()

data = client2.query("""SELECT max("connected_devices") FROM "wifi_count" """ + \
                      """WHERE ("building" = '91') AND """ + \
                      """time > '2020-05-01 00:00:00' AND time < '2021-05-06 00:00:00' """ + \
                      """GROUP BY time(5m), "ap_name" fill(null)""")
