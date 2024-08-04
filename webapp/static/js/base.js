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
            }

            const hasSelection = document.querySelector('#table-body .table-row.selected') !== null;
            editButton.disabled = !hasSelection;
            deleteButton.disabled = !hasSelection;
        });
    });
}

function renderStudentRows() {
    let rowsHtml = '';
    students.forEach((student, index) => {
        rowsHtml += `
            <div class="table-row">
                <div class="index-column">${index + 1}</div>
                <div class="profile-picture"><img src="${student.cloudinary_url}" alt="Profile Picture" /></div>
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
        const cells = row.getElementsByClassName('index-column')[0];
        const textContent = Array.from(row.children).map(cell => cell.textContent.toLowerCase()).join(' ');
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