document.addEventListener('DOMContentLoaded', () => {
    const filterToggleBtn = document.getElementById('filterToggleBtn');
    const filterForm = document.getElementById('filterForm');
    const requestBtn = document.getElementById('requestBtn');
    const requestModal = document.getElementById('requestModal');
    const successModal = document.getElementById('successModal');
    const applicationForm = document.getElementById('applicationForm')

    const modalCloseButtons = document.querySelectorAll('.close-button');

    // Переключение видимости фильтра
    filterToggleBtn.addEventListener('click', () => {
        filterForm.classList.toggle('hidden');
    });

    // Открытие модального окна заявки
    requestBtn.addEventListener('click', () => {
        requestModal.classList.remove('hidden');
    });

    // Закрытие модальных окон по крестику
    modalCloseButtons.forEach(button => {
        button.addEventListener('click', () => {
            const modal = button.closest('.modal');
            if (modal) {
                modal.classList.add('hidden');
            }
        });
    });

    // Закрытие модальных окон при клике вне окна
    window.addEventListener('click', (event) => {
        if (event.target.classList.contains('modal')) {
            event.target.classList.add('hidden');
        }
    });

    applicationForm.addEventListener('submit', async function(event){
        event.preventDefault();

        const name = document.getElementById('name').value;
        const contact = document.getElementById('phone').value;
        const city = document.getElementById('city_id').value;
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

        if(application_text.length<2||application_text.length>250){
        alert('Пожалуйста, опишите более развернуто');
        return;
        }
        const applicationData = {
            name:name,
            contact:contact,
            city_id:city,
            application_type: application_type,
            application_text: application_text,
            user_id: userId
        }
        const jsonData= JSON.stringify(applicationData);

        try{
            const response = await fetch('/api/application',{
                method: 'POST',
                headers:{
                    'Content-Type':'application/json'
                },
                body: jsonData
            });
            const result = await response.json()
            if (result.message === "success"){
                alert('Ваша заявка принята, скоро с Вами свяжется наш сотрудник.');
                requestModal.classList.add('hidden');
                applicationForm.reset();
            } else{
                alert('При отправке заявки что-то пошло не так, пожалуйста повторите попытку.');
            }
        } catch(error){
            console.error('Error sending POST request:', error)
        }
   });

   filterForm.addEventListener('submit', async function(event){
        const priceFrom = document.getElementById('priceFrom');
        const priceTo = document.getElementById('priceTo');
        const areaFrom = document.getElementById('areaFrom');
        const areaTo = document.getElementById('areaTo');

        let stop = false;
        if(priceFrom.value>priceTo.value||(priceFrom.value&&priceTo.value&&priceFrom.value===priceTo.value)){
            alert('Задайте диапазон цен корректно.');
            stop = true;
        }

        if(areaFrom.value>areaTo.value||(areaFrom.value&&areaTo.value&&areaFrom.value===areaTo.value)){
            alert('Задайте диапазон площади корректно.');
            stop = true;
        }

        if(stop){
            event.preventDefault();
            return;
        }

        const formData = new FormData(this);

        // Удаляем пустые поля цен
        if (!formData.get('price_from')) {
        formData.delete('price_from');
        }
        if (!formData.get('price_to')) {
            formData.delete('price_to');
        }

        // Удаляем пустые поля площади
        if (!formData.get('area_from')) {
            formData.delete('area_from');
        }
        if (!formData.get('area_to')) {
            formData.delete('area_to');
        }

        // Отправляем форму с отфильтрованными данными
        const queryString = new URLSearchParams(formData).toString();

        // Отменяем стандартное поведение формы
        event.preventDefault();

        // Выполняем запрос с отфильтрованными данными
        fetch(`filter?${queryString}`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.text())
        .then(data => {
            document.querySelector('#propertyListings').innerHTML = data;
        })
        .catch(error => console.error('Ошибка:', error));

        filterForm.classList.toggle('hidden');
   });
});

