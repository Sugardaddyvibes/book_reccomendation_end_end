document.addEventListener("DOMContentLoaded", function () {
    const flashMessages = document.querySelectorAll(".flash-message");
    flashMessages.forEach((message) => {
        setTimeout(() => {
            message.style.opacity = "0";
            setTimeout(() => {
                message.remove();
            }, 300);
        }, 4500);
    });
});
