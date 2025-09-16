#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "MQTTClient.h"
#include "../../sub.h"
#include "pub_mqtt.h"

#define ADDRESS "localhost:1883"
#define CLIENTID "HMI_Stop_Event"
#define TOPIC "DCWallbox/HMI/PageName/ChargingProgressPageStop"
#define QOS 1
#define TIMEOUT 10000L

int pub_main()
{
    MQTTClient client;
    MQTTClient_connectOptions conn_opts = MQTTClient_connectOptions_initializer;
    int rc;

    MQTTClient_create(&client, ADDRESS, CLIENTID, MQTTCLIENT_PERSISTENCE_NONE, NULL);

    conn_opts.keepAliveInterval = 20;
    conn_opts.cleansession = 1;

    if ((rc = MQTTClient_connect(client, &conn_opts)) != MQTTCLIENT_SUCCESS)
    {
        printf("Failed to connect, return code %d\n", rc);
        exit(EXIT_FAILURE);
    }

    char payload[] = "Failure.....";
    MQTTClient_message pubmsg = MQTTClient_message_initializer;
    pubmsg.payload = payload;
    pubmsg.payloadlen = strlen(payload);
    pubmsg.qos = QOS;
    pubmsg.retained = 0;

    MQTTClient_deliveryToken token;
    MQTTClient_publishMessage(client, TOPIC, &pubmsg, &token);

    printf("Waiting for publication of %s\n"
           "on topic %s for client with ClientID: %s\n",
           payload, TOPIC, CLIENTID);

    rc = MQTTClient_waitForCompletion(client, token, TIMEOUT);
    printf("Message with delivery token %d delivered\n", token);

    MQTTClient_disconnect(client, 10000);

    printf("Client Dissconected");
    MQTTClient_destroy(&client);
    return rc;
}
