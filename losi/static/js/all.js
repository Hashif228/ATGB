    function switchTo(type) {
      const slider = document.getElementById('formSlider');
      const patientBtn = document.getElementById('patientBtn');
      const doctorBtn = document.getElementById('doctorBtn');
      const loginBox = document.getElementById('loginBox');

      if (type === 'patient') {
        slider.style.transform = 'translateX(0)';
        patientBtn.classList.add('active');
        doctorBtn.classList.remove('active');
        loginBox.style.backgroundImage = "url('https://images.unsplash.com/photo-1607746882042-944635dfe10e?auto=compress&cs=tinysrgb&dpr=2&h=1000')";
      } else {
        slider.style.transform = 'translateX(-50%)';
        doctorBtn.classList.add('active');
        patientBtn.classList.remove('active');
        loginBox.style.backgroundImage = "url('https://images.unsplash.com/photo-1588776814546-ec7a9b55f9f0?auto=compress&cs=tinysrgb&dpr=2&h=1000')";
      }
    }