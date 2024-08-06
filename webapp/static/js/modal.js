function showAddModal() {
    const modal = document.getElementById('add-modal');
    const modalBody = document.getElementById('modal-body');
    const activeTab = document.querySelector('.tab-button.active').id.replace('-tab', '');

    let modalContent = '';

    if (activeTab === 'student') {
        modalContent = `
            <form id="add-student-form">
                <label for="student-id">ID-Number:</label>
                <input type="text" id="student-id" name="studentId"><br>

                <label for="first-name">First Name:</label>
                <input type="text" id="first-name" name="firstName"><br>

                <label for="last-name">Last Name:</label>
                <input type="text" id="last-name" name="lastName"><br>

                <label for="course-name">Course Name:</label>
                <input type="text" id="course-name" name="courseName"><br>


                <div class="year-and-gender>">
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

                <button type="submit" class="confirm-button"disabled>Confirm</button>
            </form>
        `;
        modal.className = 'modal student-modal';

    } else if (activeTab === 'course') {
        modalContent = `
            <form id="add-course-form">
                <label for="course-code">Course Code:</label>
                <input type="text" id="course-code" name="courseCode"><br>
                <label for="course-name">Course Name:</label>
                <input type="text" id="course-name" name="courseName"><br>
                <label for="college-name">College Name:</label>
                <input type="text" id="college-name" name="collegeName"><br>
                <button type="submit" class="confirm-button"disabled>Confirm</button>
            </form>
        `;
        modal.className = 'modal course-modal';

    } else if (activeTab === 'college') {
        modalContent = `
            <form id="add-college-form">
                <label for="college-code">College Code:</label>
                <input type="text" id="college-code" name="collegeCode"><br>
                <label for="college-name">College Name:</label>
                <input type="text" id="college-name" name="collegeName"><br>
                <button type="submit" class="confirm-button"disabled>Confirm</button>
            </form>
        `;
        modal.className = 'modal college-modal';
    }

    modalBody.innerHTML = modalContent;
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

document.addEventListener('DOMContentLoaded', function() {
    document.addEventListener('submit', function(event) {
        if (event.target.id === 'add-student-form') {
            event.preventDefault();
            // Handle student form submission
            const formData = new FormData(event.target);
            const studentData = Object.fromEntries(formData.entries());
            console.log(studentData);
            closeModal();
        } else if (event.target.id === 'add-course-form') {
            event.preventDefault();
            // Handle course form submission
            const formData = new FormData(event.target);
            const courseData = Object.fromEntries(formData.entries());
            console.log(courseData);
            closeModal();
        } else if (event.target.id === 'add-college-form') {
            event.preventDefault();
            // Handle college form submission
            const formData = new FormData(event.target);
            const collegeData = Object.fromEntries(formData.entries());
            console.log(collegeData);
            closeModal();
        }
    });
});

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
//default na pic if walay profile

//Refresh idea
//Clear the current rows and upload the new list without refreshing the window.

