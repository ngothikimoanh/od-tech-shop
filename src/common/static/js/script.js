// Prevent event active element
// document.addEventListener("click", function (event) {
//     if (event.target.classList.contains("active") && (event.target.tagName === "A" || event.target.tagName === "BUTTON")) {
//         event.preventDefault()
//         event.stopPropagation()
//     }
// })

// Show all toasts
document.addEventListener('DOMContentLoaded', function () {
    var toastElList = document.querySelectorAll('.toast')
    toastElList.forEach(function (toastEl, index) {
        setTimeout(function () {
            var toast = new bootstrap.Toast(toastEl)
            toast.show()
        }, index * 600)
    })
})

// Auto switch theme
// const prefersDark = window.matchMedia('(prefers-color-scheme: dark)')
// const setTheme = () => {
//     const theme = prefersDark.matches ? 'dark' : 'light'
//     document.documentElement.setAttribute('data-bs-theme', theme)
// }
// setTheme()
// prefersDark.addEventListener('change', setTheme)

function currencyVND(value) {
    try {
        value = parseFloat(value);
        if (isNaN(value)) throw new Error();
        return value.toLocaleString("vi-VN") + "₫";
    } catch {
        return "0₫";
    }
}
