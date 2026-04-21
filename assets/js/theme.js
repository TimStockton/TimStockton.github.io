const toggle = document.getElementById("theme-toggle");
const root = document.documentElement;

// Load saved theme
const savedTheme = localStorage.getItem("theme");
if (savedTheme === "dark") {
    root.setAttribute("data-theme", "dark");
}

if (toggle) {
    toggle.addEventListener("click", () => {
        const current = root.getAttribute("data-theme");

        if (current === "dark") {
            root.removeAttribute("data-theme");
            localStorage.setItem("theme", "light");
            toggle.textContent = "🌙";
        } else {
            root.setAttribute("data-theme", "dark");
            localStorage.setItem("theme", "dark");
            toggle.textContent = "☀️";
        }
    });
}