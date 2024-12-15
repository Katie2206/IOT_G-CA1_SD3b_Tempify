let aliveSecond = 0;
let heartBeatRate = 1000;
let pubnub;
let appChannel = "Tempify-Channel";
let ttl = 60;

const setupPubNub = () => {
    pubnub = new PubNub({
        publishKey: 'pub-c-ad694749-9bad-47ee-8f11-c0c31bd34e98',
        subscribeKey: 'sub-c-e9f75f41-3ccb-4ac1-826b-f1b00bef42d5',
        cryptoModule: PubNub.CryptoModule.aesCbcCryptoModule({cipherKey:'et4y586hd4ty58he'}),
        userId: 'testUser12'
    });
    console.log("Checking PubNub:   ", pubnub)
    
    const channel = pubnub.channel(appChannel);
    
    const subscription = channel.subscription();
    
    pubnub.addListener({
        status: (s) =>{
            console.log("Status", s.category);
            console.log("Message", s.message);
        },
        message: (event) => {
            console.log("Message2", event.message);
            const PI_response = event.message;
            const time_value = PI_response.time_taken;
            const temp_value = PI_response.temperature_value;
            const humidity_value = PI_response.humidity_value;
            const soil_value = PI_response.soil_value;
            console.log("time", time_value, "temp", temp_value, "humidity", humidity_value, "soil" , soil_value)
        }
    });

    subscription.onMessage = (messageEvent) => {
        handleMessage(messageEvent.message);
    };

    console.log("channel:", channel)
    subscription.subscribe();
};

function handleMessage(message)
{
    console.log("message here",message.soil_value)
    if(message.soil_value == 'LOW')
    {
        document.getElementById("soil_sensor").innerHTML = "LOW";
    }
    if(message.soil_value == 'HIGH')
    {
        document.getElementById("soil_sensor").innerHTML = "HIGH";
    }
}

const publishMessage = async(message) => {
    const publishPayload = {
        channel: appChannel,
        message: {
            message:message
        },
    };
    await pubnub.publish(publishPayload);
}

