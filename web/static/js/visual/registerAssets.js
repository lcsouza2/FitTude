export function setPasswordRequirementsVisible(passwordContainer) {
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

export function setPasswordRequirementsHidden(passwordContainer) {

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

