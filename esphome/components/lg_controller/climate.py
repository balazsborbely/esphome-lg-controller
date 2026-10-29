import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import binary_sensor, climate, number, select, sensor, switch, text_sensor, uart
from esphome.const import (
    CONF_ID,
    CONF_RX_PIN,
    CONF_INTERNAL,
    DEVICE_CLASS_DURATION,
    DEVICE_CLASS_ENERGY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_TEMPERATURE,
    STATE_CLASS_MEASUREMENT,
    STATE_CLASS_TOTAL_INCREASING,
    UNIT_CELSIUS,
    UNIT_HOUR,
    UNIT_KILOWATT,
    UNIT_KILOWATT_HOURS,
    UNIT_PERCENT,
)

CODEOWNERS = ["JanM321"]
DEPENDENCIES = ["uart"]
AUTO_LOAD = ["binary_sensor", "number", "switch", "sensor", "select", "text_sensor"]

lg_controller_ns = cg.esphome_ns.namespace("lg_controller")
LgController = lg_controller_ns.class_(
    "LgController", cg.Component, uart.UARTDevice, climate.Climate
)
LgNumber = lg_controller_ns.class_("LgNumber", number.Number, cg.Component)
LgSelect = lg_controller_ns.class_("LgSelect", select.Select, cg.Component)
LgSwitch = lg_controller_ns.class_("LgSwitch", switch.Switch, cg.Component)

CONF_FAHRENHEIT = "fahrenheit"
CONF_IS_SLAVE_CONTROLLER = "is_slave_controller"
CONF_TARGET_TEMPERATURE_STEP = "target_temperature_step"
CONF_OVERCOOLING_SETTING = "overcooling_setting"

CONF_TEMPERATURE_SENSOR = "temperature_sensor"

CONF_VANE1 = "vane1"
CONF_VANE2 = "vane2"
CONF_VANE3 = "vane3"
CONF_VANE4 = "vane4"
CONF_OVERHEATING = "overheating"

CONF_FAN_SPEED_SLOW = "fan_speed_slow"
CONF_FAN_SPEED_LOW = "fan_speed_low"
CONF_FAN_SPEED_MEDIUM = "fan_speed_medium"
CONF_FAN_SPEED_HIGH = "fan_speed_high"
CONF_SLEEP_TIMER = "sleep_timer"

CONF_ERROR_CODE = "error_code"
CONF_PIPE_TEMP_IN = "pipe_temp_in"
CONF_PIPE_TEMP_MID = "pipe_temp_mid"
CONF_PIPE_TEMP_OUT = "pipe_temp_out"
CONF_POWER_CONSUMPTION = "power_consumption"
CONF_CURRENT_POWER = "current_power"
CONF_HUMIDITY = "humidity"
CONF_FAN_OPERATION_TIME = "fan_operation_time"
CONF_INDOOR_UNIT_OPERATION_TIME = "indoor_unit_operation_time"
CONF_PRECISE_ROOM_TEMPERATURE = "precise_room_temperature"
CONF_OVERCOOLING = "overcooling"
CONF_COOLING_THERMAL_OFF_FAN = "cooling_thermal_off_fan"
CONF_TEMPERATURE_CONTROL_STEP = "temperature_control_step"
CONF_STATIC_PRESSURE_STEP = "static_pressure_step"
CONF_CONTINUOUS_FAN = "continuous_fan"
CONF_TEMPERATURE_BASED_FAN_AUTO = "temperature_based_fan_auto"
CONF_ADVANCED_SETTINGS_RAW = "advanced_settings_raw"
CONF_EXTENDED_SETTINGS_RAW = "extended_settings_raw"

CONF_DEFROST = "defrost"
CONF_PREHEAT = "preheat"
CONF_OUTDOOR = "outdoor"
CONF_AUTO_DRY_ACTIVE = "auto_dry_active"

CONF_PURIFIER = "purifier"
CONF_INTERNAL_THERMISTOR = "internal_thermistor"
CONF_AUTO_DRY = "auto_dry"

