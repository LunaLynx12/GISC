# GISC Wiki

## Overview
The GISC Wiki is a lightweight, client-side wiki designed for easy content management and accessibility. The site dynamically loads content from structured JSON files without requiring a backend, making it fast and efficient.

## Features

✅ Category-Based Navigation – Content is organized into categories for easy access.

✅ Dynamic Content Loading – Only the necessary JSON files are fetched to optimize performance.

✅ Fully Responsive – Works seamlessly on desktops, tablets, and mobile devices.

✅ GitHub Pages Compatible – Can be hosted easily without a backend.

## File Structure
```plaintext
/
├── index.html          # Main HTML file
├── styles.css          # Stylesheet for layout and design
├── script.js           # JavaScript for dynamic content loading
├── categories.json     # Lists all categories and their JSON file references
├── content/            # Folder containing individual category JSON files
│   ├── splunk.json
│   ├── wazuh.json
│   └── ...
└── images/             # Folder for images used in wiki articles
    ├── splunk
│   ├── wazuh
│   └── ...
```

## How It Works
1. **Loading the Sidebar**
   - The sidebar loads categories from `categories.json`.
   - Each category has topics, which reference a JSON file and a topic key.

2. **Fetching Topic Content**
   - When a topic is clicked, the corresponding JSON file from `content/` is fetched.
   - The topic's content is displayed dynamically on the main page.

## Example JSON Structure
```json
{
    "splunk": {
        "title": "Getting Started with Splunk",
        "content": [
            { "type": "text", "value": "Splunk is a powerful log analysis tool..." },
            { "type": "image", "value": "images/splunk-dashboard.png" }
        ]
    }
}
```

## Running Locally
```sh
# Clone the repository
git clone https://github.com/yourusername/gisc-wiki.git
cd gisc-wiki

# Open index.html in a browser
start index.html  # Windows
open index.html   # macOS
xdg-open index.html  # Linux
```

## Hosting on GitHub Pages
1. Commit and push your changes.
2. Go to **Settings > Pages** in your repository.
3. Set the branch to `main` (or `gh-pages` if using a separate branch).
4. Save and access your wiki via `https://yourusername.github.io/gisc-wiki/`.

## Contributing
Feel free to contribute by adding new categories, topics, or improving the layout. Fork the repository and submit a pull request!

## License
See the License file for details

