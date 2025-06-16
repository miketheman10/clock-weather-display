document.addEventListener("DOMContentLoaded", () => {
    const toggleButton = document.getElementById("themeToggle");

    toggleButton.addEventListener("click", () => {
        const body = document.body;
        const currentMode = body.classList.contains("light")
            ? "light"
            : body.classList.contains("dark")
            ? "dark"
            : "darker";

        let nextMode;
        if (currentMode === "light") nextMode = "dark";
        else if (currentMode === "dark") nextMode = "darker";
        else nextMode = "light";

        body.classList.remove("light", "dark", "darker");
        body.classList.add(nextMode);
    });

    // Auto-refresh every 5 minutes
    setTimeout(() => {
        window.location.reload();
    }, 300000);
});