VANE_OPTIONS = ["0 (Default)", "1 (Up)", "2", "3", "4", "5", "6 (Down)"]
OVERHEATING_OPTIONS = ["0 (Default)", "1 (+4C/+6C)", "2 (+2C/+4C)", "3 (-1C/+1C)", "4 (-0.5C/+0.5C)"]
OVERCOOLING_OPTIONS = ["0 (Default: +0.5C/-0.5C)", "1 (+6C/+4C)", "2 (+4C/+2C)", "3 (+1C/-1C)"]
TEMPERATURE_CONTROL_STEP_OPTIONS = ["0 (1C)", "1 (0.5C)"]
COOLING_THERMAL_OFF_FAN_OPTIONS = ["0 (Fan Low)", "1 (Fan Off)", "2 (Fan Setting)"]

CONFIG_SCHEMA = climate.climate_schema(LgController).extend(
    {
        cv.Required(CONF_RX_PIN): pins.gpio_input_pin_schema,

        cv.Required(CONF_FAHRENHEIT): cv.boolean,
        cv.Required(CONF_IS_SLAVE_CONTROLLER): cv.boolean,
        cv.Optional(CONF_TARGET_TEMPERATURE_STEP, default=0.5): cv.one_of(0.5, 1.0, float=True),
        # Installer setting 27 to write to the unit (0-3). -1 or omitted = echo the unit's value.
        cv.Optional(CONF_OVERCOOLING_SETTING, default=-1): cv.int_range(min=-1, max=3),

        cv.Optional(CONF_TEMPERATURE_SENSOR): cv.use_id(sensor.Sensor),

        cv.Required(CONF_VANE1): select.select_schema(LgSelect),
        cv.Required(CONF_VANE2): select.select_schema(LgSelect),
        cv.Required(CONF_VANE3): select.select_schema(LgSelect),
        cv.Required(CONF_VANE4): select.select_schema(LgSelect),
        cv.Required(CONF_OVERHEATING): select.select_schema(LgSelect),

        cv.Required(CONF_FAN_SPEED_SLOW): number.number_schema(LgNumber),
        cv.Required(CONF_FAN_SPEED_LOW): number.number_schema(LgNumber),
        cv.Required(CONF_FAN_SPEED_MEDIUM): number.number_schema(LgNumber),
        cv.Required(CONF_FAN_SPEED_HIGH): number.number_schema(LgNumber),
        cv.Required(CONF_SLEEP_TIMER): number.number_schema(LgNumber),

        cv.Required(CONF_ERROR_CODE): sensor.sensor_schema(accuracy_decimals=0),
        cv.Required(CONF_PIPE_TEMP_IN): sensor.sensor_schema(),
        cv.Required(CONF_PIPE_TEMP_MID): sensor.sensor_schema(),
        cv.Required(CONF_PIPE_TEMP_OUT): sensor.sensor_schema(),
        cv.Optional(CONF_POWER_CONSUMPTION): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT_HOURS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_ENERGY,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_CURRENT_POWER): sensor.sensor_schema(
            unit_of_measurement=UNIT_KILOWATT,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_POWER,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_HUMIDITY): sensor.sensor_schema(
            unit_of_measurement=UNIT_PERCENT,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_HUMIDITY,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        cv.Optional(CONF_FAN_OPERATION_TIME): sensor.sensor_schema(
            unit_of_measurement=UNIT_HOUR,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_DURATION,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_INDOOR_UNIT_OPERATION_TIME): sensor.sensor_schema(
            unit_of_measurement=UNIT_HOUR,
            accuracy_decimals=0,
            device_class=DEVICE_CLASS_DURATION,
            state_class=STATE_CLASS_TOTAL_INCREASING,
        ),
        cv.Optional(CONF_PRECISE_ROOM_TEMPERATURE): sensor.sensor_schema(
            unit_of_measurement=UNIT_CELSIUS,
            accuracy_decimals=1,
            device_class=DEVICE_CLASS_TEMPERATURE,
            state_class=STATE_CLASS_MEASUREMENT,
        ),
        # Installer setting 27 (overcooling) as select dropdown.
        cv.Optional(CONF_OVERCOOLING): select.select_schema(LgSelect),
        cv.Optional(CONF_COOLING_THERMAL_OFF_FAN): select.select_schema(LgSelect),
        # Installer settings: 17 (0 = 1 °C, 1 = 0.5 °C control), 32 (static pressure
        # step), 46 (continuous fan), 51 (temperature-based fan speed auto).
        cv.Optional(CONF_TEMPERATURE_CONTROL_STEP): select.select_schema(LgSelect),
        cv.Optional(CONF_STATIC_PRESSURE_STEP): sensor.sensor_schema(accuracy_decimals=0),
        cv.Optional(CONF_CONTINUOUS_FAN): switch.switch_schema(LgSwitch),
        cv.Optional(CONF_TEMPERATURE_BASED_FAN_AUTO): switch.switch_schema(LgSwitch),
        # Raw hex of the unit's 0xCD frame and 0xCE.00/10/11/12 sub-frames, which are only
        # partly documented. Published only when they change.
        cv.Optional(CONF_ADVANCED_SETTINGS_RAW): text_sensor.text_sensor_schema(),
        cv.Optional(CONF_EXTENDED_SETTINGS_RAW): text_sensor.text_sensor_schema(),

        cv.Required(CONF_DEFROST): binary_sensor.binary_sensor_schema(),
        cv.Required(CONF_PREHEAT): binary_sensor.binary_sensor_schema(),
        cv.Required(CONF_OUTDOOR): binary_sensor.binary_sensor_schema(),
        cv.Required(CONF_AUTO_DRY_ACTIVE): binary_sensor.binary_sensor_schema(),

        cv.Required(CONF_PURIFIER): switch.switch_schema(LgSwitch),
        cv.Required(CONF_INTERNAL_THERMISTOR): switch.switch_schema(LgSwitch),
        cv.Required(CONF_AUTO_DRY): switch.switch_schema(LgSwitch),
    }
).extend(cv.COMPONENT_SCHEMA).extend(uart.UART_DEVICE_SCHEMA)

