
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
        }
        form.classList.add('was-validated');
    }, false);
    });
}, false);
})();

//Client-Side Validation for Unit, Choice
let unitErrorMsg = document.getElementById('unit-error')
let choiceErrorMsg = document.getElementById('choice-error')
let q_form = document.getElementById('qForm')

q_form.addEventListener('submit', (event) => {
    if ($('input[name=unit_no]:checked').length <= 0) {   
        unitErrorMsg.classList.add('d-block')  
        event.preventDefault()
        event.stopPropagation() 
    } 
})
q_form.addEventListener('change', () => {
    if ($('input[name=unit_no]:checked').length > 0) {  
        unitErrorMsg.classList.remove('d-block')
    } 
})
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

//Unit Button Input
let label_1 = document.getElementById('label_unit_no-0')
let label_2 = document.getElementById('label_unit_no-1')
let label_3 = document.getElementById('label_unit_no-2')
let optionMenu = document.getElementById('options')
let unitLabelList = [label_1, label_2, label_3]

for (let i = 0; i < unitLabelList.length; i++) {
    unitLabelList[i].addEventListener('click', function() {
        toggle((i+1).toString())
    })
}
    
//Modal popup for exit question creation
let exitClick = document.getElementsByClassName('click-exit')
for (let i = 0; i < exitClick.length; i++) {
    exitClick[i].addEventListener("mouseenter", function() {
        $('#Modal').modal('toggle')
    })
}

//getTopics fetches list of topics for a given unit
function getTopics(unit, startChap) {
    fetch('/topic' + '/' + unit).then(function(response) { 
        response.json().then(function(data) {
            let optionHTML = ''
            let currChapNo = startChap
            let hasPrinted = false
            for (let topic of data.topics) {
                if (topic.chapNo != currChapNo) {
                    currChapNo += 1
                    hasPrinted = false
                }
                if (hasPrinted) {
                } else {
                    optionHTML += '<optgroup label = "Chapter ' + currChapNo + '">'
                    hasPrinted = true
                }
                optionHTML += '<option class = "form-control" value="' + topic.id + '">'+ topic.name + '</option>'
            }
        optionMenu.innerHTML = optionHTML
        })
    });
}

//turns on classes, turns off for offList
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

//turns off classes, turns on for onList
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

// Unit Buttons
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
for (let i = 0; i < fcList.length; i++) {
    fcList[i].addEventListener('click', function() {
        toggle2('c'+(i+1).toString())
    })
}

//Choice Buttons
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
