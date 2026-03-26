// Contact Form
document.getElementById("contactForm").addEventListener("submit", async function(e) {
    e.preventDefault();
    const data = {
        name: document.getElementById("name").value,
        email: document.getElementById("email").value,
        message: document.getElementById("message").value
    };
    const res = await fetch('/contact', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    });
    const result = await res.json();
    document.getElementById("response").innerText = result.message;
});

// Scroll Animation
const sections = document.querySelectorAll("section");
function revealSections() {
    sections.forEach(section => {
        const top = section.getBoundingClientRect().top;
        const trigger = window.innerHeight - 100;
        if (top < trigger) {
            section.style.opacity = "1";
            section.style.transform = "translateY(0)";
        }
    });
}
window.addEventListener("scroll", revealSections);
window.addEventListener("load", revealSections);