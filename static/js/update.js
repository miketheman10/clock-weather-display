document.addEventListener("DOMContentLoaded", () => {
    async function fetchData() {
        try {
            const res = await fetch("/api");
            if (!res.ok) throw new Error("failed");
            const data = await res.json();
            if (data.error) throw new Error(data.error);
            updateDOM(data);
        } catch (err) {
            console.error("update failed", err);
        }
    }

    function updateDOM(data) {
        document.getElementById("time").textContent = data.time;
        document.getElementById("tempValue").textContent = data.temperature + "\u00B0F";
        document.getElementById("summary").textContent = data.summary;
        const icon = document.getElementById("weatherIcon");
        icon.src = `/static/icons/${data.icon}.svg`;
        if (!window.manualMode) {
            document.body.classList.remove("light", "dark", "darker");
            document.body.classList.add(data.mode);
        }

        const forecastRow = document.getElementById("forecastRow");
        forecastRow.innerHTML = data.forecast
            .map((day) => {
                return `\n            <div class="forecast-card">\n                <div class="day">${day.day}</div>\n                <img src="/static/icons/${day.icon}.svg" class="small-icon" alt="icon" />\n                <div class="temps">${day.high}\u00B0 / ${day.low}\u00B0</div>\n            </div>`;
            })
            .join("");
    }

    fetchData();
    setInterval(fetchData, 60000);
});
