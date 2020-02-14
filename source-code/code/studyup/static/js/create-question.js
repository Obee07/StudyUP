/*
LICENSE
This is a course requirement for CS 192 Software Engineering II 
under the supervision of Asst. Prof. Ma. Rowena C. Solamo 
of the Department of Computer Science, College of Engineering, 
University of the Philippines, Diliman for the AY 2019-2020

AUTHORS: Ang, Karina Kylle L. 
         Kopio, Katrina Mae D. 
         Principio, Roberto Jr. D.

CODE HISTORY
01-23-2020 Principio - File created, code added, documentation added

INFO
File Creation Date: January 24, 2020
Development Group: Group 9 - StudyUP Team
Client Group: Ma'am Solamo, CS 192 Class
Purpose of the Software: To provide a collaborative learning
    environment in the courses of UP Diliman.
*/

//Bootstrap Client-Side Validation
(function() {
'use strict';
window.addEventListener('load', function() {  
    var forms = document.getElementsByClassName('needs-validation');
    var validation = Array.prototype.filter.call(forms, function(form) {
    form.addEventListener('submit', function(event) {
        if (form.checkValidity() === false) {
        event.preventDefault();
        event.stopPropagation();
        console.log('MAY MALI')
        }
        form.classList.add('was-validated');
    }, false);
    });
}, false);
})();

//Client-Side Validation for Choice
let choiceErrorMsg = document.getElementById('choice-error')
let q_form = document.getElementById('qForm')

q_form.addEventListener('submit', () => {
    if ($('input[name=solution_id]:checked').length <= 0) { 
        choiceErrorMsg.classList.add('d-block')  
        event.preventDefault()
        event.stopPropagation()
    }
})

q_form.addEventListener('change', () => {
    if ($('input[name=solution_id]:checked').length > 0) {  
        choiceErrorMsg.classList.remove('d-block')
    } 
})

let optionMenu = document.getElementById('options')

//Modal popup for exit question creation
let exitClick = document.getElementsByClassName('click-exit')
for (let i = 0; i < exitClick.length; i++) {
    exitClick[i].addEventListener("mouseenter", function() {
        $('#Modal').modal('toggle')
    })
}

/*
Name: toggleBtnOn
Creation Date: Jan 23, 2020
Purpose: adds 'sClass' class for the arg 'on', removes class of each element in 'offList'
Args: on (DOM element) - is the element to have 'sClass' class added
      offList (list of DOM elements) - stores elements that will have 'sClass' class deleted
      sClass (string) - name of class to be added to 'on', removed for 'offList'
Return value: None
*/

function toggleBtnOn(on, offList, sClass) {
    for (let i = 0; i < sClass.length; i++) {
        on.classList.add(sClass[i])
    }
    for (let i = 0; i < offList.length; i++) {
        if (on === offList[i]) {
        } else {
            for (let j = 0; j < sClass.length; j++) {
                offList[i].classList.remove(sClass[j])
            }
        }   
    }
}

/*
Name: toggleBtnOff
Creation Date: Jan 23, 2020
Purpose: removes 'sClass' class for the arg 'off', adds class of each element in 'onList'
Args: off (DOM element) - is the element to have 'sClass' class removed
      onList (list of DOM elements) - stores elements that will have 'sClass' class added
      sClass (string) - name of class to be removed to 'on', added for 'onList'
Return value: None
*/
function toggleBtnOff(off, onList, sClass) {
    for (let i = 0; i < sClass.length; i++) {
        off.classList.remove(sClass[i])
    }
    for (let i = 0; i < onList.length; i++) {
        if (off === onList[i]) {
        } else {
            for (let j = 0; j < sClass.length; j++) {
                onList[i].classList.add(sClass[j])
            }
        }   
    }
}

/*
Name: toggle
Creation Date: Jan 23, 2020
Purpose: toggle logic for Unit buttons
Args: num (string) - determines which button is to be toggled
Return value: None
*/
function toggle(num) {
    if (num === '1') {
    toggleBtnOn(label_1, unitLabelList, ["active"])
    optionMenu.disabled = false
    getTopics(num, 1)
        
    } else if (num === '2') {
    toggleBtnOn(label_2, unitLabelList, ["active"])
    optionMenu.disabled = false
    getTopics(num, 6)
    
    } else if (num === '3') {
    toggleBtnOn(label_3, unitLabelList, ["active"])
    optionMenu.disabled = false
    getTopics(num, 11)
    }
}
let fc_1 = document.getElementById('fc_1')
let fc_2 = document.getElementById('fc_2')
let fc_3 = document.getElementById('fc_3')
let fc_4 = document.getElementById('fc_4')
fcList = [fc_1, fc_2, fc_3, fc_4]
    
let c_1 = document.getElementById('c_1')
let c_2 = document.getElementById('c_2')
let c_3 = document.getElementById('c_3')
let c_4 = document.getElementById('c_4')
cList = [c_1, c_2, c_3, c_4]

//Adding event listeners for select correct answer choice buttons
for (let i = 0; i < cList.length; i++) {
    cList[i].addEventListener('click', function() {
        toggle2('c'+(i+1).toString())
    })
}

/*
Name: toggle2
Creation Date: Jan 23, 2020
Purpose: toggle logic for correct choice buttons
Args: num (string) - determines which button is to be toggled
Return value: None
*/
function toggle2(num) {
    if (num === 'c1') {
        toggleBtnOn(c_1, cList, ['btn-success', 'active'])
        toggleBtnOn(fc_1, fcList, ['green-bg'])
        toggleBtnOff(c_1, cList, ['btn-secondary'])
        
    } else if (num === 'c2') {
        toggleBtnOn(c_2, cList, ['btn-success', 'active'])
        toggleBtnOn(fc_2, fcList, ['green-bg'])
        toggleBtnOff(c_2, cList, ['btn-secondary'])
        
    } else if (num === 'c3') {
        toggleBtnOn(c_3, cList, ['btn-success', 'active'])
        toggleBtnOn(fc_3, fcList, ['green-bg'])
        toggleBtnOff(c_3, cList, ['btn-secondary'])
        
    } else if (num === 'c4') {
        toggleBtnOn(c_4, cList, ['btn-success', 'active'])
        toggleBtnOn(fc_4, fcList, ['green-bg'])
        toggleBtnOff(c_4, cList, ['btn-secondary']) 
    } 
}



/*
ARCHIVE
Name: getTopics (API)
Creation Date: Jan 23, 2020
Purpose: calls an API to fetch the topics for a given unit, for dynamic select
Args: unit (string) - determines which subroute the API calls
      startChap (int) - counter for optgroup labels
Return value: None
*/
// function getTopics(unit, startChap) {
//     fetch('/topic' + '/' + unit).then(function(response) { 
//         response.json().then(function(data) {
//             let optionHTML = ''
//             let currChapNo = startChap
//             let hasPrinted = false
//             for (let topic of data.topics) {
//                 if (topic.chapNo != currChapNo) {
//                     currChapNo += 1
//                     hasPrinted = false
//                 }
//                 if (hasPrinted) {
//                 } else {
//                     optionHTML += '<optgroup label = "Chapter ' + currChapNo + '">'
//                     hasPrinted = true
//                 }
//                 optionHTML += '<option class = "form-control" value="' + topic.id + '">'+ topic.name + '</option>'
//             }
//         optionMenu.innerHTML = optionHTML
//         })
//     });
// }
