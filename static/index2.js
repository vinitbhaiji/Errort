function closeWindow(){
    alert("This looks good!!")
    input_img=document.getElementById("img");
    img1=URL.createObjectURL(input_img.files[0]);
    
    window.close()
}

function update(){
    fetch('/change_flag')
}

function update1(){
    fetch('/change_flag1')
}

function update2(){
    fetch('/change_flag2')
}

function showerrors(){
    fetch('/errordetected')
    .then(response => response.json())
    .then(data => {
        // Display the values on the HTML page
        // document.getElementById('value').innerText = data.value;
        const iconDiv=document.getElementById('value')
        const flagValue=data.value
        if (flagValue === 1) {
            iconDiv.innerHTML = '✅'; // Right tick icon
        } else if (flagValue === 2) {
            iconDiv.innerHTML = '❌'; // Wrong tick icon
        } else {
            iconDiv.innerHTML = '❓'; // Question mark for unknown flag value
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function setValue() {
    fetch('/reset')
    const newValue = ' ' ;
    document.getElementById('value').innerText = newValue;
}