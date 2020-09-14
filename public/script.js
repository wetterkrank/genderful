function printResult(text) {
    let resultsList = document.getElementById('results-list');
    let li = document.createElement('li');
    let code = document.createElement('code');
    let resultText = document.createTextNode(text);
    code.appendChild(resultText);
    li.appendChild(code);
    if (document.getElementById('results').hasAttribute('hidden')) {
        document.getElementById('results').removeAttribute('hidden');
    }
    resultsList.insertBefore(li, resultsList.firstChild);
}

async function submitWord(event) {
    event.preventDefault();
    let word = event.target.elements['predict-input'].value;
    if (word) {
        event.target.elements['predict-input'].value = '';
        document.getElementById('spinner').removeAttribute('hidden');
        word = encodeURIComponent(word)
        let response = await fetch(`/predict?word=${word}`);
        let json = await response.json();
        document.getElementById('spinner').setAttribute('hidden', '');
        // console.log(json);
        if (json['word']) {
            let resultsEntry = `${json['word']}: ${json['gender']} (${json['probability']})`;
            printResult(resultsEntry)
        }
    }
}

function initOnLoad() {
    document.getElementById('predict-form').addEventListener('submit', submitWord);
}

document.addEventListener('DOMContentLoaded', initOnLoad);