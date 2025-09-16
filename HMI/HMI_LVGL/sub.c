#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "MQTTClient.h"
#include "stdint.h"
#include "sub.h"
#include <unistd.h>
#include <syslog.h>

#include <time.h>

#define MAX_LOG_SIZE 5 * 1024 * 1024 // 5MB

#define ADDRESS "localhost:1883"
#define CLIENTID "ExampleClientSub"
#define TOPIC "DCWallbox/HMI/PageName/#"
#define QOS 1

const char *logFilePath = "mqtt_log.txt";
// #define TIMEOUT     100L

// PageNumber constants
const int CONST_BootPage = 0;
const int CONST_DeviceFailure = 1;
const int CONST_HealthCheck = 2;
const int CONST_ChargingInitPage = 3;
const int CONST_ChargingProgressPage = 4;
const int CONST_MissingConfig = 5;
const int CONST_ReadyToCharge = 6;

int Page;
int HealthIcon;
int PlugStatus; 
int CloudConnection;
int CableCheckStatus;
int PowerBoardStatus;
int HeartBeatMsg;
float SolarEnergy = 0;
float GridEnergy = 0;
float ySolarPwr;
float yGridPwr;
int xTime;
float TotCost = 0;
int PauseTimer;
int StopEventAck;
int ChargingState = -1;
int StopEvent;
char *arr_split[20];
 
volatile MQTTClient_deliveryToken deliveredtoken;

int currentLogSize = 0;
FILE *logFile = NULL;

void delivered(void *context, MQTTClient_deliveryToken dt)
{
    printf("Message with token value %d delivery confirmed\n", dt);
    deliveredtoken = dt;
}


/*
For spltting mqtt messages to tokens and then updatIng the global variables
for this we take topicname as reference and then based on that we split the data
*/
void processString(char *inputString, char *topicName)
{

    char modifiedString[100];  // Assuming a maximum length for the modified string    
    strcpy(modifiedString, inputString);

    // Tokenize the modified string    
 
    if(strncmp(topicName,"DCWallbox/HMI/PageName/AllPage",100)==0 ){

    // Replace ":" with space in the modified string    
    for (int i = 0; i < strlen(modifiedString); i++) {

        if (modifiedString[i] == ':') {

            modifiedString[i] = ' ';

        }    
        }

    char *token = strtok(modifiedString, " ");
    int i = 0;
    while (token != NULL) {
        arr_split[i]= token;
        i++;
        token = strtok(NULL, " "); // Get the next token
    }
            HealthIcon = atoi(arr_split[0]);
            PlugStatus = atoi(arr_split[1]);
            CloudConnection = atoi(arr_split[2]);
            
            // printf("health icon %d\n",HealthIcon);
            // printf("PlugStatus %d\n",PlugStatus);
            // printf("CloudConnection %d\n",CloudConnection);  
            
        
    }

    if(strncmp(topicName,"DCWallbox/HMI/PageName/ChargingProgressPage",100)==0 ){
    for (int i = 0; i < strlen(modifiedString); i++) {

        if (modifiedString[i] == ':') {

            modifiedString[i] = ' ';

        }    
        }

    char *token = strtok(modifiedString, " ");
    int i = 0;
    while (token != NULL) {
        arr_split[i]= token;
        i++;
        token = strtok(NULL, " "); // Get the next token
    }
            SolarEnergy = atof(arr_split[0]);
            GridEnergy = atof(arr_split[1]);
            ySolarPwr = atof(arr_split[2]);
            yGridPwr = atof(arr_split[3]);
            xTime = atof(arr_split[4]);
            TotCost = atof(arr_split[5]);
            PauseTimer = atoi(arr_split[6]);
            StopEventAck = atoi(arr_split[7]);
            ChargingState = atoi(arr_split[8]);
            
            Page = CONST_ChargingProgressPage;

            // printf("Page %d\n", Page);
            // printf("SolarEnergy %f\n",SolarEnergy);
            // printf("GridEnergy %f\n",GridEnergy);
            // printf("ySolarPwr %f\n",ySolarPwr);  
            // printf("yGridPwr %f\n",yGridPwr);
            // printf("xTime %d\n",xTime);
            // printf("TotCost %f\n",TotCost);
            // printf("TimeHr %d\n",PauseTimer);
            // printf("StopEventAck %d\n",StopEventAck);
            // printf("ChargingState %d\n",ChargingState);       
    }
    if(strncmp(topicName,"DCWallbox/HMI/PageName/HealthCheck",100)==0 ){
        
    // Replace ":" with space in the modified string    
    for (int i = 0; i < strlen(modifiedString); i++) {

        if (modifiedString[i] == ':') {

            modifiedString[i] = ' ';

        }    
        }

    char *token = strtok(modifiedString, " ");
    int i = 0;
    while (token != NULL) {
        arr_split[i]= token;
        i++;
        token = strtok(NULL, " "); // Get the next token
    }
            CableCheckStatus = atoi(arr_split[0]);
            PowerBoardStatus = atoi(arr_split[1]);
            HeartBeatMsg = atoi(arr_split[2]);
            Page = CONST_HealthCheck;

            printf("Page %d\n", Page);
        
    }

    if(strncmp(topicName,"DCWallbox/HMI/PageName/BootPage",100)==0 ){
        Page = CONST_BootPage;
        printf("Page %d\n", Page);
    }
    if(strncmp(topicName,"DCWallbox/HMI/PageName/DeviceFailure",100)==0 ){
        Page = CONST_DeviceFailure;
        printf("Page %d\n", Page);
    }
     if(strncmp(topicName,"DCWallbox/HMI/PageName/MissingConfig",100)==0 ){
        Page = CONST_MissingConfig;
        printf("Page %d\n", Page);
    }
    if(strncmp(topicName,"DCWallbox/HMI/PageName/ReadyToCharge",100)==0 ){
        Page = CONST_ReadyToCharge;
        printf("Page %d\n", Page);
    }
    if(strncmp(topicName,"DCWallbox/HMI/PageName/ChargingInitPage",100)==0 ){
        Page = CONST_ChargingInitPage;
        printf("Page %d\n", Page);
    }

        
}

 
int msgarrvd(void *context, char *topicName, int topicLen, MQTTClient_message *message)
{
    if (logFile == NULL || currentLogSize >= MAX_LOG_SIZE)
    {
        if (logFile)
        {
            fclose(logFile);
            logFile = NULL;
        }
        time_t current_time;
        struct tm *time_info;
        char filename[30]; // Adjust the buffer size as needed

        time(&current_time);
        time_info = localtime(&current_time);
        strftime(filename, sizeof(filename), "/home/mqtt_log.txt", time_info);

        logFile = fopen(filename, "a");
        if (logFile)
        {
            fseek(logFile, 0, SEEK_END);
            currentLogSize = ftell(logFile);
        }
    }

    if (logFile)
    {
        // Get the current date and time
        time_t current_time;
        struct tm *time_info;
        char time_string[20]; // Adjust the buffer size as needed

        time(&current_time);
        time_info = localtime(&current_time);
        strftime(time_string, sizeof(time_string), "%Y-%m-%d %H:%M:%S", time_info);

        // Write the date, time, topic, and message to the log file
        fprintf(logFile, "%s", time_string);
        fprintf(logFile, " Topic: %s", topicName);
        fprintf(logFile, " Message: %.*s\n", message->payloadlen, (char *)message->payload);
        // fprintf(logFile, "--------------------------------------------------------------------------------\n");
        fflush(logFile);
        currentLogSize = ftell(logFile);
    }

    
    processString((char*)message->payload,(char*)topicName);

   
    
    //printf("   message: %.*s\n", message->payloadlen, (char*)message->payload);
    

    MQTTClient_freeMessage(&message);
    MQTTClient_free(topicName);
    return 1;
}
 
