odoo.define('payment_areeba.areeba', function (require) {
    "use strict";
    
    require('web.dom_ready');
    if (!$('.o_payment_form').length) {
        return Promise.reject("DOM doesn't contain '.o_payment_form'");
    }
    
    var observer = new MutationObserver(function (mutations, observer) {
        for (var i = 0; i < mutations.length; ++i) {
            for (var j = 0; j < mutations[i].addedNodes.length; ++j) {
                if (mutations[i].addedNodes[j].tagName.toLowerCase() === "form" && mutations[i].addedNodes[j].getAttribute('provider') === 'areeba') {
                    _createAreebaCheckout($(mutations[i].addedNodes[j]));
                }
            }
        }
    });
    
    function getFormData($form) {
        var unindexed_array = $form.serializeArray();
        var indexed_array = {};

        $.map(unindexed_array, function (n, i) {
            indexed_array[n.name] = n.value;
        });
        return indexed_array;
    }

    function _createAreebaCheckout(providerForm) {
        const formData = getFormData(providerForm);

        Checkout.configure({
            merchant: formData.merchant_id,
            order: {
                amount: formData.amount,
                currency: formData.currency,
                description: formData.reference,
                id: formData.reference,
            },
            session: {
                id: formData.session_id,
            },
            interaction: {
                operation: 'PURCHASE',
                merchant: {
                    name: formData.merchant_name,
                    address: {
                        line1: formData.merchant_street,
                        line2: formData.merchant_street2,
                    },
                    logo: formData.logo,
                },
            },
        });

        Checkout.showPaymentPage();
    };

    _createAreebaCheckout($('form[provider="areeba"]'));
});
    