let salesChart = null;

function setQuestion(question) {
    document.getElementById("question").value = question;
}

async function askQuestion() {
    const question = document.getElementById("question").value.trim();
    const status = document.getElementById("status");
    const answer = document.getElementById("answer");
    const button = document.getElementById("askButton");

    if (!question) {
        status.textContent = "Please enter a question.";
        return;
    }

    button.disabled = true;
    status.textContent = "AI is analyzing your question...";
    answer.textContent = "";

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ question })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Request failed");
        }

        status.textContent = "Analysis completed";

        // Display AI-generated explanation
       const explanation = data.explanation || "No explanation available.";
       const formattedHTML = marked.parse(explanation);
       answer.innerHTML = DOMPurify.sanitize(formattedHTML);

        // Generate chart from actual database results
        if (data.analysis && data.analysis.length > 0) {
            const result = data.analysis[0].result;

            if (Array.isArray(result) && result.length > 0) {
                const labels = result.map(item => item.label);
                const values = result.map(item => item.value);

                drawChart(labels, values);
            } else if (typeof result === "number") {
                drawChart(["Result"], [result]);
            } else {
                clearChart();
            }
        } else {
            clearChart();
        }

    } catch (error) {
        status.textContent = "Error: " + error.message;
        clearChart();

    } finally {
        button.disabled = false;
    }
}

function drawChart(labels, values) {
    const ctx = document.getElementById("salesChart");

    if (salesChart) {
        salesChart.destroy();
    }

    salesChart = new Chart(ctx, {
        type: "bar",
        data: {
            labels: labels,
            datasets: [{
                label: "Revenue (₹)",
                data: values,
                backgroundColor: "#5279c7"
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

function clearChart() {
    if (salesChart) {
        salesChart.destroy();
        salesChart = null;
    }
}