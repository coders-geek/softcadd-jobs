// Initialize tooltips and popovers
document.addEventListener('DOMContentLoaded', function() {
    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })

    // Enable popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'))
    popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl)
    })

    // Form validation
    const forms = document.querySelectorAll('.needs-validation')
    Array.prototype.slice.call(forms)
        .forEach(function (form) {
            form.addEventListener('submit', function (event) {
                if (!form.checkValidity()) {
                    event.preventDefault()
                    event.stopPropagation()
                }
                form.classList.add('was-validated')
            }, false)
        })

    // Auto-hide alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert')
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.classList.add('fade')
            alert.addEventListener('transitionend', () => alert.remove())
        }, 5000)
    })

    // Initialize date pickers
    const dateInputs = document.querySelectorAll('input[type="date"], input[type="datetime-local"]')
    dateInputs.forEach(input => {
        if (!input.value) {
            const now = new Date()
            const year = now.getFullYear()
            const month = String(now.getMonth() + 1).padStart(2, '0')
            const day = String(now.getDate()).padStart(2, '0')
            const hours = String(now.getHours()).padStart(2, '0')
            const minutes = String(now.getMinutes()).padStart(2, '0')

            if (input.type === 'date') {
                input.value = `${year}-${month}-${day}`
            } else {
                input.value = `${year}-${month}-${day}T${hours}:${minutes}`
            }
        }
    })

    // Salary range display
    function updateSalaryOutput() {
        const minSalary = document.getElementById('id_min_salary')
        const maxSalary = document.getElementById('id_max_salary')
        const output = document.getElementById('salaryOutput')

        if (minSalary && maxSalary && output) {
            output.innerText = `$${minSalary.value || '0'} - $${maxSalary.value || '0'}`
        }
    }

    const minSalaryInput = document.getElementById('id_min_salary')
    const maxSalaryInput = document.getElementById('id_max_salary')

    if (minSalaryInput && maxSalaryInput) {
        minSalaryInput.addEventListener('input', updateSalaryOutput)
        maxSalaryInput.addEventListener('input', updateSalaryOutput)
        updateSalaryOutput() // Initialize on page load
    }
})