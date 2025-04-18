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

const browserIdKey = 'browser_id'
function generateUUID() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}
function getBrowserId() {
    const match = document.cookie.match(new RegExp('(^| )' + browserIdKey + '=([^;]+)'))
    return match ? match[2] : null
}
function setBrowserId() {
    const uuid = generateUUID()
    document.cookie = `${browserIdKey}=${uuid}`;
    console.log('Set browser id success')
}
if (getBrowserId() === null) setBrowserId()
