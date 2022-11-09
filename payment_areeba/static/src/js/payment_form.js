odoo.define('payment_areeba.payment_form', function (require) {
   
    
    const PaymentForm = require('payment.payment_form');
    
    PaymentForm.include({
        willStart: function () {
            const script = document.createElement('script');
            script.src = 'https://epayment.areeba.com/checkout/version/60/checkout.js';
            script.setAttribute('data-error', 'errorCallback');
            document.head.append(script);
            window.errorCallback  = (err) => {
                this.displayError(err.cause, err.explanation);
            };
            return this._super.apply(this, arguments);
        },
    });
});
    