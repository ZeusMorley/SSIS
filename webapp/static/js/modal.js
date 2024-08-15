function previewPhoto() {
    const fileInput = document.getElementById('student-photo');
    const photoPreview = document.getElementById('photo-preview');

    if (fileInput.files && fileInput.files[0]) {
        const reader = new FileReader();

        reader.onload = function(e) {
            photoPreview.src = e.target.result;
            photoPreview.style.display = 'block';
        }

        reader.readAsDataURL(fileInput.files[0]); 
    } else {
        photoPreview.style.display = 'none';
    }
}


function populateCollegeDropdown() {
    const collegeDropdown = document.getElementById('college-dropdown');
    if (!collegeDropdown) return;

    colleges.forEach(college => {
        const option = document.createElement('option');
        option.value = college.collegeCode;
        option.textContent = `${college.collegeCode} - ${college.collegeName}`;
        collegeDropdown.appendChild(option);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    populateCollegeDropdown();
});

function populateCourseDropdown() {
    const courseDropdown = document.getElementById('course-dropdown');
    if (!courseDropdown) return;

    courses.forEach(course => {
        const option = document.createElement('option');
        option.value = course.courseCode;
        option.textContent = `${course.courseCode} - ${course.courseName}`;
        courseDropdown.appendChild(option);
    });
}

document.addEventListener('DOMContentLoaded', () => {
    populateCourseDropdown();
});


function attachCourseFormSubmitListener() {
    const form = document.getElementById('add-course-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(form);
            const courseData = Object.fromEntries(formData.entries());

            fetch('/course/add-course', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(courseData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showErrorModal(data.message, data.type);
                    setTimeout(() => {
                        location.reload();
                    }, 3000);
                } else {
                    showErrorModal(data.message, data.type);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
}

function attachStudentFormSubmitListener() {
    const form = document.getElementById('add-student-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(form);

            fetch('/student/add-student', {
                method: 'POST',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showErrorModal(data.message, data.type);
                    setTimeout(() => {
                        location.reload();
                    }, 3000);
                } else {
                    showErrorModal(data.message, data.type);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
}


function showCollegeEditModal(collegeCode, collegeName) {
    const modal = document.getElementById('add-modal');
    const modalBody = document.getElementById('modal-body');

    const modalContent = `
        <form id="edit-college-form">
            <label for="college-code">College Code:</label>
            <input type="text" id="college-code" name="newCollegeCode" value="${collegeCode}"><br>
            <label for="college-name">College Name:</label>
            <input type="text" id="college-name" name="newCollegeName" value="${collegeName}"><br>
            <input type="hidden" id="current-college-code" name="currentCollegeCode" value="${collegeCode}">
            <button type="submit" class="confirm-button" id="college-confirm">Confirm</button>
        </form>
    `;

    modalBody.innerHTML = modalContent;
    modal.className = 'modal college-modal';
    modal.style.display = "block";

    attachEditCollegeFormSubmitListener();
}

function attachEditCollegeFormSubmitListener() {
    const form = document.getElementById('edit-college-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(form);
            const collegeData = Object.fromEntries(formData.entries());

            fetch('/college/update-college', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(collegeData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showErrorModal(data.message, data.type);
                    setTimeout(() => {
                        location.reload();
                    }, 3000);
                } else {
                    showErrorModal(data.message, data.type);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
}

function showCourseEditModal(courseCode, courseName, collegeName) {
    const modal = document.getElementById('add-modal');
    const modalBody = document.getElementById('modal-body');

    const modalContent = `
        <form id="edit-course-form">
            <label for="course-code">Course Code:</label>
            <input type="text" id="course-code" name="courseCode" value="${courseCode}"><br>
            <label for="course-name">Course Name:</label>
            <input type="text" id="course-name" name="courseName" value="${courseName}"><br>
            <label for="college-name">College Name:</label>
            <select id="college-dropdown" name="collegeName">
            </select><br>
            <input type="hidden" id="current-course-code" name="currentCourseCode" value="${courseCode}">
            <button type="submit" class="confirm-button" id="course-confirm">Confirm</button>
        </form>
    `;

    modalBody.innerHTML = modalContent;
    modal.className = 'modal course-modal';
    modal.style.display = "block";

    populateCollegeDropdown();

    attachEditCourseFormSubmitListener(courseCode);
}

function attachEditCourseFormSubmitListener() {
    const form = document.getElementById('edit-course-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(form);
            const courseData = Object.fromEntries(formData.entries());

            fetch('/course/update-course', {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(courseData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showErrorModal(data.message, data.type);
                    setTimeout(() => {
                        location.reload();
                    }, 3000);
                } else {
                    showErrorModal(data.message, data.type);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
}

function showStudentEditModal(studentId, firstName, lastName, gender, year, cloudinary_url, courseCode) {
    const modal = document.getElementById('add-modal');
    const modalBody = document.getElementById('modal-body');

    const modalContent = `
        <form id="edit-student-form" enctype="multipart/form-data">
            <label for="student-id">ID Number:</label>
            <input type="text" id="student-id" name="studentId" value="${studentId}"><br>
            
            <label for="first-name">First Name:</label>
            <input type="text" id="first-name" name="firstName" value="${firstName}"><br>
            
            <label for="last-name">Last Name:</label>
            <input type="text" id="last-name" name="lastName" value="${lastName}"><br>

            <label for="course-name">Course Name:</label>
            <select id="course-dropdown" name="courseName">
            </select><br>

            <div class="year-and-gender">
                <label for="year">Year</label>
                <label for="gender">Gender:</label><br>
            </div>

            <div class="radio-group">
                <div class="year1-and-male">
                    <div class="radio-year">
                        <label for="year1">1</label>
                        <input type="radio" id="year1" name="year" value="1" ${year === "1" ? "checked" : ""}>
                    </div>

                    <div class="radio-gender">
                        <input type="radio" id="male" name="gender" value="Male" ${gender === "Male" ? "checked" : ""}>
                        <label for="male">Male</label><br>
                    </div>
                </div>

                <div class="year2-and-female">
                    <div class="radio-year">
                        <label for="year2">2</label>
                        <input type="radio" id="year2" name="year" value="2" ${year === "2" ? "checked" : ""}>
                    </div>

                    <div class="radio-gender">
                        <input type="radio" id="female" name="gender" value="Female" ${gender === "Female" ? "checked" : ""}>
                        <label for="female">Female</label><br>
                    </div>
                </div>

                <div class="radio-year">
                    <label for="year3">3</label>
                    <input type="radio" id="year3" name="year" value="3" ${year === "3" ? "checked" : ""}>
                </div>

                <div class="radio-year">
                    <label for="year4">4</label>
                    <input type="radio" id="year4" name="year" value="4" ${year === "4" ? "checked" : ""}>
                </div>
            </div>
            
            <label for="student-photo">Upload Photo:</label>
            <input type="file" id="student-photo" name="studentPhoto" accept="image/*" onchange="previewPhoto()"><br>
            
            <img src="${cloudinary_url}"
                id="photo-preview"
                alt="Profile Picture" 
                onerror="this.onerror=null; this.src='https://res.cloudinary.com/dmvwcolfi/image/upload/v1722969919/student_photos/up5upsjz6e86isvae6qw.jpg';" />

            <input type="checkbox" id="clearPhoto" name="clearPhoto" value="on">
            <label for="clearPhoto">Clear Profile Photo</label>
            
            <input type="hidden" id="current-student-id" name="currentStudentId" value="${studentId}">
            <button type="submit" class="confirm-button" id="student-confirm">Confirm</button>
        </form>

    `;

    modalBody.innerHTML = modalContent;
    modal.className = 'modal student-modal';
    modal.style.display = "block";

    populateCourseDropdown(courseCode);

    attachEditStudentFormSubmitListener(studentId);
}


function attachEditStudentFormSubmitListener() {
    const form = document.getElementById('edit-student-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();

            const formData = new FormData(form);

            fetch(`/student/update-student`, {
                method: 'PUT',
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showErrorModal(data.message, data.type);
                    setTimeout(() => {
                        location.reload();
                    }, 3000);
                } else {
                    showErrorModal(data.message, data.type);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
}

function showAddModal() {
    const modal = document.getElementById('add-modal');
    const modalBody = document.getElementById('modal-body');
    const activeTab = document.querySelector('.tab-button.active').id.replace('-tab', '');

    let modalContent = '';

    if (activeTab === 'student') {
        modalContent = `
            <form id="add-student-form" enctype="multipart/form-data">
                <label for="student-id">ID-Number:</label>
                <input type="text" id="student-id" name="studentId"><br>

                <label for="first-name">First Name:</label>
                <input type="text" id="first-name" name="firstName"><br>

                <label for="last-name">Last Name:</label>
                <input type="text" id="last-name" name="lastName"><br>

                <label for="course-name">Course Name:</label>
                <select id="course-dropdown" name="courseName">
                </select><br>
                
                <div class="year-and-gender">
                    <label for="year">Year</label>
                    <label for="gender">Gender:</label><br>
                </div>

                <div class="radio-group">
                    <div class="year1-and-male">
                        <div class="radio-year">
                            <label for="year1">1</label>
                            <input type="radio" id="year1" name="year" value="1">
                        </div>

                        <div class="radio-gender">
                            <input type="radio" id="male" name="gender" value="Male">
                            <label for="male">Male</label><br>
                        </div>
                    </div>

                    <div class="year2-and-female">
                        <div class="radio-year">
                            <label for="year2">2</label>
                            <input type="radio" id="year2" name="year" value="2">
                        </div>

                        <div class="radio-gender">
                            <input type="radio" id="female" name="gender" value="Female">
                            <label for="female">Female</label><br>
                        </div>
                    </div>

                    <div class="radio-year">
                        <label for="year3">3</label>
                        <input type="radio" id="year3" name="year" value="3">
                    </div>

                    <div class="radio-year">
                        <label for="year4">4</label>
                        <input type="radio" id="year4" name="year" value="4">
                    </div>
                </div>

                <label for="student-photo">Upload Photo:</label>
                <input type="file" id="student-photo" name="studentPhoto" accept="image/*" onchange="previewPhoto()"><br>
                
                <img id="photo-preview" src="https://res.cloudinary.com/dmvwcolfi/image/upload/v1722969919/student_photos/up5upsjz6e86isvae6qw.jpg">
                
                <button type="submit" class="confirm-button" id="student-confirm">Confirm</button>
            </form>
        `;
        modal.className = 'modal student-modal';
        modalBody.innerHTML = modalContent;
        populateCourseDropdown();
        attachStudentFormSubmitListener();

    } else if (activeTab === 'course') {
        modalContent = `
            <form id="add-course-form">
                <label for="course-code">Course Code:</label>
                <input type="text" id="course-code" name="courseCode"><br>
                <label for="course-name">Course Name:</label>
                <input type="text" id="course-name" name="courseName"><br>\
                <label for="college-name">College Name:</label>
                <select id="college-dropdown" name="collegeName">
                </select><br>
                <button type="submit" class="confirm-button" id="course-confirm">Confirm</button>
            </form>
        `;
        modal.className = 'modal course-modal';
        modalBody.innerHTML = modalContent;
        populateCollegeDropdown();
        attachCourseFormSubmitListener();

    } else if (activeTab === 'college') {
        modalContent = `
            <form id="add-college-form">
                <label for="college-code">College Code:</label>
                <input type="text" id="college-code" name="collegeCode"><br>
                <label for="college-name">College Name:</label>
                <input type="text" id="college-name" name="collegeName"><br>
                <button type="submit" class="confirm-button" id="college-confirm">Confirm</button>
            </form>
        `;
        modal.className = 'modal college-modal';
        modalBody.innerHTML = modalContent;
        attachCollegeFormSubmitListener();
    }

    modal.style.display = "block";
}

function closeModal() {
    const modal = document.getElementById('add-modal');
    modal.style.display = "none";
}

window.onclick = function(event) {
    const modal = document.getElementById('add-modal');
    if (event.target === modal) {
        modal.style.display = "none";
    }
}

function attachCollegeFormSubmitListener() {
    const form = document.getElementById('add-college-form');
    if (form) {
        form.addEventListener('submit', function(event) {
            event.preventDefault();
            const formData = new FormData(form);
            const collegeData = Object.fromEntries(formData.entries());

            fetch('/college/add-college', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(collegeData)
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    showErrorModal(data.message, data.type);
                    setTimeout(() => {
                        location.reload();
                    }, 3000);
                } else {
                    setTimeout(() => {
                        location.reload();
                    }, 3000);
                    showErrorModal(data.message, data.type);
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }
}




// Reminder:
// (DONE) Implement: Dapat ma off ang buttons kada change tab since ma off man sd tung select

//(error handling/catching)

//Add 
// bawal mag add ug existing or duplicate na idnumber, courseid, and collegeid

//Delete
//bawal mag delete ug course or college nga naay sulod

//Edit
//bawal i edit ang into existing ang idnumber, courseid, ug college id

//Features to add
//Add - maka add, upload(to cloudyinary and preview ug profile pic 
//Edit - maka usab ug imong profile pic or i clear ang profile pic
// (DONE)default na pic if walay profile