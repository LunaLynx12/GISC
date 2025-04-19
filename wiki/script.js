const GITHUB_USERNAME = 'LunaLynx12';
const GITHUB_REPO = 'GISC';
const GITHUB_BRANCH = 'main';

document.addEventListener('DOMContentLoaded', function () {
    if (window.location.hash.startsWith('#/wiki/')) {
        loadMarkdownContent();
    } else {
        fetchTeamStructure();
    }
});

async function fetchFolderContents(path) {
    const url = `https://api.github.com/repos/${GITHUB_USERNAME}/${GITHUB_REPO}/contents/${path}?ref=${GITHUB_BRANCH}`;
    const response = await fetch(url);
    if (!response.ok) throw new Error(`GitHub API error: ${response.status}`);
    return response.json();
}

async function fetchTeamStructure() {
    try {
        const teams = await fetchFolderContents('wiki');
        const allowedTeams = ['Splunk', 'Attack Scripts', 'Infrastructure'];

        const teamFolders = teams.filter(item =>
            item.type === 'dir' && allowedTeams.includes(item.name)
        );

        const teamData = await Promise.all(
            teamFolders.map(async team => {
                const members = await fetchFolderContents(`wiki/${team.name}`);
                return {
                    id: team.name,
                    name: team.name,
                    members: members.filter(m => m.type === 'dir')
                };
            })
        );

        renderTeamList(teamData);
    } catch (error) {
        console.error('Error loading team structure:', error);
        renderError('Failed to load team structure. Please try again later.');
    }
}

function renderTeamList(teams) {
    const teamsContainer = document.getElementById('teams-list');
    teamsContainer.innerHTML = '';

    if (teams.length === 0) {
        teamsContainer.innerHTML = '<p>No teams found.</p>';
        return;
    }

    teams.forEach(team => {
        const teamCard = document.createElement('div');
        teamCard.className = 'team-card';

        const memberList = team.members.length > 0 ?
            `<ul class="member-list">
                ${team.members.map(member =>
                    `<li>
                        <a href="#/wiki/${team.id}/${member.name}/notes.md" 
                           data-path="${team.id}/${member.name}/notes.md">
                            ${member.name}
                        </a>
                    </li>`
                ).join('')}
            </ul>` :
            '<p>No members in this team</p>';

        teamCard.innerHTML = `
            <h3>${team.name}</h3>
            ${memberList}
        `;

        teamsContainer.appendChild(teamCard);
    });

    document.querySelectorAll('.member-list a').forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();
            const path = this.getAttribute('data-path');
            window.location.hash = `#/wiki/${path}`;
            loadMarkdownContent();
        });
    });
}

async function loadMarkdownContent() {
    const hash = window.location.hash.substring(1);
    const pathParts = hash.split('/').slice(2);
    const fullPath = pathParts.join('/');

    try {
        const lastSegment = pathParts[pathParts.length - 1] || '';
        const isFile = lastSegment.includes('.');

        if (isFile) {
            await renderFileContent(fullPath);
        } else {
            // Only show directory listing - no automatic notes.md search
            const items = await fetchFolderContents(`wiki/${fullPath}`);
            renderDirectoryListing(fullPath, items);
        }
    } catch (error) {
        console.error('Error loading content:', error);
        renderError('Failed to load content. Please try again later.');
    }
}

async function renderFileContent(fullPath) {
    const mainContent = document.querySelector('main');
    const breadcrumb = generateBreadcrumb(fullPath.split('/'));
    const rawUrl = `https://raw.githubusercontent.com/${GITHUB_USERNAME}/${GITHUB_REPO}/${GITHUB_BRANCH}/wiki/${fullPath}`;
    const githubUrl = `https://github.com/${GITHUB_USERNAME}/${GITHUB_REPO}/blob/${GITHUB_BRANCH}/wiki/${fullPath}`;

    // Get directory contents for navigation
    const directoryPath = fullPath.split('/').slice(0, -1).join('/');
    const directoryItems = await fetchFolderContents(`wiki/${directoryPath}`);

    // Check if this is an unsupported file type that should redirect
    if (shouldRedirect(fullPath)) {
        // Only redirect on direct click, not automatically
        if (!sessionStorage.getItem('preventRedirect')) {
            sessionStorage.setItem('preventRedirect', 'true');
            window.location.href = githubUrl;
            return;
        }
        sessionStorage.removeItem('preventRedirect');
    }

    // Handle different file types
    if (fullPath.endsWith('.md')) {
        const response = await fetch(rawUrl);
        const fileContent = await response.text();
        const htmlContent = marked.parse(fileContent);
        
        // Filter out current file and sort directories first
        const otherFiles = directoryItems
            .filter(item => item.name !== fullPath.split('/').pop())
            .sort((a, b) => {
                if (a.type === b.type) return a.name.localeCompare(b.name);
                return a.type === 'dir' ? -1 : 1;
            });

        const fileList = otherFiles.map(item => {
            const icon = item.type === 'dir' ? '📁' : getFileIcon(item.name);
            return `
                <li>
                    <a href="#/wiki/${directoryPath}/${item.name}" class="${shouldRedirect(`${directoryPath}/${item.name}`) ? 'redirect-link' : ''}">
                        ${icon} ${item.name}
                    </a>
                </li>
            `;
        }).join('');

        mainContent.innerHTML = `
            ${breadcrumb}
            <div class="markdown-content">${htmlContent}</div>
            ${otherFiles.length > 0 ? `
            <div class="file-navigation">
                <h3>Other Files in This Directory:</h3>
                <ul>${fileList}</ul>
            </div>
            ` : ''}
        `;
    } 
    else if (isImageFile(fullPath)) {
        mainContent.innerHTML = `
            ${breadcrumb}
            <div class="image-container">
                <img src="${rawUrl}" alt="${fullPath.split('/').pop()}" />
                <p><a href="${rawUrl}" download>Download Image</a></p>
            </div>
        `;
    }
    else if (isCodeFile(fullPath)) {
        const response = await fetch(rawUrl);
        const fileContent = await response.text();
        const language = getCodeLanguage(fullPath);
        const highlightedCode = hljs.highlight(fileContent, { language }).value;
        mainContent.innerHTML = `
            ${breadcrumb}
            <div class="code-container">
                <pre><code class="language-${language}">${highlightedCode}</code></pre>
                <p><a href="${githubUrl}" target="_blank">View on GitHub</a></p>
            </div>
        `;
    }

    // Add click handlers for navigation links
    document.querySelectorAll('.file-navigation a').forEach(link => {
        link.addEventListener('click', function (e) {
            if (this.classList.contains('redirect-link')) {
                sessionStorage.setItem('preventRedirect', 'true');
            }
        });
    });
}

