function showErrorModal(message, type) {
    let existingModal = document.querySelector('.error-modal');
    if (existingModal) {
        existingModal.remove();
    }

    const errorModal = document.createElement('div');
    errorModal.className = `error-modal ${type}`;
    errorModal.innerHTML = `<p>${message}</p>`;
    document.body.appendChild(errorModal);
    errorModal.style.display = 'block';

    setTimeout(() => {
        errorModal.style.display = 'none';
        document.body.removeChild(errorModal);
    }, 3000);
}
