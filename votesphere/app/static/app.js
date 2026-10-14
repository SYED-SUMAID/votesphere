const question = document.getElementById("question");
const optionsContainer = document.getElementById("options");
const form = document.getElementById("voting-form");
const voteButton = document.getElementById("vote-button");
const message = document.getElementById("message");
const resultsContainer = document.getElementById("results");

let currentPoll = null;
let hasVoted = false;


async function loadPoll() {
    try {
        const response = await fetch("/api/polls");

        if (!response.ok) {
            throw new Error("Unable to load polls");
        }

        const polls = await response.json();

        if (polls.length === 0) {
            question.textContent = "No polls available.";
            voteButton.disabled = true;
            return;
        }

        currentPoll = polls[0];

        question.textContent = currentPoll.question;
        optionsContainer.replaceChildren();

       currentPoll.options.forEach(option => {
    const label = document.createElement("label");
    label.className = "option";

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.name = "option";
    checkbox.value = option.id;

    label.append(checkbox);
    label.append(document.createTextNode(option.text));

    optionsContainer.appendChild(label);
});
        renderResults(currentPoll.options);

    } catch (error) {
        question.textContent = "Unable to load the poll.";
        message.textContent = error.message;
    }
}


function renderResults(options) {
    resultsContainer.replaceChildren();

    const totalVotes = options.reduce(
        (total, option) => total + option.votes,
        0
    );

    options.forEach(option => {
        const percentage = totalVotes
            ? (option.votes / totalVotes) * 100
            : 0;

        const result = document.createElement("div");
        result.className = "result";

        const label = document.createElement("div");
        label.className = "result-label";

        const name = document.createElement("span");
        name.textContent = option.text;

        const count = document.createElement("span");
        count.textContent =
            `${option.votes} votes (${percentage.toFixed(1)}%)`;

        const progress = document.createElement("div");
        progress.className = "progress";

        const bar = document.createElement("div");
        bar.className = "progress-bar";
        bar.style.width = `${percentage}%`;

        progress.appendChild(bar);
        label.append(name, count);
        result.append(label, progress);

        resultsContainer.appendChild(result);
    });
}


form.addEventListener("submit", async event => {
    event.preventDefault();

    if (!currentPoll || hasVoted) {
        return;
    }

    const selected = document.querySelector(
        'input[name="option"]:checked'
    );

    if (!selected) {
        message.textContent = "Please select an option.";
        return;
    }

    voteButton.disabled = true;
    message.textContent = "Submitting your vote...";

    try {
        const response = await fetch(
            `/api/polls/${currentPoll.id}/vote/${selected.value}`,
            {
                method: "POST",
                headers: {
                    "Accept": "application/json"
                }
            }
        );

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Voting failed");
        }

        hasVoted = true;
        message.textContent = data.message;

        await loadPoll();

        optionsContainer.querySelectorAll("input").forEach(input => {
            input.disabled = true;
        });

        voteButton.textContent = "Vote Submitted";

    } catch (error) {
        message.textContent = error.message;
        voteButton.disabled = false;
    }
});


loadPoll();