async def to_code(config):
    rx_pin = await cg.gpio_pin_expression(config[CONF_RX_PIN])

    if CONF_TEMPERATURE_SENSOR in config:
        temperature_sensor = await cg.get_variable(config[CONF_TEMPERATURE_SENSOR])
    else:
        temperature_sensor = cg.nullptr

    # Hide entities not supported for 'slave' controllers.
    if config[CONF_IS_SLAVE_CONTROLLER]:
        config[CONF_FAN_SPEED_SLOW][CONF_INTERNAL] = True
        config[CONF_FAN_SPEED_LOW][CONF_INTERNAL] = True
        config[CONF_FAN_SPEED_MEDIUM][CONF_INTERNAL] = True
        config[CONF_FAN_SPEED_HIGH][CONF_INTERNAL] = True
        config[CONF_OVERHEATING][CONF_INTERNAL] = True
        config[CONF_INTERNAL_THERMISTOR][CONF_INTERNAL] = True

    vane1 = await select.new_select(config[CONF_VANE1], options=VANE_OPTIONS)
    vane2 = await select.new_select(config[CONF_VANE2], options=VANE_OPTIONS)
    vane3 = await select.new_select(config[CONF_VANE3], options=VANE_OPTIONS)
    vane4 = await select.new_select(config[CONF_VANE4], options=VANE_OPTIONS)
    overheating = await select.new_select(config[CONF_OVERHEATING], options=OVERHEATING_OPTIONS)

    fan_speed_slow = await number.new_number(config[CONF_FAN_SPEED_SLOW], min_value=0, max_value=255, step=1)
    fan_speed_low = await number.new_number(config[CONF_FAN_SPEED_LOW], min_value=0, max_value=255, step=1)
    fan_speed_medium = await number.new_number(config[CONF_FAN_SPEED_MEDIUM], min_value=0, max_value=255, step=1)
    fan_speed_high = await number.new_number(config[CONF_FAN_SPEED_HIGH], min_value=0, max_value=255, step=1)
    sleep_timer = await number.new_number(config[CONF_SLEEP_TIMER], min_value=0, max_value=420, step=1)

    error_code = await sensor.new_sensor(config[CONF_ERROR_CODE])
    pipe_temp_in = await sensor.new_sensor(config[CONF_PIPE_TEMP_IN])
    pipe_temp_mid = await sensor.new_sensor(config[CONF_PIPE_TEMP_MID])
    pipe_temp_out = await sensor.new_sensor(config[CONF_PIPE_TEMP_OUT])
    if CONF_POWER_CONSUMPTION in config:
        power_consumption = await sensor.new_sensor(config[CONF_POWER_CONSUMPTION])
    else:
        power_consumption = cg.nullptr
    if CONF_CURRENT_POWER in config:
        current_power = await sensor.new_sensor(config[CONF_CURRENT_POWER])
    else:
        current_power = cg.nullptr
    if CONF_HUMIDITY in config:
        humidity = await sensor.new_sensor(config[CONF_HUMIDITY])
    else:
        humidity = cg.nullptr
    if CONF_FAN_OPERATION_TIME in config:
        fan_operation_time = await sensor.new_sensor(config[CONF_FAN_OPERATION_TIME])
    else:
        fan_operation_time = cg.nullptr
    if CONF_INDOOR_UNIT_OPERATION_TIME in config:
        indoor_unit_operation_time = await sensor.new_sensor(config[CONF_INDOOR_UNIT_OPERATION_TIME])
    else:
        indoor_unit_operation_time = cg.nullptr
    if CONF_PRECISE_ROOM_TEMPERATURE in config:
        precise_room_temperature = await sensor.new_sensor(config[CONF_PRECISE_ROOM_TEMPERATURE])
    else:
        precise_room_temperature = cg.nullptr
    if CONF_OVERCOOLING in config:
        overcooling = await select.new_select(config[CONF_OVERCOOLING], options=OVERCOOLING_OPTIONS)
    else:
        overcooling = cg.nullptr
    if CONF_COOLING_THERMAL_OFF_FAN in config:
        cooling_thermal_off_fan = await select.new_select(
            config[CONF_COOLING_THERMAL_OFF_FAN], options=COOLING_THERMAL_OFF_FAN_OPTIONS
        )
    else:
        cooling_thermal_off_fan = cg.nullptr

    defrost = await binary_sensor.new_binary_sensor(config[CONF_DEFROST])
    preheat = await binary_sensor.new_binary_sensor(config[CONF_PREHEAT])
    outdoor = await binary_sensor.new_binary_sensor(config[CONF_OUTDOOR])
    auto_dry_active = await binary_sensor.new_binary_sensor(config[CONF_AUTO_DRY_ACTIVE])

    purifier = await switch.new_switch(config[CONF_PURIFIER])
    internal_thermistor = await switch.new_switch(config[CONF_INTERNAL_THERMISTOR])
    auto_dry = await switch.new_switch(config[CONF_AUTO_DRY])

    var = cg.new_Pvariable(config[CONF_ID], rx_pin, temperature_sensor,
                           vane1, vane2, vane3, vane4, overheating,
                           fan_speed_slow, fan_speed_low, fan_speed_medium, fan_speed_high,
                           sleep_timer,
                           error_code, pipe_temp_in, pipe_temp_mid, pipe_temp_out,
                           power_consumption, current_power,
                           humidity, fan_operation_time, indoor_unit_operation_time,
                           precise_room_temperature,
                           overcooling, cooling_thermal_off_fan,
                           defrost, preheat, outdoor, auto_dry_active,
                           purifier, internal_thermistor, auto_dry,
                           config[CONF_FAHRENHEIT], config[CONF_IS_SLAVE_CONTROLLER])
    cg.add(var.set_overcooling_target(config[CONF_OVERCOOLING_SETTING]))
    cg.add(var.set_target_temperature_step(config[CONF_TARGET_TEMPERATURE_STEP]))
    if CONF_TEMPERATURE_CONTROL_STEP in config:
        step_sel = await select.new_select(
            config[CONF_TEMPERATURE_CONTROL_STEP], options=TEMPERATURE_CONTROL_STEP_OPTIONS
        )
        cg.add(var.set_temperature_control_step_select(step_sel))
    if CONF_STATIC_PRESSURE_STEP in config:
        sens = await sensor.new_sensor(config[CONF_STATIC_PRESSURE_STEP])
        cg.add(var.set_static_pressure_step_sensor(sens))
    if CONF_CONTINUOUS_FAN in config:
        cont_fan = await switch.new_switch(config[CONF_CONTINUOUS_FAN])
        cg.add(var.set_continuous_fan_switch(cont_fan))
    if CONF_TEMPERATURE_BASED_FAN_AUTO in config:
        fan_auto = await switch.new_switch(config[CONF_TEMPERATURE_BASED_FAN_AUTO])
        cg.add(var.set_temperature_based_fan_auto_switch(fan_auto))
    for key in (CONF_ADVANCED_SETTINGS_RAW, CONF_EXTENDED_SETTINGS_RAW):
        if key in config:
            sens = await text_sensor.new_text_sensor(config[key])
            cg.add(getattr(var, f"set_{key}_text_sensor")(sens))
    await climate.register_climate(var, config)
    await cg.register_component(var, config)
    await uart.register_uart_device(var, config)
