document.addEventListener("DOMContentLoaded", function () {
    // ✅ Emoji Dropdown Menu
    let dropdown = document.querySelector(".dropdown-menu");
    let emojiContainer = document.querySelector(".emoji-container");

    emojiContainer.addEventListener("click", function (event) {
        event.stopPropagation();
        dropdown.style.display = dropdown.style.display === "flex" ? "none" : "flex";
    });

    document.addEventListener("click", function () {
        dropdown.style.display = "none";
    });

    dropdown.addEventListener("click", function (event) {
        event.stopPropagation();
    });

    // ✅ Search Bar Auto-Suggestions
    const searchBar = document.getElementById("search-bar");
    const suggestionsBox = document.getElementById("suggestions");

    searchBar.addEventListener("input", function () {
        if (searchBar.value.trim() === "") {
            suggestionsBox.style.display = "none";
            return;
        }

        fetch(`/get-pet-suggestions/?query=${searchBar.value}`)
            .then(response => response.json())
            .then(data => {
                suggestionsBox.innerHTML = "";
                if (data.length === 0) {
                    suggestionsBox.style.display = "none";
                    return;
                }

                suggestionsBox.style.display = "block";

                data.forEach(pet => {
                    let suggestion = document.createElement("div");
                    suggestion.textContent = pet.name;
                    suggestion.classList.add("suggestion-item");
                    suggestion.addEventListener("click", function () {
                        searchBar.value = pet.name;
                        suggestionsBox.style.display = "none";
                    });
                    suggestionsBox.appendChild(suggestion);
                });
            })
            .catch(error => console.error("Error fetching suggestions:", error));
    });

    // ✅ Close suggestions on clicking outside
    document.addEventListener("click", function (e) {
        if (!searchBar.contains(e.target) && !suggestionsBox.contains(e.target)) {
            suggestionsBox.style.display = "none";
        }
    });

    // ✅ Animated Stats Counter
    function animateCount(id, start, end, duration) {
        let obj = document.getElementById(id);
        let range = end - start;
        let current = start;
        let increment = range / (duration / 10);
        let timer = setInterval(function () {
            current += increment;
            obj.innerText = Math.floor(current);
            if (current >= end) {
                clearInterval(timer);
                obj.innerText = end;
            }
        }, 10);
    }

    // ✅ Run stats animation when the section comes into view (only once)
    let statsAnimated = false;
    function startStatsAnimation() {
        if (statsAnimated) return;
        let statsSection = document.querySelector(".stats-section");
        let position = statsSection.getBoundingClientRect().top;
        let screenHeight = window.innerHeight;

        if (position < screenHeight - 100) {
            animateCount("petsAdopted", 100, 120, 3000);
            animateCount("happyHomes", 80, 95, 3000);
            statsAnimated = true;
            window.removeEventListener("scroll", startStatsAnimation);
        }
    }

    window.addEventListener("scroll", startStatsAnimation);

    // ✅ Remove Bottom Navbar & Replace with New Section
    function replaceBottomNavbar() {
        let bottomNavbar = document.querySelector(".bottom-navbar");
        if (bottomNavbar) {
            bottomNavbar.remove();
        }

        // Create a new attractive section
        let newSection = document.createElement("section");
        newSection.className = "new-attractive-section";
        newSection.innerHTML = `
            <div class="attractive-container">
                <h2>Find Your Perfect Pet 🐶🐱</h2>
                <p>Discover loving pets waiting for a home. Browse through a variety of adorable companions.</p>
                <a href="/adopt" class="explore-btn">Explore Now</a>
            </div>
        `;

        // Append the new section to a suitable place
        document.body.appendChild(newSection);
    }

    // Run this function once the page loads
    replaceBottomNavbar();
});
