async function space_text(){
    let corrupted_text = document.getElementById('userInput').value;
    const response = await fetch('/api/data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ corrupted_text: corrupted_text })
    });
    
    const data = await response.json();
    let result = document.getElementById('outputText');
    result.value = data.spaced_text;
}
    
let btn = document.getElementById('generateButton').addEventListener('click', space_text);

document.getElementById("aboutButton").addEventListener("click", () => {
    const aboutText = `S pacege nis ana cad emicpro jec t d e       vel oped b y As af De lme di g o an d R omi Zar chid uri ng the irgrad uates tudiesin N eu ro sc ience  and  D ata Sci ence. I t d emons trat es the use of a Long Short-Term Memory arti ficial ne ural net work for the au toma tic det ection an d corre ction of miss ing and mis placed sp aces i n t ext.`;
    document.getElementById("userInput").value = aboutText;
}); s