document.addEventListener('DOMContentLoaded', function() {
    showTab('student');
    
    document.getElementById('search-input').value = '';
    
    filterTable(); 
});

function showTab(tabName) {
    const tabs = document.querySelectorAll('.tab-button');
    tabs.forEach(tab => {
        tab.classList.remove('active');
    });

    document.querySelector(`.tab-button[onclick="showTab('${tabName}')"]`).classList.add('active');

    let headersHtml = '';
    let bodyHtml = '';

    if (tabName === 'student') {
        headersHtml = `
            <div class="index-column"></div>
            <div class="profile-picture">Profile Picture</div>
            <div class="id-number">Id Number</div>
            <div class="first-last-name">First Name<br>Last Name</div>
            <div class="course">Course</div>
            <div class="year">Year</div>
            <div class="gender">Gender</div>
            <div class="college">College</div>
        `;
        bodyHtml = renderStudentRows();
    } else if (tabName === 'course') {
        headersHtml = `
            <div class="index-column"></div>
            <div class="course-code">Course Code</div>
            <div class="course-name">Course Name</div>
            <div class="college">College</div>
            <div class="student-count">Number of Students</div>
        `;
        bodyHtml = renderCourseRows();
    } else if (tabName === 'college') {
        headersHtml = `
            <div class="index-column"></div>
            <div class="college-code">College Code</div>
            <div class="college-name">College Name</div>
            <div class="course-count">Number of Courses</div>
        `;
        bodyHtml = renderCollegeRows();
    }

    document.getElementById('table-headers').innerHTML = headersHtml;
    document.getElementById('table-body').innerHTML = bodyHtml;

    document.querySelectorAll('#table-body .table-row').forEach(row => row.classList.remove('selected'));
    addRowClickListeners();

    const editButton = document.getElementById('edit-button');
    const deleteButton = document.getElementById('delete-button');
    editButton.disabled = true;
    deleteButton.disabled = true;
}

