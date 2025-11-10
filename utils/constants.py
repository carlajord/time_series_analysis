
TAG = "tag"
PI_NUMBER = "pi_number"

TIMESTAMP = "timestamp"
ON = "on"
MOTOR_POWER = "motor_power"
DISCH_T_1 = "disch_T_1"
DISCH_T_2 = "disch_T_2"
DISCH_P_1 = "disch_P_1"
DISCH_P_2 = "disch_P_2"
SUC_T_1 = "suc_T_1"
SUC_T_2 = "suc_T_2"
SUC_P_1 = "suc_P_1"
SUC_P_2 = "suc_P_2"
MASS_FLOW = "mass_flow"
VOL_FLOW = "vol_flow"
FLOW_1 = "flow_1"
FLOW_2 = "flow_2"
VIB_1_1 = "vib_1_1"
VIB_1_2 = "vib_1_2"
VIB_2_1 = "vib_2_1"
VIB_2_2 = "vib_2_2"


COMPRESSOR_TABLE = "compressor"

ALL_CDF_VARIABLES = {COMPRESSOR_TABLE: [
    ON, MOTOR_POWER, DISCH_T_1, DISCH_T_2, DISCH_P_1, DISCH_P_2,
    SUC_T_1, SUC_T_2, SUC_P_1, SUC_P_2, MASS_FLOW, VOL_FLOW,
    FLOW_1, FLOW_2, VIB_1_1, VIB_1_2, VIB_2_1, VIB_2_2
]}

ERROR = "Error"
SUCCESS = "Success"

GRANULARITY = "2min" # should always be given in minutes
