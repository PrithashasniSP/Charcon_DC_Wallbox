/*

MQTT Subscriber 

*/

extern int Page;
extern int HealthIcon;
extern int PlugStatus; 
extern int CloudConnection;
extern int CableCheckStatus;
extern int PowerBoardStatus;
extern int HeartBeatMsg;
extern float SolarEnergy;
extern float GridEnergy;
extern float ySolarPwr;
extern float yGridPwr;
extern int xTime;
extern float TotCost;
extern int StopEventAck;
extern int ChargingState;
extern int StopEvent;
extern int PauseTimer;
// extern int GSMSignal;
extern char *arr_split[20];
// extern char *Location;

extern const int CONST_BootPage;
extern const int CONST_DeviceFailure;
extern const int CONST_HealthCheck;
extern const int CONST_ChargingInitPage;
extern const int CONST_ChargingProgressPage;
extern const int CONST_MissingConfig;
extern const int CONST_ReadyToCharge;
extern const int CONST_AdminLoginPage;
 

extern int mqtt_init();