void connlost(void *context, char *cause)
{
    printf("\nConnection lost\n");
    printf("     cause: %s\n", cause);
}
 
int mqtt_init()
{
    MQTTClient client;
    MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;
    int rc;
 
    if ((rc = MQTTClient_create(&client, ADDRESS, CLIENTID,
        MQTTCLIENT_PERSISTENCE_NONE, NULL)) != MQTTCLIENT_SUCCESS)
    {
        printf("Failed to create client, return code %d\n", rc);
        rc = EXIT_FAILURE;
        goto exit;
    }
 
    if ((rc = MQTTClient_setCallbacks(client, NULL, connlost, msgarrvd, delivered)) != MQTTCLIENT_SUCCESS)
    {
        printf("Failed to set callbacks, return code %d\n", rc);
        rc = EXIT_FAILURE;
        goto destroy_exit;
    }
 
    conn_opts.keepAliveInterval = 20;
    conn_opts.cleansession = 1;
    if ((rc = MQTTClient_connect(client, &conn_opts)) != MQTTCLIENT_SUCCESS)
    {
        printf("Failed to connect, return code %d\n", rc);
        rc = EXIT_FAILURE;
        goto destroy_exit;
    }
 
    printf("Subscribing to topic %s\nfor client %s using QoS%d\n\n"
           "Press Q<Enter> to quit\n\n", TOPIC, CLIENTID, QOS);
    if ((rc = MQTTClient_subscribe(client, TOPIC, QOS)) != MQTTCLIENT_SUCCESS)
    {
        printf("Failed to subscribe, return code %d\n", rc);
        rc = EXIT_FAILURE;
    }
    else
    {
        int ch;
        do
        {
                ch = getchar();
        } while (ch!='Q' && ch != 'q');
 
        if ((rc = MQTTClient_unsubscribe(client, TOPIC)) != MQTTCLIENT_SUCCESS)
        {
                printf("Failed to unsubscribe, return code %d\n", rc);
                rc = EXIT_FAILURE;
        }
    }
 
    if ((rc = MQTTClient_disconnect(client, 10000)) != MQTTCLIENT_SUCCESS)
    {
        printf("Failed to disconnect, return code %d\n", rc);
        rc = EXIT_FAILURE;
    }
destroy_exit:
    // MQTTClient_destroy(&client);
exit:
    return rc;
}