function renderDirectoryListing(currentPath, items) {
    const mainContent = document.querySelector('main');
    const breadcrumb = generateBreadcrumb(currentPath.split('/'));

    const content = items.map(item => {
        const icon = item.type === 'dir' ? '📁' : getFileIcon(item.name);
        const href = `#/wiki/${currentPath ? currentPath + '/' : ''}${item.name}`;
        const redirectClass = shouldRedirect(`${currentPath}/${item.name}`) ? 'redirect-link' : '';
        return `
            <li class="directory-item">
                <a href="${href}" class="${redirectClass}">${icon} ${item.name}</a>
            </li>
        `;
    }).join('');

    mainContent.innerHTML = `
        ${breadcrumb}
        <div class="directory-listing">
            <h2>${decodeURIComponent(currentPath) || 'Root Directory'}</h2>
            <ul>${content}</ul>
        </div>
    `;

    // Add click handlers for redirect links
    document.querySelectorAll('.directory-item a.redirect-link').forEach(link => {
        link.addEventListener('click', function (e) {
            sessionStorage.setItem('preventRedirect', 'true');
        });
    });
}

function shouldRedirect(filename) {
    // Only redirect for specific file types
    return /\.(html?|pdf|docx?|xlsx?|pptx?|zip|rar|exe|dmg)$/i.test(filename);
}

function generateBreadcrumb(pathParts) {
    let breadcrumb = '<div class="breadcrumb"><a href="#">Home</a>';
    let currentPath = '';

    pathParts.forEach((part, index) => {
        if (part) {
            currentPath += `${part}/`;
            if (index < pathParts.length - 1) {
                breadcrumb += ` / <a href="#/wiki/${currentPath.slice(0, -1)}">${decodeURIComponent(part)}</a>`;
            } else {
                breadcrumb += ` / ${decodeURIComponent(part)}`;
            }
        }
    });

    breadcrumb += '</div>';
    return breadcrumb;
}

// Helper functions
function isImageFile(filename) {
    return /\.(jpg|jpeg|png|gif|svg|webp)$/i.test(filename);
}

function isCodeFile(filename) {
    return /\.(js|py|java|cpp|c|html|css|php|rb|sh|json)$/i.test(filename);
}

function getCodeLanguage(filename) {
    const extension = filename.split('.').pop().toLowerCase();
    const languages = {
        'js': 'javascript',
        'py': 'python',
        'html': 'html',
        'css': 'css',
        'java': 'java',
        'cpp': 'cpp',
        'c': 'c',
        'php': 'php',
        'rb': 'ruby',
        'sh': 'bash',
        'json': 'json'
    };
    return languages[extension] || 'plaintext';
}

function getFileIcon(filename) {
    if (isImageFile(filename)) return '🖼️';
    if (isCodeFile(filename)) return '📝';
    if (filename.endsWith('.pdf')) return '📕';
    if (filename.endsWith('.doc') || filename.endsWith('.docx')) return '📄';
    if (filename.endsWith('.md')) return '📄';
    return '📄';
}

function renderError(message) {
    const mainContent = document.querySelector('main');
    mainContent.innerHTML = `
        <div class="error-message">
            <p>${message}</p>
            <button onclick="window.location.hash=''">Return Home</button>
        </div>
    `;
}

window.addEventListener('hashchange', function () {
    if (window.location.hash.startsWith('#/wiki/')) {
        loadMarkdownContent();
    } else {
        document.querySelector('main').innerHTML = `
            <div class="teams-container">
                <h2>Teams</h2>
                <div id="teams-list" class="teams-grid"></div>
            </div>
        `;
        fetchTeamStructure();
    }
});