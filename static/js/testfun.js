const templateList = document.getElementById('template-list');
const expandButtons = document.querySelectorAll('.expand-button');

expandButtons.forEach(button => {
    button.addEventListener('click', () => {
        const templateContent = button.nextElementSibling;
        templateContent.classList.toggle('hidden');
    });
});
