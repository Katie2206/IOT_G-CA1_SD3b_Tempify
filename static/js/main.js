let aliveSecond = 0;
let heartBeatRate = 1000;
let pubnub;
let appChannel = "Tempify-Channel";
let ttl = 60;

function refreshToken()
{
    console.log("Get user token request");
    sendEvent('get_user_token');
    let refresh_time = (ttl-1)*60*1000;
    console.log(refresh_time);
    setTimeout('refreshToken()', refresh_time);
}

function time()
{
    let d = new Date();
    let currentSecond = d.getTime();
    if(currentSecond - aliveSecond > heartBeatRate + 1000)
    {
        document.getElementById("connection_id").innerHTML="DEAD";
    }
    else
    {
        document.getElementById("connection_id").innerHTML="ALIVE";
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

function handleClick(cb)
{
    if(cb.checked)
    {
        value="on";
    }
    else
    {
        value = "off";
    }
    publishMessage({"buzzer":value});
}

const setupPubNub = () => {
    pubnub = new PubNub({
        publishKey: 'PUBNUB_PUBLISH_KEY',
        subscribeKey: 'PUBNUB_SUBSCRIBE_KEY',
        userId: 'your_id',
    });
    
    const channel = pubnub.channel(appChannel);
    
    const subscription = channel.subscription();
    
    pubnub.addListener({
        status: (s) =>{
            console.log("Status", s.category);
        },
    });

    subscription.onMessage = (messageEvent) => {
        handleMessage(messageEvent.message);
    };

    subscription.subscribe();
};

function handleMessage(message)
{
    if(message == '"Motion":"Yes"')
    {
        document.getElementById("motion_id").innerHTML = "Yes";
    }
    if(message == '"Motion":"No"')
    {
        document.getElementById("motion_id").innerHTML = "No";
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

function grantAccess(ab)
{
    var userId = ab.id.split("-")[2];
    var readState = document.getElementById("read-user-"+userId).checked;
    var writeState = document.getElementById("write-user-"+userId).checked;
    sendEvent("grant-"+userId+"-"+readState+"-"+writeState);
}

function sendEvent(value)
{
    fetch(value,
        {
            method:"POST",
        })
        .then(response => response.json())
        .then(responseJson =>{
            console.log(responseJson);
            if(responseJson.hasOwnProperty('token'))
            {
                pubnub.setToken(responseJson.token);
                pubnub.setUUID(responseJson.uuid);
                subscribe();
            }
        });
}

function subscribe(){
    console.log("Trying to sub with token")
    const channel = pubnub.channel(appChannel)
    const subscription = channel.subscription();
    subscription.subscribe();
}