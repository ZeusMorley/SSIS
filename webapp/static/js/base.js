let selectedRow = null;

function addRowClickListeners() {
    const rows = document.querySelectorAll('#table-body .table-row');
    const editButton = document.getElementById('edit-button');
    const deleteButton = document.getElementById('delete-button');

    rows.forEach(row => {
        row.addEventListener('click', function() {
            const isSelected = row.classList.contains('selected');

            rows.forEach(r => r.classList.remove('selected'));

            if (!isSelected) {
                row.classList.add('selected');
                selectedRow = row; // Store the selected row
            } else {
                selectedRow = null; // Clear the selection
            }

            const hasSelection = selectedRow !== null;
            editButton.disabled = !hasSelection;
            deleteButton.disabled = !hasSelection;
        });
    });

    editButton.addEventListener('click', function() {
        if (selectedRow) {
            const collegeCode = selectedRow.querySelector('.college-code').textContent.trim();
            const collegeName = selectedRow.querySelector('.college-name').textContent.trim();
            showCollegeEditModal(collegeCode, collegeName);
        }
    });

    deleteButton.addEventListener('click', function() {
        if (selectedRow) {
            showConfirmationModal();
        }
    });
}

function showConfirmationModal() {
    const modal = document.getElementById('delete-confirmation-modal');
    const confirmButton = document.getElementById('confirm-delete-button');
    const cancelButton = document.getElementById('cancel-delete-button');

    modal.style.display = 'block';

    confirmButton.addEventListener('click', function() {
        deleteSelectedRow();
        closeConfirmationModal();
    });

    cancelButton.addEventListener('click', function() {
        closeConfirmationModal();
    });

    const closeButton = document.getElementById('close-confirmation-modal');
    closeButton.addEventListener('click', function() {
        closeConfirmationModal();
    });

    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            closeConfirmationModal();
        }
    });
}

function closeConfirmationModal() {
    const modal = document.getElementById('delete-confirmation-modal');
    modal.style.display = 'none';
}

function deleteSelectedRow() {
    if (selectedRow) {
        const collegeCode = selectedRow.querySelector('.college-code').textContent.trim();

        fetch('/college/delete-college', {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ collegeCode })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                selectedRow.remove();
                selectedRow = null;
                showErrorModal(data.message, data.type);
            } else {
                showErrorModal(data.message, data.type);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            showErrorModal('An unexpected error occurred.', 'error');
        });
    }
}


function renderStudentRows() {
    let rowsHtml = '';
    students.forEach((student, index) => {
        rowsHtml += `
            <div class="table-row">
                <div class="index-column">${index + 1}</div>
                <div class="profile-picture">
                    <img src="${student.cloudinary_url}" 
                        alt="Profile Picture" 
                        onerror="this.onerror=null; this.src='https://res.cloudinary.com/dmvwcolfi/image/upload/v1722969919/student_photos/up5upsjz6e86isvae6qw.jpg';" />
                </div>

                <div class="id-number">${student.studentId}</div>
                <div class="first-last-name">${student.firstName}<br>${student.lastName}</div>
                <div class="course">${student.courseName}<br>(${student.courseCode})</div>
                <div class="year">${student.year}</div>
                <div class="gender">${student.gender}</div>
                <div class="college">${student.collegeName}<br>(${student.collegeCode})</div>
            </div>
        `;
    });
    return rowsHtml;
}

function renderCourseRows() {
    let rowsHtml = '';
    courses.forEach((course, index) => {
        rowsHtml += `
            <div class="table-row">
                <div class="index-column">${index + 1}</div>
                <div class="course-code">${course.courseCode}</div>
                <div class="course-name">${course.courseName}</div>
                <div class="college">${course.collegeName}<br>(${course.collegeCode})</div>
                <div class="student-count">${course.studentCount}</div>
            </div>
        `;
    });
    return rowsHtml;
}

function renderCollegeRows() {
    let rowsHtml = '';
    colleges.forEach((college, index) => {
        rowsHtml += `
            <div class="table-row">
                <div class="index-column">${index + 1}</div>
                <div class="college-code">${college.collegeCode}</div>
                <div class="college-name">${college.collegeName}</div>
                <div class="course-count">${college.courseCount}</div>
            </div>
        `;
    });
    return rowsHtml;
}

function filterTable() {
    const searchInput = document.getElementById('search-input').value.toLowerCase();
    const tabName = document.querySelector('.tab-button.active').id.replace('-tab', '');
    const rows = document.querySelectorAll('#table-body .table-row');

    rows.forEach(row => {
        const textContent = Array.from(row.children)
            .filter(cell => !cell.classList.contains('index-column'))
            .map(cell => cell.textContent.toLowerCase())
            .join(' ');
            
        if (textContent.includes(searchInput)) {
            row.style.display = '';
        } else {
            row.style.display = 'none';
        }

        if (searchInput === "male") {
            if (textContent.includes("female")) {
                row.style.display = 'none';
            } else {
                row.style.display = '';
            }
        }
    });
}