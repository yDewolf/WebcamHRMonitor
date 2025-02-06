// import { get_percent, lerp_color } from "utils.js";

let bpm_label = document.getElementById("BpmLabel")
let heart_img = document.getElementById("HeartImg")
let current_bpm = 0.0

// Min Bpm for lerping between text colors (white to red)
const MIN_BPM = 72.0
const MAX_BPM = 140.0
// Threshold to activate the shake animation
const SHAKE_THRESHOLD = 100.0

// Connect to the websocket server and handle bpm updates
var ws = new WebSocket("ws://localhost:8765/");

ws.onopen = function(){
    console.log("Connection is Established");
};

ws.addEventListener("message", ({ data }) => {
    const event = JSON.parse(data);
    console.log(event)
    switch (event.type) {
        case "bpm_update":
            current_bpm = Math.floor(Number(event.value))
            update_bpm()
            // console.log(current_bpm)
            break;
    }
});

function update_bpm() {
    bpm_label.innerText = current_bpm.toString();
    bpm_label.style.color = lerp_color('#FFFFFF', '#de1010', Math.max(get_percent(MIN_BPM, MAX_BPM, current_bpm), 0.0))
    if (current_bpm > SHAKE_THRESHOLD) {
        bpm_label.style.animationName = "shake"
    } else {
        bpm_label.style.animationName = ""
    }

    heart_img.style.animationDuration = 60 / current_bpm + "s";
}