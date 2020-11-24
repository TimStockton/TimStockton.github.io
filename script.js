/* prevent the form from being submitted, allows build() to change values without an immediate reset */
document.getElementById("submit").addEventListener("click", function(event){
  event.preventDefault()
});
/* takes the user input from the builder form and outputs an NPC */
function build() {
  /* NAME */
  var npcNameOutput = document.getElementById("npcName").value;
  document.getElementById("npcNameOutput").innerHTML = "Name: " + npcNameOutput;
  /* AGE */
  var npcAgeOutput = document.getElementById("npcAge").value;
  document.getElementById("npcAgeOutput").innerHTML = "Age: " + npcAgeOutput;
  /* HEIGHT */
  var npcHeightOutput = document.getElementById("npcHeight").value;
  document.getElementById("npcHeightOutput").innerHTML = "Height: " + npcHeightOutput;
  /* WEIGHT */
  var npcWeightOutput = document.getElementById("npcWeight").value;
  document.getElementById("npcWeightOutput").innerHTML = "Weight: " + npcWeightOutput;
  /* SEX */
  var npcSexOutput = document.getElementById("sex-dropdown").value;
  document.getElementById("npcSexOutput").innerHTML = "Sex: " + npcSexOutput;
  /* RACE */
  var npcRaceOutput = document.getElementById("race-dropdown").value;
  document.getElementById("npcRaceOutput").innerHTML = "Race: " + npcRaceOutput;
  /* CLASS */
  var npcClassOutput = document.getElementById("class-dropdown").value;
  document.getElementById("npcClassOutput").innerHTML = "Class: " + npcClassOutput;
  /* ABILITY SCORES */
  var npcAbilityScoresOutput = [0,0,0,0,0,0];
  npcAbilityScoresOutput[0] = document.getElementById("npcStrength").value;
  npcAbilityScoresOutput[1] = document.getElementById("npcDexterity").value;
  npcAbilityScoresOutput[2] = document.getElementById("npcConstitution").value;
  npcAbilityScoresOutput[3] = document.getElementById("npcIntelligence").value;
  npcAbilityScoresOutput[4] = document.getElementById("npcWisdom").value;
  npcAbilityScoresOutput[5] = document.getElementById("npcCharisma").value;
  document.getElementById("npcAbilityScoresOutput").innerHTML = "Ability Scores: " +
  "STR[" + npcAbilityScoresOutput[0] + "] " + "DEX[" + npcAbilityScoresOutput[1] + "] " +
  "CON[" + npcAbilityScoresOutput[2] + "] " + "INT[" + npcAbilityScoresOutput[3] + "] " +
  "WIS[" + npcAbilityScoresOutput[4] + "] " + "CHA[" + npcAbilityScoresOutput[5] + "]";
  /* ALIGNMENT -fix- */
  var npcAlignmentOutput = document.getElementById("npcAlignment").value;
  document.getElementById("npcAlignmentOutput").innerHTML = "Alignment: " + npcAlignmentOutput;
  /* ADDITIONAL NOTES -fix- */
  var npcNotesOutput = document.getElementById("npcNotes").value;
  document.getElementById("npcNotesOutput").innerHTML = "Notes: " + npcNotesOutput;
}
/* EXPORT NPC TO NEW FILE -fix- */
function download(text, name, type) {
  var a = document.getElementById("a");
  var file = new Blob([text], {type: type});
  a.href = URL.createObjectURL(file);
  a.download = name;
}

/* var saveData = (function () {
var a = document.createElement("a");
document.body.appendChild(a);
a.style = "display: none";
return function (data, fileName) {
    var json = JSON.stringify(data),
        blob = new Blob([json], {type: "octet/stream"}),
        url = window.URL.createObjectURL(blob);
    a.href = url;
    a.download = fileName;
    a.click();
    window.URL.revokeObjectURL(url);
};
}());

var data = { x: 42, s: "hello, world", d: new Date() },
    fileName = "my-download.json";

saveData(data, fileName); ANOTHER POSSIBLE WAY TO EXPORT NPC TO FILE */
