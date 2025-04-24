document.addEventListener('DOMContentLoaded', () => {
    // Modal functionality
    const modal = document.getElementById("request-modal");
    const openModalButton = document.getElementById("open-request-modal");
    const closeButton = document.querySelector(".modal-content .close-button");

    openModalButton.onclick = function() {
        modal.style.display = "block";
    }

    closeButton.onclick = function() {
        modal.style.display = "none";
    }

    // Close the modal when clicking outside of it
    window.onclick = function(event) {
        if (event.target == modal) {
            modal.style.display = "none";
        }
    }

    // Prevent modal from closing when clicking inside the form
    const modalContent = document.querySelector(".modal-content");
    modalContent.onclick = function(event) {
        event.stopPropagation(); // Stop the click from propagating to the window
    }


    // Simple Carousel Functionality (Swipe/Drag)
    const carouselTrack = document.querySelector('.carousel-track');
    const carouselContainer = document.querySelector('.carousel-container');
    const items = document.querySelectorAll('.carousel-item');
    const paginationContainer = document.querySelector('.carousel-pagination');

    if (items.length > 0) {
         let currentIndex = 0;
         let isDragging = false;
         let startPos = 0;
         let currentTranslate = 0;
         let prevTranslate = 0;
         let animationFrame;

        // Create pagination dots
        for (let i = 0; i < items.length; i++) {
            const dot = document.createElement('span');
            dot.classList.add('pagination-dot');
            if (i === 0) {
                dot.classList.add('active');
            }
            dot.addEventListener('click', () => moveToSlide(i));
            paginationContainer.appendChild(dot);
        }

        const paginationDots = paginationContainer.querySelectorAll('.pagination-dot');

        function setPositionByIndex() {
            currentTranslate = currentIndex * -items[0].clientWidth;
            prevTranslate = currentTranslate;
            setSliderPosition();
            updatePagination();
        }

        function setSliderPosition() {
            carouselTrack.style.transform = `translateX(${currentTranslate}px)`;
        }

        function updatePagination() {
            paginationDots.forEach((dot, index) => {
                if (index === currentIndex) {
                    dot.classList.add('active');
                } else {
                    dot.classList.remove('active');
                }
            });
        }

        function moveToSlide(index) {
            if (index < 0 || index >= items.length) return;
            currentIndex = index;
            setPositionByIndex();
        }


        // Mouse and Touch event listeners
        carouselTrack.addEventListener('touchstart', touchStart);
        carouselTrack.addEventListener('touchend', touchEnd);
        carouselTrack.addEventListener('touchmove', touchMove);

        carouselTrack.addEventListener('mousedown', touchStart);
        carouselTrack.addEventListener('mouseup', touchEnd);
        carouselTrack.addEventListener('mousemove', touchMove);
        carouselTrack.addEventListener('mouseleave', touchEnd); // End drag if mouse leaves

        function getPositionX(event) {
            return event.type.includes('mouse') ? event.pageX : event.touches[0].clientX;
        }

        function touchStart(event) {
            isDragging = true;
            startPos = getPositionX(event);
            carouselTrack.style.transition = 'none'; // Remove transition while dragging
            animationFrame = requestAnimationFrame(animation); // Start animation loop for smooth dragging
        }

        function touchMove(event) {
            if (!isDragging) return;
            const currentPosition = getPositionX(event);
            const moveDistance = currentPosition - startPos;
            currentTranslate = prevTranslate + moveDistance;

            // Optional: Add boundary checks if needed, but min-width handles basic flow
            // Prevent dragging past the first/last slide might be added here
        }

        function touchEnd() {
            cancelAnimationFrame(animationFrame); // Stop animation loop
            isDragging = false;
            carouselTrack.style.transition = 'transform 0.3s ease-in-out'; // Re-add transition

            const movedBy = currentTranslate - prevTranslate;
            const itemWidth = items[0].clientWidth;

            // Determine if we should change slide
            // If moved more than 25% of the item width
            if (movedBy < -itemWidth / 4 && currentIndex < items.length - 1) {
                currentIndex += 1;
            } else if (movedBy > itemWidth / 4 && currentIndex > 0) {
                currentIndex -= 1;
            }

            // Move to the calculated index
            setPositionByIndex();
        }

        function animation() {
            setSliderPosition();
            if (isDragging) requestAnimationFrame(animation);
        }

        // Update carousel position and item width on window resize
        window.addEventListener('resize', setPositionByIndex);

        // Initial setup
        setPositionByIndex();

    } else {
         console.warn("No carousel items found.");
         // Hide carousel or show message if no items
         carouselContainer.style.display = 'none';
         paginationContainer.style.display = 'none';
    }

     // Form Submission (Basic Example - no backend)
     const requestForm = document.getElementById("request-form");
     requestForm.addEventListener('submit', async function(event) {
         event.preventDefault(); // Prevent actual form submission

         const name = document.getElementById('name').value;
         const contact = document.getElementById('phone').value;
         const application_text = document.getElementById('message').value;
         const object_id = document.getElementById('object_id').value;
         const user_id = document.getElementById('user_id').value;

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
            application_text: application_text,
            object_id: object_id,
            user_id: user_id
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
                modal.style.display = "none";
                requestForm.reset();

            } else{
                alert('При отправке заявки что-то пошло не так, пожалуйста повторите попытку.');
            }
        } catch(error){
            console.error('Error sending POST request:', error)
        }
     });

});

