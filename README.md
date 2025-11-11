# Minimal DJI Cloud API example for DeepPlants Application

Minimal working example using DJI Cloud API. Adapted for DP application.
## New version modification
1. Using Eclipse Mosquitto: https://mosquitto.org/
2. TMUX implmentation with panel configuration in `start.yaml`

## Setup
1. Open the container `dji-cnt`
2. Run 
```
tmuxp load DJI_Cloud_API_minimal_DP/start.yaml
```

### Connecting the controller

1. Open DJI Pilot App
2. Go to `Cloud Service` -> `Other platforms`
3. Write url `http://HOST_ADDR:5000/login` and connect
4. Press Login.

Expected output:

```
📨Got msg: thing/product/1ZNBK7LC00AB/osd
🌍Status: Lat: 0 Lon: 0 height: 16.160583 att_head 10.4 att_pitch -0.4 att_roll 0.2
{'61-0-0': {'gimbal_pitch': 0,
            'gimbal_roll': 0,
            'gimbal_yaw': 117.8,
            'measure_target_altitude': 0,   
            'measure_target_distance': 4.2,
            'measure_target_error_state': 3,
            'measure_target_latitude': 0,
            'measure_target_longitude': 0,
            'payload_index': '61-0-0',
            'version': 1},
 'elevation': 0,
 'firmware_version': '03.31.0000',
 'gear': 1,
 'home_distance': 0,
 'horizontal_speed': 0,
 'longitude': 0,
 'mode_code': 0,
 'position_state': {'gps_number': 0,
                    'is_fixed': 0,
                    'quality': 0,
                    'rtk_number': 0},
 'storage': {'total': 24434700, 'used': 7723000},
 'total_flight_distance': 0,
 'total_flight_time': 0,
 'track_id': '',
 'vertical_speed': 0,
 'wind_direction': 0,
 'wind_speed': 0}
```