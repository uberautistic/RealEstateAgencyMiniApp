document.addEventListener('DOMContentLoaded', function () {
    const user = Telegram.WebApp.initDataUnsafe.user;
    const sendApplicationButton = document.getElementById('send-application-button');
    sendApplicationButton.addEventListener('click', async function () {
        // Если пользователь существует, добавляем его user_id и first_name в URL, иначе редирект без него
        if (user && user.id) {
            const response = await fetch('https://loosely-pleasant-dace.cloudpub.ru/api/phone_number?user_id='+user.id, {
                method: 'GET',
                headers:{
                    'Content-type':'application/json'
                }});
            const result = await response.json();
            console.log('Response from /phone_number:', result);
            const phone_number = result.phone_number;
            if (phone_number==="no user") {
                alert('Вы не зарегистрированы в нашем боте, пожалуйста, пройдите процедуру регистрации');
                return;
            } else {
                window.location.href = `/form?user_id=${user.id}&first_name=${user.first_name}&phone_number=${phone_number}`;
            }
        } else {
            window.location.href = `/form`;
        }
    });
});