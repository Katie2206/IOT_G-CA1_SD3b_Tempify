let aliveSecond = 0;
let heartBeatRate = 1000;
let pubnub;
let appChannel = "Tempify-Channel";
let ttl = 60;

function refreshToken()
{
    console.log("Get plant token request");
    sendEvent('get_plant_token');
    let refresh_time = (ttl-1)*60*1000;
    console.log(refresh_time);
    setTimeout('refreshToken()', refresh_time);
}

function get_temp(){
    
}

function time()
{
    let d = new Date();
    let currentSecond = d.getTime();
    if(currentSecond - aliveSecond > heartBeatRate + 1000)
    {
        // document.getElementById("connection_id").innerHTML="DEAD";
        console.log("DEAD")
    }
    else
    {
        // document.getElementById("connection_id").innerHTML="ALIVE";
        console.log("ALIVE")
    }
    setTimeout('time()', 1000);
}

function keepAlive()
{
    fetch('/keep_alive')
    .then(response=>{
        if(response.ok){
            let date = new Date();
            aliveSecond = date.getTime();
	    return response.json();
        }
        throw new Error('Server offline');
    })
    .catch(error=>console.log(error));
    setTimeout('keepAlive()', heartBeatRate);
}


const setupPubNub = () => {
    pubnub = new PubNub({
        publishKey: 'pub-c-ad694749-9bad-47ee-8f11-c0c31bd34e98',
        subscribeKey: 'sub-c-e9f75f41-3ccb-4ac1-826b-f1b00bef42d5',
        userId: 'testUser12'
    });
    console.log("Checking PubNub:   ", pubnub)
    
    const channel = pubnub.channel(appChannel);
    
    const subscription = channel.subscription();
    
    pubnub.addListener({
        status: (s) =>{
            console.log("Status", s.category);
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
    temp = message.temperature_value;
    soil = message.soil_value;
    humidity = message.humidity_value;

    if(soil == 'LOW')
    {   
       document.getElementById("soil_sensor").innerHTML = "LOW";
    }
    if(soil == 'HIGH')
    {
        document.getElementById("soil_sensor").innerHTML = "HIGH";
    }
    if(humidity > 0 || humidity < 100)
    {
        document.getElementById("humidity").innerHTML = humidity;
    }
    if(humidity < 0 || humidity > 100)
    {
        document.getElementById("humidity").innerHTML = "ERROR";
    }
    if(temp > 0 || temp < 100)
    {
        document.getElementById("temp").innerHTML = temp;
    }
    if(temp < 0 || temp > 100)
    {
        document.getElementById("temp").innerHTML = "ERROR";
    }

    // TRYING TO PASS LIVE DATA TO DATABASE
    // fetch('/pubnub_data',
    //     {method: "POST",
    //         body: JSON.stringify({
    //             temperature: temp,
    //             humidity: humidity,
    //             soil: soil
    //         })
    //     })
    //     .then(response=>response.json())
    //     .catch(error=>console.log(error));

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

function subscribe(){
    console.log("Trying to sub with token")
    const channel = pubnub.channel(appChannel)
    const subscription = channel.subscription();
    subscription.subscribe();
}