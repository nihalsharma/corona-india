from pymongo import MongoClient

from settings.settings import MONGODB_HOST


class _DBConnSingleton(object):
    class __DBConnection:
        connection = None

        def __init__(self):
            self.client = MongoClient(MONGODB_HOST, 27017)
            self.db = self.client['trackerDB']

        def get_client(self):
            return self.client, self.db

        def save_details(self, details):
            from api import cache_manager
            collection = self.db['vehicleLocations']
            collection3 = self.db['trip_running_vehicles_details']

            gps_mapping_collection = self.db['vehicle_gps_mapping']
            gps_mapping_cursor = gps_mapping_collection.find()
            mapping_result = list(gps_mapping_cursor)
            mapping_list = {}

            # Convert data from mongo to the form {'vehicle_no': 'gps_used'}
            for x in mapping_result:
                mapping_list[x['vehicle']] = x['gps_used']

            vehicles, vehicles3 = [], []

            for detail in details:
                vehicle_number = detail.get('vehicle', '')
                if vehicle_number not in mapping_list or mapping_list[vehicle_number] == detail.get('gps_provider', '') or \
                        detail.get('gps_provider', '') == 'Manual':
                    cursor3 = collection3.find(
                        {'vehicle': detail.get('vehicle', ''), 'recorded_at': detail.get('recorded_at')}).limit(1)
                    result3 = list(cursor3)
                    if not result3:
                        vehicles3.append(detail)

                        # check if data not already present in 'vehicleLocations' db
                        cursor = collection.find(
                            {'vehicle': detail.get('vehicle', ''), 'recorded_at': detail.get('recorded_at')}).limit(1)

                        result = list(cursor)
                        if not result:
                            vehicles.append(detail)

            if vehicles3:
                try:
                    collection3.insert_many(vehicles3)
                    cache_manager.set_latest_vehicle_details_in_cache(vehicles3)
                except Exception as ex:
                    print('Error: collection3.insert_many(details) - ' + str(ex))
            if vehicles:
                try:
                    collection.insert_many(vehicles)
                except Exception as ex:
                    print('Error: collection.insert_many(details) - ' + str(ex))

    def __init__(self):
        # just for the sake of information
        self.db_conn = _DBConnSingleton.__DBConnection()


_db_singleton = _DBConnSingleton()


def DBConnection():
    return _db_singleton
