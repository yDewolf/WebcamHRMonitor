// import { get_percent, lerp_color } from "utils.js";

const bpmRequest = new Request("/get_current_hr")

let bpm_label = document.getElementById("BpmLabel")
let heart_img = document.getElementById("HeartImg")
let current_bpm = 0.0

// Min Bpm for lerping between text colors (white to red)
const MIN_BPM = 72.0
const MAX_BPM = 140.0
// Threshold to activate the shake animation
const SHAKE_THRESHOLD = 100.0

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
setInterval(function(){
    fetch(bpmRequest)
        .then((response) => response.json())
        .then((data) => {
            current_bpm = data.bpm
        });

    update_bpm()
}, 1000);