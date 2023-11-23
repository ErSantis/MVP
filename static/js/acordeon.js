document.addEventListener("DOMContentLoaded", function () {
    const collapsibleButtons = document.querySelectorAll(
        ".collapsible-trigger-btn"
    );

    collapsibleButtons.forEach((collapsibleButton) => {
        const collapsibleContentDataHeight =
            collapsibleButton.nextElementSibling.offsetHeight;
        collapsibleButton.nextElementSibling.style.height = 0;
        collapsibleButton.addEventListener("click", (e) => {
            if (
                !e.currentTarget.parentElement.classList.contains("collapsible-tab__open")
            ) {
                e.currentTarget.parentElement.classList.toggle("collapsible-tab__open");
                e.currentTarget.nextElementSibling.style.height = `${collapsibleContentDataHeight}px`;
            } else {
                e.currentTarget.parentElement.classList.remove("collapsible-tab__open");
                e.currentTarget.nextElementSibling.style.height = 0;
            }
        });
    });
});