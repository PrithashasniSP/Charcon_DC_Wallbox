CAN_Signals = {
	"targetContactorsStatus": None,
	"evConnectionState": None,
	"chargingState": None,
	"targetVoltage": None,
	"targetCurrent": None,
	"batteryStateOfCharge": None,
	"cableCheckVoltage": None,
	"vehicleId": None,
	"chargeMode": None,
	"evMinPower": None,
	"evMinCurrent": None,
	"evMinVoltage": None,
	"evMaxCurent": None,
	"evMaxPower": None,
	"evMaxVoltage": None,
	"chargingProfileMaxPowerLimit": None,
	"timeToFullSoc": None,
	"CHRGR_iAcAct": None,
	"CHRGR_iAcAct2": None,
	"CHRGR_iAcAct3": None,
	"CHRGR_uAcActPha1": None,
	"CHRGR_uAcActPha2": None,
	"CHRGR_uAcActPha3": None,
	"CHRGR_iDcAct": None,
	"CHRGR_stOperAct": None,
	"CHRGR_uDcAct": None,
	"CHRGR_stErr": None,
	"CHRGR_stHvIntlck": None,
	"DC1_bReqMIL": None,
	"DC1_stT30c": None,
	"DC1_Temp": None,
	"mc_VCU_OBCControl": None,
	"VCU_OBCMode_Cmd": None,
	"VCU_uDcReqChrgr": None,
	"VCU_iDcLimChrgr": None,
	"VCU_iAcMaxAllwdChrgr": None,
	"CRC_VCU_OBCControl": None,
	"CrashDetect": None,
	"CrashConfirmed_Sts": None,
	"mc_ACU_Crash": None,
	"CRC_VCU_OBCControl": None,
	"NWM_WkUp_BCU_Rx": None,
	"NWM_WkUp_BCU_Reason": None,
	"NWM_WkUp_BCU_NodeAddress": None,
	"NWM_Sleep_BCU_Req": None,
	"mc_VCU_DCDCControl": None,
	"VCU_VoltageDemandHV": None,
	"VCU_CurrentLimitHV": None,
	"VCU_CurrentLimitLV": None,
	"VCU_VoltageDemandLV": None,
	"VCU_DCDCMode_Cmd": None,
	"VCU_stHvDeactvnDC": None,
	"CRC_VCU_DCDCControl": None,
	"mc_VCU_SysControl": None,
	"KL15_VCU_Sts": None,
	"HV_HVIL_Sts": None,
	"CRC_VCU_SysControl": None,
	"limitVoltageMin": None,
	"limitVoltageMax": None,
	"limitPowerMax": None,
	"limitPowerMin": None,
	"limitCurrentMin": None,
	"limitCurrentMax": None,
	"contactorsStatus": None,
	"operationalStatus": None,
	"isolationStatus": None,
	"drivenVoltage": None,
	"drivenCurrent": None,
	"temperature": None,
	"measuredVoltage": None,
	"measuredCurrent": None,
}


HMI_Signals = {
    "HealthIcon": None,
    "SolarEnergy": None,
    "GridEnergy": None,
    "ySolarPwr": None,
    "yGridPwr": None,
    "xTime": None,
    "TotCost": None,
    "PauseTimer": None,
    "StopEventAck": None,
    "ChargingState": None,
    "CostPerKwh": None,
    "MaxGridCurrent": None,
    "SolarPanelArea": None,
    "StopEvent": None,
    }
    
OCPP_Signals = {
    "Voltage": 0,
    "Current": 0,
}
    
IMD_ip = None
Contractor_op = 0 #{0: open, 1: Closed}

CntrCharConFrameRecv = 0
CntrVseccFrameRecv = 0

MaxOutPwr = None

StopChargingEv = False
StopChargingHMI = False

EnergyTransferActive = False
