document.addEventListener("DOMContentLoaded", function () {
    loadReadme();
    loadSidebar();
});

function loadReadme() {
    fetch("README.md")
    .then(response => response.text())
    .then(markdown => {
        let converter = new showdown.Converter();
        let htmlContent = converter.makeHtml(markdown);
        document.getElementById("content-body").innerHTML = htmlContent;
    })
    .catch(error => {
        console.error("Error loading README.md:", error);
        document.getElementById("content-body").innerHTML = "<p>Failed to load content.</p>";
    });
}

function loadSidebar() {
    fetch("categories.json")
        .then(response => response.json())
        .then(categories => {
            let sidebar = document.getElementById("sidebar-content");
            sidebar.innerHTML = "";

            categories.forEach(category => {
                let section = document.createElement("div");
                section.innerHTML = `<h2>${category.name}</h2><ul></ul>`;
                let ul = section.querySelector("ul");

                category.topics.forEach(topic => {
                    let li = document.createElement("li");
                    li.textContent = topic.name;
                    li.onclick = () => loadTopic(category.file, topic.key);
                    ul.appendChild(li);
                });

                sidebar.appendChild(section);
            });
        })
        .catch(error => console.error("Error loading categories:", error));
}

function loadTopic(categoryFile, topicKey) {
    fetch(`content/${categoryFile}`)
        .then(response => response.json())
        .then(data => {
            if (data[topicKey]) {
                showContent(data[topicKey]);
            } else {
                console.error("Topic not found in", categoryFile);
            }
        })
        .catch(error => console.error("Error loading topic:", error));
}
function showContent(topic) {
    let contentArea = document.querySelector(".content");
    contentArea.innerHTML = `<h2>${topic.title}</h2>`;

    topic.content.forEach(section => {
        if (section.type === "text") {
            let paragraph = document.createElement("p");
            paragraph.innerText = section.value;
            contentArea.appendChild(paragraph);
        } else if (section.type === "image") {
            let image = document.createElement("img");
            image.src = section.value;
            contentArea.appendChild(image);
        } else if (section.type === "subtitle") {
            let subtitle = document.createElement("h3");
            subtitle.innerText = section.value;
            contentArea.appendChild(subtitle);
        } else if (section.type === "list") {
            let ul = document.createElement("ul");
            section.value.forEach(item => {
                let li = document.createElement("li");
                li.innerText = item;
                ul.appendChild(li);
            });
            contentArea.appendChild(ul);
        } else if (section.type === "pdf") {
            let iframe = document.createElement("iframe");
            iframe.src = section.value;
            iframe.width = "100%";
            iframe.height = "500px"; // Adjust as needed
            iframe.style.border = "none";
            contentArea.appendChild(iframe);
        }
    });
}

document.addEventListener("DOMContentLoaded", function() {
    const sidebar = document.querySelector(".sidebar");
    const toggleBtn = document.createElement("button");
    toggleBtn.textContent = "☰ Menu";
    toggleBtn.classList.add("sidebar-toggle");
    document.body.appendChild(toggleBtn);

    toggleBtn.addEventListener("click", function() {
        sidebar.classList.toggle("visible");
    });
});
