from tests.test_config import client

request_data = {
    "load_id": "123456",
    "load_creation_date_time": "22-12-2022",
    "business_unit": "string",
    "load_reference_number": "1",
    "customer_id": "21",
    "fuel_surcharge": "string",
    "additional_charge": "string",
    "number_of_stops": "string",
    "total_loaded_miles": "string",
    "last_segment_miles": "string",
    "pickup_appointment_start_date_time": "12-12-2022",
    "pickup_appointment_end_date_time": "25-12-2022",
    "delivery_appointment_start_date_time": "12-12-2022",
    "delivery_appointment_end_date_time": "25-12-2022",
    "required_equipment": "string",
    "hazmat": "string",
    "commodity_type": "string",
    "load_max_weight": "string",
    "critical": "string",
    "load_status": "string",
    "pickup_status": "string",
    "delivery_status": "string",
    "pickup_arrival_actual_date_time": "string",
    "delivery_arrival_actual_date_time": "string",
    "scenario_id": "string",
    "load_total_revenue": "string",
    "linehaul_revenue": "string",
    "pickup_location_id": "string",
    "delivery_location_id": "string",
    "active": True,
    "associated_trip_ids": "string",
    "pickup_departure_actual_date_time": "string",
    "delivery_departure_actual_date_time": "string",
    "run_data_id": "string",
    "timeoff": "string",
    "type": "string",
    "assigned_driver_id": "string",
    "load_weight_on_last_segment": "string",
    "pickup_arrival_eta": "string",
    "pickup_departure_etd": "string",
    "delivery_arrival_eta": "string",
    "delivery_departure_etd": "string",
    "trip_sequence": "string"
}


response_data = request_data.copy()

record_id = 0


def test_create_load():
    response = client.post("/loads/", json=request_data)
    global record_id
    record_id = response.json()["load_data_id"]
    assert response.status_code == 200
    global response_data
    response_data.update({"load_data_id": record_id})
    assert response.json() == response_data


def test_get_loads():
    response = client.get("/loads/")
    assert response.status_code == 200
    assert len(response.json()) >= 1


def test_get_load():
    response = client.get(f"/loads/{record_id}")
    assert response.status_code == 200
    assert response.json() == response_data


def test_get_load_not_found():
    response = client.get(f"/loads/{record_id+1}")
    assert response.status_code == 404
    assert response.json() == {'detail': f'loads {record_id+1} not found'}


updated_load = request_data.copy()
updated_load.update({"load_id": "654321", "active": False})


def test_update_load():
    response = client.put(f"/loads/{record_id}", json=updated_load)
    assert response.status_code == 200
    updated_response_data = response_data.copy()
    updated_response_data.update({"load_id": "654321", "active": False})
    assert response.json() == updated_response_data


def test_update_load_not_found():
    response = client.put(f"/loads/{record_id+1}", json=updated_load)
    assert response.status_code == 404
    assert response.json() == {'detail': f'loads {record_id+1} not found'}


def test_delete_load():
    response = client.delete(f"/loads/{record_id}")
    assert response.status_code == 200
    assert response.json() == "Delete successfully"


def test_delete_load_not_found():
    response = client.delete(f"/loads/{record_id}")
    assert response.status_code == 404
    assert response.json() == {'detail': f'loads {record_id} not found'}
