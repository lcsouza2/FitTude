const senhaInput = document.getElementById('senha');

const requirements = {
    length: document.getElementById('length-check'),
    uppercase: document.getElementById('uppercase-check'),
    lowercase: document.getElementById('lowercase-check'),
    number: document.getElementById('number-check'),
    special: document.getElementById('special-check')
};

const passwordContainer = document.querySelector('.password-requirements-container');
const passwordRequirements = document.querySelector('.password-requirements');

function setPasswordRequirementsVisible(passwordContainer) {
    passwordContainer.classList.add('active');

    passwordContainer.animate([
        {width: '0%', height: '0px'},
        {width: '100%', height: '100%   '}
    ], {
        duration: 500,
        easing: 'ease',
        fill: 'forwards'
    });
}

function setPasswordRequirementsHidden(passwordContainer) {

    passwordContainer.animate([
            {width: '100%', height: '100%'},
            {width: '0%', height: '0px'}
        ], {
            duration: 500,
            easing: 'ease',
            fill: 'forwards'
      });

    passwordContainer.classList.remove('visible');
}

senhaInput.addEventListener('focus', function() {
        setPasswordRequirementsVisible(passwordContainer);

        requestAnimationFrame(() => {
        passwordRequirements.classList.add('visible');
    });
});

senhaInput.addEventListener('blur', function() {
    setPasswordRequirementsHidden( passwordContainer);

    setTimeout(() => {
        passwordContainer.classList.remove('active');
    }, 300); 

});

senhaInput.addEventListener('input', function() {
    const senha = this.value;

    if(senha.length >= 8) {
        requirements.length.classList.add('valid');
    } else {
        requirements.length.classList.remove('valid');
    }
    
    if(/[A-Z]/.test(senha)) {
        requirements.uppercase.classList.add('valid');
    } else {
        requirements.uppercase.classList.remove('valid');
    }
    
    if(/[a-z]/.test(senha)) {
        requirements.lowercase.classList.add('valid');
    } else {
        requirements.lowercase.classList.remove('valid');
    }
    
    if(/[0-9]/.test(senha)) {
        requirements.number.classList.add('valid');
    } else {
        requirements.number.classList.remove('valid');
    }
    
    if(/[!@#$%^&*(),.?":{}|<>/]/.test(senha)) {
        requirements.special.classList.add('valid');
    } else {
        requirements.special.classList.remove('valid');
    }
});
