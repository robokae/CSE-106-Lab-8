let xhttp = new XMLHttpRequest();
let method;
let baseURL = "http://localhost:5000";
let async = true;

const tableHeadings = {
    enrolledTableHeadings: ["Name", "Instructor", "Time", "Enrollment"],
    addTableHeadings: ["Option", "Name", "Instructor", "Time", "Enrollment"],
    instructorCoursesHeadings: ["Name", "Instructor", "Time", "Enrollment"],
    courseGradebookHeadings: ["Student", "Grade"]
}

function generateHTML(tableData, headings) {
    let headingsHTML = "";
    let tableBodyHTML = "";
    let tableRowLength;

    for (let i = 0; i < headings.length; i++) {
        headingsHTML += `<th>${headings[i]}</th>`;
    }

    for (let j = 0; j < tableData.length; j++) {
        tableBodyHTML += "<tr>"

        tableRowLength = Object.keys(tableData[j]).length;

        for (let k = 0; k < tableRowLength; k++) {
            tableBodyHTML += `<td>${tableData[j][headings[k].toLowerCase()]}</td>`;
        }

        tableBodyHTML += "</tr>";
    }

    return {
        headingsHTML,
        tableBodyHTML
    };
}

function generateTable(headingType, dataFromServer) {
    let headingsRow = document.querySelector(".headings-row");
    let tableBody = document.querySelector(".data-table-body");

    let tableData = JSON.parse(dataFromServer);

    switch (headingType) {
        case ("enrolled"):
            tableHTML = generateHTML(tableData, tableHeadings.enrolledTableHeadings);
            break;
        case ("add"):
            tableHTML = generateHTML(tableData, tableHeadings.addTableHeadings);
            break;
    }

    headingsRow.innerHTML = tableHTML.headingsHTML;
    tableBody.innerHTML = tableHTML.tableBodyHTML;
}


function getTable(nameOfTab, studentName) {
    let enrolledTab = document.querySelector(".enrolled-tab");
    let addTab = document.querySelector(".add-tab");

    // get enrolled table 
    if (nameOfTab === "enrolled") {
        // change tab styling
        if (!enrolledTab.classList.contains("active-tab")) {
            enrolledTab.classList.add("active-tab");
        }
        
        if (addTab.classList.contains("active-tab")) {
            addTab.classList.remove("active-tab");
        }

        method = "GET";
        let url = `${baseURL}/enrolled/${studentName}`;
        xhttp.open(method, url, async);

        xhttp.onload = function() {
            generateTable(nameOfTab, this.response);
        };
        
        xhttp.send();
    }

    // get add table
    else if (nameOfTab === "add") {
        // change tab styling
        if (!addTab.classList.contains("active-tab")) {
            addTab.classList.add("active-tab");
        }

        if (enrolledTab.classList.contains("active-tab")) {
            enrolledTab.classList.remove("active-tab");
        }

        method = "GET";
        url = `${baseURL}/courses`;
        xhttp.open(method, url, async);

        xhttp.onload = function() {
            generateTable(nameOfTab, this.response);
        };

        xhttp.send();
    }
}