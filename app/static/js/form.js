document.addEventListener('DOMContentLoaded', () => {
  const applicationForm = document.getElementById('applicationForm');
  const successPopup = document.getElementById('successPopup');
  const closePopupButton = document.getElementById('closePopup');

  applicationForm.addEventListener('submit', async function(event) {
    event.preventDefault();

    const name = document.getElementById('name').value;
    const contact = document.getElementById('phone').value;
    const city = document.getElementById('city').value;
    const application_type = document.getElementById('applicationType').value;
    const application_text = document.getElementById('applicationText').value;
    const userId = document.getElementById('user_id').value;

    if(name.length<2||name.length>50){
        alert('Имя должно быть от 2 до 50 символов');
        return;
    }
    /*if(contact.length<12){
        alert('Введите номер телефона корректно');
        return;
    }*/
    if(city.length<2||city.length>50){
        alert('Город должен быть от 2 до 50 символов');
        return;
    }
    if(application_type.length<2||application_type.length>50){
        alert('Тип заявки должен быть от 2 до 50 символов');
        return;
    }
    if(application_text.length<2||application_text.length>250){
        alert('Пожалуйста, опишите более развернуто');
        return;
    }
    const applicationData = {
        name:name,
        contact:contact,
        city:city,
        application_type: application_type,
        application_text: application_text,
        user_id: userId
    }
    const jsonData= JSON.stringify(applicationData);

    try{
        const response = await fetch('api/application', {
            method: 'POST',
            headers:{
                'Content-type':'application/json'
            },
            body: jsonData
        });
        const result = await response.json();
        //console.log('Response from /form:', result);
    } catch(error) {
        console.error('Error sending POST request:', error)
    }
    successPopup.classList.add('open');
  });

  closePopupButton.addEventListener('click', function() {
    setTimeout(()=>{
        window.Telegram.WebApp.close();
    }, 100);
    successPopup.classList.remove('open');
  });
});