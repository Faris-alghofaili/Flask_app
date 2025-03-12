document.addEventListener('DOMContentLoaded', () => {
    const addProjectBtn = document.getElementById('addProjectBtn');
    const projectModal = document.getElementById('projectModal');
    const closeModal = document.getElementById('closeModal');
    const projectForm = document.getElementById('projectForm');
    const projectsGrid = document.getElementById('projectsGrid');

    // Open modal on "Add new project" button click
    addProjectBtn.addEventListener('click', () => {
        projectModal.style.display = 'flex';
    });

    // Close modal when clicking the close button
    closeModal.addEventListener('click', () => {
        projectModal.style.display = 'none';
    });

    // Close modal when clicking outside the modal content
    window.addEventListener('click', (event) => {
        if (event.target === projectModal) {
            projectModal.style.display = 'none';
        }
    });

    // Handle form submission to create a new project card
    projectForm.addEventListener('submit', (event) => {
        event.preventDefault();

        // Get user input
        const projectName = document.getElementById('projectName').value;
        const translatedVersion = document.getElementById('translatedVersion').value;
        const language = document.getElementById('language').value;

        // Create new project card
        const projectCard = document.createElement('div');
        projectCard.className = 'project-card';
        projectCard.innerHTML = `
            <p class="project-title">${projectName}</p>
            <p class="project-lang">${language}</p>
            <button class="project-btn">Next</button>
        `;

        // Add the new card to the grid
        projectsGrid.appendChild(projectCard);

        // Reset form and close modal
        projectForm.reset();
        projectModal.style.display = 'none';
    });
});
